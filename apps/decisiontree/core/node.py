from typing import Dict


class Node:
    def __init__(self, parent: 'Node', name, is_leaf=False, decision=None, data=None):
        self.parent = parent
        self.name = name
        self.children: Dict[str, 'Node'] = {}
        self.data = data
        self.is_leaf = is_leaf
        self.decision = decision

    def __repr__(self):
        return f"{self.name}"

    def print_tree(self) -> Dict:
        return {
            "name": self.name,
            "values": {
                key: value.print_tree() if value else None
                for key, value in self.children.items()
            },
            "data": [str(d) for d in self.data] if self.data else None,
            "decision": self.decision,
            "is_leaf": self.is_leaf
        }
