import json
import math
from typing import List, Dict, Any, Set, Tuple

from apps.decisiontree.decision_data import DecisionData
from apps.decisiontree.node import Node
from apps.enums.enums import Temperature, Humidity, Soil, ERun, EDayCycle
from project.utils.stream import Stream


class DecisionTree:
    def __init__(self, target: str):
        self.target = target
        self.map_value_set = {
            key: {i.value for i in value}
            for key, value in [*DecisionData.__annotations__.items()]
        }

    def get_value_set(self, prop: str) -> Set[str]:
        return self.map_value_set[prop]

    def calc_entropy(self, p: float, i_list: List[float]) -> float:
        sum = 0
        for i in i_list:
            if i == 0:
                continue
            sum += (-i / p) * math.log2(i / p)
        return sum

    def calc_entropy_from_map(self, p: float, i_map: Dict[Any, Any]) -> float:
        return self.calc_entropy(p, Stream.of(i_map.values()).map(len).to_list())

    def gain_and_create_leaf(self, node: Node, prop: str, H_S: float, data: List[DecisionData]) -> Tuple[float, Dict]:
        H_x_S = 0
        prop_value_set = self.get_value_set(prop)
        decision_map = {}
        for prop_value in prop_value_set:
            child_data = Stream(data).filter(lambda d: getattr(d, prop) == prop_value).to_list()
            child_data_map = {
                target_value: Stream(child_data).filter(lambda d: getattr(d, self.target) ==target_value ).to_list()
                for target_value in self.get_value_set(self.target)
            }
            print(child_data)
            print(child_data_map)
            entropy = self.calc_entropy_from_map(len(child_data), child_data_map)
            if entropy == 0:
                decision_map[prop_value] = Node(node, self.target, child_data)
            H_x_S = len(child_data) / len(data) * entropy
            print(f"({len(child_data)}/{len(data)})*{entropy} = {H_x_S}")

        """Step 3"""
        G_x_S = H_S - H_x_S

        print(f"""{"-" * 50}
{prop}
{"H_S":^12}|{"H_xS":^12}|{"G_xS":^12}
{H_S:^12.2f}|{H_x_S:^12.2f}|{G_x_S:^12.2f}""")
        return G_x_S, decision_map

    def create_node(self, props: List, data: List[DecisionData], parent_node: Node):
        data_map = {
            value: Stream(data).filter(lambda o: getattr(o, self.target) == value).to_list()
            for value in self.get_value_set(self.target)
        }
        biggest_gain = - float("inf")
        node = Node(parent_node, None, data)
        """ STEP 1 """
        H_S = self.calc_entropy_from_map(len(data), data_map)
        """ STEP 2 """
        picked_decision = {}
        for prop in props:
            gain, decision_map = self.gain_and_create_leaf(node, prop, H_S, data)
            if gain > biggest_gain:
                biggest_gain = gain
                picked_node_name = prop
                picked_decision = decision_map

        """ STEP 3"""
        print("picked node: ", picked_node_name)
        node.name = picked_node_name
        node.children = picked_decision

        for prop_value in self.get_value_set(picked_node_name):
            if node.children.get(prop_value):
                continue
            next_props = [*props]
            next_props.remove(picked_node_name)
            next_node_data = Stream.of(data).filter(lambda d: getattr(d, picked_node_name) == prop_value).to_list()
            node.children[prop_value] = self.create_node(next_props, next_node_data, node)
        return node


if __name__ == '__main__':
    data = [
        DecisionData(EDayCycle.DAY, Temperature.HOT, Humidity.HIGH, Soil.LOW, ERun.Y),
        DecisionData(EDayCycle.DAY, Temperature.HOT, Humidity.HIGH, Soil.HIGH, ERun.N),
        DecisionData(EDayCycle.NIGHT, Temperature.HOT, Humidity.HIGH, Soil.LOW, ERun.Y),
        DecisionData(EDayCycle.NIGHT, Temperature.MID, Humidity.HIGH, Soil.LOW, ERun.Y),
        DecisionData(EDayCycle.NIGHT, Temperature.COOL, Humidity.NORMAL, Soil.LOW, ERun.Y),
        DecisionData(EDayCycle.NIGHT, Temperature.COOL, Humidity.NORMAL, Soil.HIGH, ERun.N),
        DecisionData(EDayCycle.DAY, Temperature.COOL, Humidity.NORMAL, Soil.HIGH, ERun.N),
        DecisionData(EDayCycle.DAY, Temperature.MID, Humidity.HIGH, Soil.LOW, ERun.N),
        DecisionData(EDayCycle.DAY, Temperature.COOL, Humidity.NORMAL, Soil.LOW, ERun.N),
        DecisionData(EDayCycle.NIGHT, Temperature.MID, Humidity.NORMAL, Soil.LOW, ERun.N),
        DecisionData(EDayCycle.DAY, Temperature.MID, Humidity.NORMAL, Soil.HIGH, ERun.N),
        DecisionData(EDayCycle.NIGHT, Temperature.MID, Humidity.HIGH, Soil.HIGH, ERun.N),
        DecisionData(EDayCycle.NIGHT, Temperature.HOT, Humidity.NORMAL, Soil.LOW, ERun.Y),
        DecisionData(EDayCycle.DAY, Temperature.MID, Humidity.HIGH, Soil.HIGH, ERun.N),
    ]

    # print(DecisionTree().gain(parent_prop, parent_value_set, child_prop, child_value_set, data))
    decision_tree = DecisionTree("run")
    props = [*DecisionData.__annotations__.keys()]
    props.remove("run")
    tree = decision_tree.create_node(props, data, None)
    d = tree.print_tree()
    print(json.dump(d, open("tree.json", "w")))