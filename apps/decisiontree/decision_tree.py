import json
import math
from typing import List, Dict, Any

from apps.decisiontree.decision_data import DecisionData
from apps.decisiontree.node import Node
from apps.enums.enums import Temperature, Humidity, Soil, ERun, EDayCycle
from project.utils.stream import Stream


class DecisionTree:
    def __init__(self):
        self.unchecked_properties = []

    def calc_entropy(self, p: float, i_list: List[float]) -> float:
        sum = 0
        for i in i_list:
            if i == 0:
                continue
            sum += (-i / p) * math.log2(i / p)
        return sum

    def calc_entropy_from_map(self, p: float, i_map: Dict[Any, Any]) -> float:
        return self.calc_entropy(p, Stream.of(i_map.values()).map(len).to_list())

    def avg_entropy_info(self):
        ...

    def gain(self, parent_prop: str, parent_value_set: List, child_prop: str, child_value_set: List, data: List[DecisionData]) -> float:
        """
        Để xác định các nút trong mô hình cây quyết định, ta thực hiện tính Infomation Gain tại mỗi nút theo trình tự sau:
        •Bước 1: Tính toán hệ số Entropy của biến mục tiêu S có N phần tử với Nc phần tử thuộc lớp c cho trước:
        H(S)=  – ∑c=1 (Nc/N) log(Nc/N)
        •Bước 2: Tính hàm số Entropy tại mỗi thuộc tính: với thuộc tính x, các điểm dữ liệu trong S được chia ra K child node S1, S2, …, SK với số điểm trong mỗi child node lần lượt là m1, m2 ,…, mK , ta có:
        H(x, S) = ∑Kk=1 (mk / N) * H(Sk )
        Bước 3: Chỉ số Gain Information được tính bằng:
        G(x, S) = H(S) – H(x,S)
        """
        """Step 1"""

        parent_data_map = {
            value: Stream(data).filter(lambda d: getattr(d, parent_prop) == value).to_list()
            for value in parent_value_set
        }
        H_S = self.calc_entropy_from_map(len(data), parent_data_map)

        """Step 2"""
        H_x_S = 0
        for child_value in child_value_set:
            child_data = Stream(data).filter(lambda d: getattr(d, child_prop) == child_value).to_list()
            child_data_map = {
                parent_value: Stream(child_data).filter(lambda d: getattr(d, parent_prop) == parent_value).to_list()
                for parent_value in parent_value_set
            }
            H_x_S += (len(child_data)) / len(data) * self.calc_entropy_from_map(len(child_data), child_data_map)

        """Step 3"""
        G_x_S = H_S - H_x_S

        print(f"""{"-" * 50}
{child_prop}
{"H_S":^12}|{"H_xS":^12}|{"G_xS":^12}
{H_S:^12.2f}|{H_x_S:^12.2f}|{G_x_S:^12.2f}""")
        return G_x_S

    def get_value_set(self, prop: str):
        for key, type_ in DecisionData.__annotations__.items():
            if key == prop:
                return [e.value for e in type_]
        raise ValueError("cannot get value set")

    def create_node(self, parent_prop, parent_value_set, data, parent_node:Node, target):
        biggest_gain = -float("inf")

        if not self.unchecked_properties:
            return None

        for key in self.unchecked_properties:
            parent_value_set = self.get_value_set(target)
            child_prop = key
            child_value_set = self.get_value_set(key)
            gain = self.gain(parent_prop, parent_value_set, child_prop, child_value_set, data)
            if gain ==0:
                node = Node(parent_node, next_node_name, data)
            if gain > biggest_gain:
                biggest_gain = gain
                next_node_name = child_prop
                next_node_value_set = child_value_set

        self.unchecked_properties.remove(next_node_name)
        node = Node(parent_node, next_node_name, data)
        print(f"done create node, pick node: {node}")
        for child_value in next_node_value_set:
            node.children[child_value] = self.create_node(
                next_node_name, next_node_value_set, Stream.of(data).filter(lambda d: getattr(d, next_node_name) == child_value).to_list(), node, target
            )


        return node

    def init_tree(self, target: str, data: List[DecisionData]):
        # init
        parent_prop = target
        self.unchecked_properties = list(DecisionData.__annotations__.keys())
        self.unchecked_properties.remove(target)
        parent_node = None
        # generate tree
        return self.create_node(parent_prop, self.get_value_set(parent_prop), data, parent_node, target)


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

    target = "run"

    parent_prop = "run"
    parent_value_set = [e.value for e in ERun]
    child_prop = "dayc"
    child_value_set = [e.value for e in EDayCycle]

    # print(DecisionTree().gain(parent_prop, parent_value_set, child_prop, child_value_set, data))
    root = DecisionTree().init_tree("run", data)
    d = root.print_tree()
    print(json.dump(d, open("tree.json", "w")))
