from multiprocessing import Process
from typing import Dict
from uuid import uuid4, UUID

from project.utils import functions


class TaskManager:
    tasks: Dict[UUID, Process] = {}

    def add_task(self, task: Process) -> UUID:
        uuid = uuid4()
        self.tasks.update({uuid: task})
        return uuid

    def kill_task(self, t_id: UUID) -> None:
        t = self.tasks.get(t_id)
        t.terminate()

    def shutdown(self) -> None:
        for uuid, t in self.tasks.items():
            if t:
                t.terminate()
            functions.debug(f"{uuid} terminated")


# TASK_MANAGER = TaskManager()
