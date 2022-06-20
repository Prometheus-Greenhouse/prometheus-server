from typing import List, Set, Tuple, Union

import orjson
from SpiffWorkflow import SequenceFlow
from SpiffWorkflow.bpmn.specs.ExclusiveGateway import ExclusiveGateway
from SpiffWorkflow.bpmn.specs.events import StartEvent
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.camunda.parser.CamundaParser import CamundaParser
from SpiffWorkflow.camunda.specs.UserTask import UserTask
from SpiffWorkflow.specs import TaskSpec
from lxml import etree

from apps.workflow.generator.state_spec import StateSpec
from apps.workflow.generator.store import Store
from apps.workflow.generator.transition_spec import TransitionSpec
from project.utils import functions
from project.utils.functions import emp_str


class WorkflowGenerator:
    transitions: List[TransitionSpec] = list()
    class_strings: List[str] = list()
    state_specs: List[StateSpec] = list()

    def __init__(self, filename, spec, store=Store("./")):
        self.filename = filename
        self.spec = spec
        self.store = store

    def extract_exclusive_gateway(self, gateway: ExclusiveGateway) -> Tuple[List[UserTask], List[TransitionSpec]]:
        start_node_id = gateway.inputs[0].name
        possible_states: [TransitionSpec] = list()
        for seq in gateway.get_outgoing_sequences():
            seq: SequenceFlow
            target_task: UserTask = seq.target_task_spec
            transition_id = f"{emp_str(start_node_id)}_{seq.name}_{target_task.name}"
            transition = TransitionSpec(
                id=transition_id,
                action=seq.name,
                start_node_id=start_node_id,
                next_node_id=target_task.name,
                status_out_message=f"{seq.documentation}",
            )
            self.transitions.append(transition)
            possible_states.append(transition)
        return list(map(lambda seq: seq.target_task_spec, gateway.get_outgoing_sequences())), possible_states

    def travel_states(self, state: Union[UserTask, StartEvent]) -> List[TaskSpec]:
        try:
            state_spec = StateSpec(id=state.name, name=state.description, documentation=orjson.loads(state.documentation))
        except Exception:
            state_spec = StateSpec(id=state.name, name=state.description, documentation={})
        seqs = list(state.get_outgoing_sequences())
        new_states: List[TaskSpec] = list()
        if seqs:
            seq: SequenceFlow = seqs[0]
            target_task = seq.target_task_spec
            if isinstance(target_task, ExclusiveGateway):
                next_tasks, possible_state = self.extract_exclusive_gateway(target_task)
                state_spec.possible_states += possible_state
                new_states = [*next_tasks, target_task]
            if isinstance(target_task, UserTask):
                transition_id = f"{emp_str(state.name)}_{seq.name}_{target_task.name}"
                transition = TransitionSpec(
                    id=transition_id,
                    action=seq.name,
                    start_node_id=state.name,
                    next_node_id=target_task.name,
                    status_out_message=f"{seq.documentation}",
                )
                self.transitions.append(transition)
                state_spec.possible_states.append(transition)
                new_states = [target_task]
        self.state_specs.append(state_spec)
        return new_states

    def get_all_states(self, parser: CamundaParser) -> Set[TaskSpec]:
        workflow = BpmnWorkflow(parser.get_spec(self.spec))
        workflow.do_engine_steps()
        ready_tasks = workflow.get_tasks()
        closes: Set[TaskSpec] = set()
        opens: Set[TaskSpec] = set(map(lambda t: t.task_spec, ready_tasks))
        while len(opens) > 0:
            task = opens.pop()
            if isinstance(task, UserTask) and task not in closes:
                seqs = list(task.get_outgoing_sequences())
                if seqs:
                    seq: SequenceFlow = seqs[0]
                    opens.add(seq.target_task_spec)
            if isinstance(task, ExclusiveGateway) and task not in closes:
                for seq in task.get_outgoing_sequences():
                    opens.add(seq.target_task_spec)
            closes.add(task)
        return closes

    def generate(self) -> None:
        parser = CamundaParser()
        f = functions.op(self.filename, 'r', encoding="utf8")
        parser.add_bpmn_xml(etree.parse(f), filename=self.filename)
        workflow = BpmnWorkflow(parser.get_spec(self.spec))
        workflow.do_engine_steps()
        closes: Set[TaskSpec] = set()
        opens: Set[TaskSpec] = self.get_all_states(parser)
        while len(opens) > 0:
            task = opens.pop()
            if isinstance(task, UserTask) and task not in closes:
                opens.union(set(self.travel_states(task)))
            if isinstance(task, ExclusiveGateway) and task not in closes:
                for seq in task.get_outgoing_sequences():
                    seq: SequenceFlow
                    target_task: UserTask = seq.target_task_spec
                    opens.union(set(self.travel_states(target_task)))
            if isinstance(task, StartEvent) and task.name == "start_event":
                opens.union(set(self.travel_states(task)))
            closes.add(task)

        self.store.save_class(self.state_specs)
        self.store.save_state_enum(self.state_specs)
        self.store.save_transition_enum(self.transitions)
        self.store.save_action_enum(self.transitions)


# async def run_database():
#     mongo_db = AsyncIOMotorDatabase(AsyncIOMotorClient(DATABASES.mongo.url), "los-workflow")
#     node_collection = LosCollection("mst_node", mongo_db)
#     nodes = json.load(functions.op("./code/nodes.json", "r", encoding="utf8"))
#     await node_collection.delete_many({})
#     await node_collection.insert_many(nodes)
#
#     node_link_collection = LosCollection("mst_node_link", mongo_db)
#     node_links = json.load(functions.op("./code/node_links.json", "r", encoding="utf8"))
#     await node_link_collection.delete_many({})
#     await node_link_collection.insert_many(node_links)


if __name__ == "__main__":
    filename = "../../../diagrams/simple_flow.bpmn"
    spec = "states"
    generator = WorkflowGenerator(filename, spec, Store("./code", "./code/constants", "./code/states"))
    generator.generate()
    # asyncio.get_event_loop().run_until_complete(run_database())
