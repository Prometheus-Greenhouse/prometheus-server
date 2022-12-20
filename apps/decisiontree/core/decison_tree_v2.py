import json
import math
from typing import Dict, Any, List, Set, Tuple

from apps.decisiontree.core.model import DecisionTreeDataModel
from apps.decisiontree.core.node import Node
from apps.enums.enums import ERunValue, EDayCycleValue, ETemperatureValue, ESoilMoistureValue, EHumidityValue, EWaterValue, ESensorType
from project.utils.stream import Stream


class DecisionTreeCore:
    def __init__(self, target):
        self.target = target

    def get_value_set(self, prop: str) -> Set:
        return {i.value for i in prop}

    def calc_entropy(self, p: float, i_list: List[float]) -> float:
        sum = 0
        for i in i_list:
            if i == 0:
                continue
            sum += (-i / p) * math.log2(i / p)
        return sum

    def calc_entropy_from_map(self, p: float, i_map: Dict[Any, Any]) -> float:
        return self.calc_entropy(p, Stream.of(i_map.values()).map(len).to_list())

    def calc_gain(self, prop: str, data: List, H_S, node: Node) -> Tuple[float, Dict]:
        """"""
        """     
        2.1 Tính toán entropy của tất cả giá trị.
        """
        H_x_S = 0
        pro_value_set = self.get_value_set(prop)
        decision_map = {}
        for prop_value in pro_value_set:
            child_data = Stream(data).filter(lambda d: d.get(prop) == prop_value).to_list()
            child_data_map = {
                target_value: Stream(child_data).filter(lambda o: o.get(self.target) == target_value).to_list()
                for target_value in self.get_value_set(self.target)
            }
            entropy_ = self.calc_entropy_from_map(len(child_data), child_data_map)

            if entropy_ == 0:
                # print("create leaf node here", prop, prop_value)
                decision_map[prop_value] = Node(node, ESensorType.get_sensor_type(self.target), True, child_data[0].get(self.target) if child_data else None, child_data)
            H_x_S += (len(child_data)) / len(data) * entropy_
        """
        2.2 Tính entropy trung bình cho thuộc tính đang thực hiện.
        """
        G_x_S = H_S - H_x_S
        return G_x_S, decision_map

    def create_vote_node(self, data: List[DecisionTreeDataModel], parent_node: Node):
        map_counter = {v: 0 for v in self.get_value_set(self.target)}
        for d in data:
            map_counter[d.get(self.target)] += 1

        max = -float("inf")
        decision = None
        for key, value in map_counter.items():
            if value > max:
                max = value
                decision = key

        return Node(parent_node, ESensorType.get_sensor_type(self.target), True, decision=decision, data=data)

    def create_node(self, props: List, data: List, parent_node: Node = None):
        data_map = {
            value: Stream(data).filter(lambda o: o.get(self.target) == value).to_list()
            for value in self.get_value_set(self.target)
        }
        biggest_gain = - float("inf")
        node = Node(parent_node, None, data=data)
        """ STEP 1 """
        H_S = self.calc_entropy_from_map(len(data), data_map)
        """ STEP 2 """
        picked_decision = {}
        for prop in props:
            gain, decision_map = self.calc_gain(prop, data, H_S, node)
            if gain > biggest_gain:
                biggest_gain = gain
                picked_node_name = prop
                picked_decision = decision_map

        """ STEP 3"""

        # print("picked node: ", picked_node_name)
        node.name = ESensorType.get_sensor_type(picked_node_name)
        node.children = picked_decision

        for prop_value in self.get_value_set(picked_node_name):
            if node.children.get(prop_value):
                continue
            next_props = [*props]
            next_props.remove(picked_node_name)
            next_node_data = Stream.of(data).filter(lambda d: d.get(picked_node_name) == prop_value).to_list()
            if next_props:
                node.children[prop_value] = self.create_node(next_props, next_node_data, node)
            else:
                node.children[prop_value] = self.create_vote_node(next_node_data, node)
        return node


if __name__ == '__main__':
    DAYC = EDayCycleValue
    TEMP = ETemperatureValue
    WATER = EWaterValue
    HUM = EHumidityValue
    SOIL = ESoilMoistureValue
    RUN = ERunValue
    TARGET = RUN
    props = [DAYC, WATER, TEMP, HUM, SOIL]

    data = [
        DecisionTreeDataModel(EDayCycleValue.DAY, EWaterValue.HIGH, ETemperatureValue.HIGH, EHumidityValue.HIGH, ESoilMoistureValue.LOW, ERunValue.Y),
        DecisionTreeDataModel(EDayCycleValue.DAY, EWaterValue.HIGH, ETemperatureValue.HIGH, EHumidityValue.HIGH, ESoilMoistureValue.HIGH, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.NIGHT, EWaterValue.LOW, ETemperatureValue.HIGH, EHumidityValue.HIGH, ESoilMoistureValue.LOW, ERunValue.Y),
        DecisionTreeDataModel(EDayCycleValue.NIGHT, EWaterValue.LOW, ETemperatureValue.HIGH, EHumidityValue.HIGH, ESoilMoistureValue.LOW, ERunValue.Y),
        DecisionTreeDataModel(EDayCycleValue.NIGHT, EWaterValue.LOW, ETemperatureValue.LOW, EHumidityValue.MID, ESoilMoistureValue.LOW, ERunValue.Y),
        DecisionTreeDataModel(EDayCycleValue.NIGHT, EWaterValue.LOW, ETemperatureValue.LOW, EHumidityValue.MID, ESoilMoistureValue.HIGH, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.DAY, EWaterValue.HIGH, ETemperatureValue.LOW, EHumidityValue.MID, ESoilMoistureValue.HIGH, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.DAY, EWaterValue.HIGH, ETemperatureValue.LOW, EHumidityValue.HIGH, ESoilMoistureValue.LOW, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.DAY, EWaterValue.LOW, ETemperatureValue.LOW, EHumidityValue.MID, ESoilMoistureValue.LOW, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.NIGHT, EWaterValue.HIGH, ETemperatureValue.HIGH, EHumidityValue.MID, ESoilMoistureValue.LOW, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.DAY, EWaterValue.HIGH, ETemperatureValue.HIGH, EHumidityValue.MID, ESoilMoistureValue.HIGH, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.NIGHT, EWaterValue.HIGH, ETemperatureValue.HIGH, EHumidityValue.HIGH, ESoilMoistureValue.HIGH, ERunValue.N),
        DecisionTreeDataModel(EDayCycleValue.NIGHT, EWaterValue.LOW, ETemperatureValue.HIGH, EHumidityValue.MID, ESoilMoistureValue.LOW, ERunValue.Y),
        DecisionTreeDataModel(EDayCycleValue.DAY, EWaterValue.HIGH, ETemperatureValue.HIGH, EHumidityValue.HIGH, ESoilMoistureValue.HIGH, ERunValue.N),
    ]
    core = DecisionTreeCore(TARGET)
    tree = core.create_node(props, data, None)
    print(tree.print_tree())
    print(json.dump(tree.print_tree(), open("tree.json", "w")))
