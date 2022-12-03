from typing import Dict


class Node:
    def __init__(self, parent: 'Node', name, data):
        self.parent = parent
        self.name = name
        self.children: Dict[str, 'Node'] = {}
        self.data = data
        self.leaf = None

    def __repr__(self):
        return f"{self.name}"

    def print_tree(self) -> Dict:
        return {
            "name": self.name,
            "children": {
                key: value.print_tree() if value else None
                for key, value in self.children.items()
            },
            "data": [str(d) for d in self.data]
        }
