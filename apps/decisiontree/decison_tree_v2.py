import json
import math
from typing import Dict, Any, List, Set, Tuple

from apps.decisiontree.node import Node
from apps.enums.enums import ERun, EDayCycle, Temperature, Soil, Humidity
from project.utils.stream import Stream

DAYC = 0
TEMP = 1
HUM = 2
SOIL = 3
RUN = 4
TARGET = RUN


def get_value_set(prop: str) -> Set:
    map_value_set = [
        {i.value for i in e}
        for e in [EDayCycle, Temperature, Humidity, Soil, ERun]
    ]
    return map_value_set[prop]


def calc_entropy(p: float, i_list: List[float]) -> float:
    sum = 0
    for i in i_list:
        if i == 0:
            continue
        sum += (-i / p) * math.log2(i / p)
    return sum


def calc_entropy_from_map(p: float, i_map: Dict[Any, Any]) -> float:
    return calc_entropy(p, Stream.of(i_map.values()).map(len).to_list())


def calc_gain(prop: int, data: List, H_S, node: Node) -> Tuple[float, Dict]:
    """"""
    """     
    2.1 Tính toán entropy của tất cả giá trị.
    """
    H_x_S = 0
    pro_value_set = get_value_set(prop)
    decision_map = {}
    for prop_value in pro_value_set:
        child_data = Stream(data).filter(lambda d: d[prop] == prop_value).to_list()
        child_data_map = {
            target_value: Stream(child_data).filter(lambda o: o[TARGET] == target_value).to_list()
            for target_value in get_value_set(TARGET)
        }
        entropy_ = calc_entropy_from_map(len(child_data), child_data_map)

        if entropy_ == 0:
            print("create leaf node here", prop, prop_value)
            decision_map[prop_value] = Node(node, TARGET, child_data)
        H_x_S += (len(child_data)) / len(data) * entropy_
    """
    2.2 Tính entropy trung bình cho thuộc tính đang thực hiện.
    """
    G_x_S = H_S - H_x_S
    return G_x_S, decision_map


def create_node(props: List, data: List, parent_node: Node):
    data_map = {
        value: Stream(data).filter(lambda o: o[TARGET] == value).to_list()
        for value in get_value_set(TARGET)
    }
    biggest_gain = - float("inf")
    node = Node(parent_node, None, data)
    """ STEP 1 """
    H_S = calc_entropy_from_map(len(data), data_map)
    """ STEP 2 """
    picked_decision = {}
    for prop in props:
        gain, decision_map = calc_gain(prop, data, H_S, node)
        if gain > biggest_gain:
            biggest_gain = gain
            picked_node_name = prop
            picked_decision = decision_map

    """ STEP 3"""
    print("picked node: ", picked_node_name)
    node.name = picked_node_name
    node.children = picked_decision

    for prop_value in get_value_set(picked_node_name):
        if node.children.get(prop_value):
            continue
        next_props = [*props]
        next_props.remove(picked_node_name)
        next_node_data = Stream.of(data).filter(lambda d: d[picked_node_name] == prop_value).to_list()
        node.children[prop_value] = create_node(next_props, next_node_data, node)
    return node


if __name__ == '__main__':
    props = [DAYC, TEMP, HUM, SOIL]

    data = [
        [EDayCycle.DAY, Temperature.HOT, Humidity.HIGH, Soil.LOW, ERun.Y],
        [EDayCycle.DAY, Temperature.HOT, Humidity.HIGH, Soil.HIGH, ERun.N],
        [EDayCycle.NIGHT, Temperature.HOT, Humidity.HIGH, Soil.LOW, ERun.Y],
        [EDayCycle.NIGHT, Temperature.MID, Humidity.HIGH, Soil.LOW, ERun.Y],
        [EDayCycle.NIGHT, Temperature.COOL, Humidity.NORMAL, Soil.LOW, ERun.Y],
        [EDayCycle.NIGHT, Temperature.COOL, Humidity.NORMAL, Soil.HIGH, ERun.N],
        [EDayCycle.DAY, Temperature.COOL, Humidity.NORMAL, Soil.HIGH, ERun.N],
        [EDayCycle.DAY, Temperature.MID, Humidity.HIGH, Soil.LOW, ERun.N],
        [EDayCycle.DAY, Temperature.COOL, Humidity.NORMAL, Soil.LOW, ERun.N],
        [EDayCycle.NIGHT, Temperature.MID, Humidity.NORMAL, Soil.LOW, ERun.N],
        [EDayCycle.DAY, Temperature.MID, Humidity.NORMAL, Soil.HIGH, ERun.N],
        [EDayCycle.NIGHT, Temperature.MID, Humidity.HIGH, Soil.HIGH, ERun.N],
        [EDayCycle.NIGHT, Temperature.HOT, Humidity.NORMAL, Soil.LOW, ERun.Y],
        [EDayCycle.DAY, Temperature.MID, Humidity.HIGH, Soil.HIGH, ERun.N],
    ]
    tree = create_node(props, data, None)
    json.dump(tree.print_tree(), open("tree.json", "w"))
