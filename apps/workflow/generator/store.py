import os
import re
from os import path
from typing import Iterable, List, Tuple

from project.utils import functions
from state_spec import StateSpec
from transition_spec import TransitionSpec


class Store:
    def __init__(self, base_dir="./", const_dir="/", state_dir="/"):
        self.dir = base_dir
        self.const_dir = const_dir
        self.state_dir = state_dir
        dirs = [("dir", base_dir), ("const_dir", const_dir), ("state_dir", state_dir)]
        for param, dir in dirs:
            if not dir.endswith("/"):
                dir += "/"
            if not path.exists(dir):
                os.mkdir(dir)
            setattr(self, param, dir)

    def __write_state_class_init(self, init_items: List[Tuple[str, str]]):
        with functions.op(f"{self.state_dir}__init__.py", "w") as f:
            all = ",".join([f'"{class_name}"' for module, class_name in sorted(set(init_items), key=lambda x: x[1])])
            import_str = "\n".join([f"from .{module} import {class_name}" for module, class_name in sorted(set(init_items), key=lambda x: x[1])])
            f.write(f"__all__ = [{all}]\n{import_str}")

    def state_dir_handler(self, state_id) -> Tuple:
        parts = state_id.split("_")
        limit = 0
        counter = 0
        current_dir = self.state_dir
        while len(parts) > 1 and counter < limit:
            current_dir += parts[counter]
            if counter + 1 < len(parts) and parts[counter + 1].isnumeric():
                current_dir += f"_{parts[counter + 1]}"
                counter += 1
            current_dir += "/"
            if not path.exists(f"{current_dir}"):
                os.mkdir(f"{current_dir}")
            counter += 1
        file_name = "_".join(parts[counter:])
        module = re.sub(r"/+", ".", current_dir.replace(self.state_dir, "")) + file_name
        class_name = functions.to_pascal_case(state_id)
        return (module, class_name, current_dir, file_name)

    def save_class(self, states: Iterable[StateSpec]):
        init_items = []
        for state in states:
            module, class_name, current_dir, file_name = self.state_dir_handler(state.id)
            file_path = f"{current_dir}/{file_name}"
            init_items.append((module, class_name,))
            with open(f"{file_path}.py", "w", encoding="utf8") as f:
                f.write(
                    "\n".join([
                        "from typing import Dict",
                        "from loguru import logger",
                        "from starlette import status",
                        "from apps.workflow.constants.action import EAction",
                        "from apps.workflow.constants.state import EState",
                        "from apps.workflow.constants.transition import ETransition",
                        "from apps.workflow.roles import ERole",
                        "from apps.workflow.states.base import State, PermissionSchema, NextStateRequest",
                        "from project.core import error_code, HTTPException",
                    ])
                    # + "\n\n".join(sorted(set(map(lambda s: s.to_state(), states))))
                    + state.to_state()
                )
        self.__write_state_class_init(init_items)

    def save_transition_enum(self, transitions: Iterable[TransitionSpec]):
        with open(f"{self.const_dir}/transition.py", "w", encoding="utf8") as f:
            f.write(
                "from enum import auto\n"
                + "from fastapi_utils.enums import StrEnum\n"
                + "class ETransition(StrEnum):\n"
                + "\n".join(sorted(set(map(lambda t: f"\t{t.id} = auto()\n\t", transitions))))
            )

    def save_state_enum(self, states: Iterable[StateSpec]):
        with open(f"{self.const_dir}/state.py", "w", encoding="utf8") as f:
            f.write(
                "from enum import auto\n"
                + "from fastapi_utils.enums import StrEnum\n"
                + "class EState(StrEnum):\n"
                + "\n".join(sorted(set(map(lambda s: f"\t{s.id} = auto()\n\t\"{s.name}\"", states))))
            )

    def save_action_enum(self, transitions: Iterable[TransitionSpec]):
        actions = set(map(lambda t: t.action, transitions))
        with functions.op(f"{self.const_dir}action.py", "w") as f:
            f.write(
                "from enum import auto\n"
                + "from fastapi_utils.enums import StrEnum\n"
                + "class EAction(StrEnum):\n"
                + "\n".join(sorted(set(map(lambda a: f"\t{a} = auto()\n", actions))))
            )

    # def save_path_enum(self, transitions: Iterable[TransitionSpec]):
    #     paths = set(map(lambda t: f"{t.action}_path", transitions))
    #     with functions.op(f"{self.const_dir}path.py", "w") as f:
    #         f.write(
    #             "from fastapi_utils.enums import StrEnum\n"
    #             + "class EPath(StrEnum):\n"
    #             + "\n".join(sorted(set(map(lambda a: f"\t{a} = None ", paths))))
    #         )

    # def save_nodes(self, states: List[StateSpec]):
    #     with functions.op(f"{self.dir}nodes.json", "w") as f:
    #         f.write(
    #             """[ """
    #             + ",".join(sorted(set(map(lambda s: s.to_node(), states))))
    #             + "]"
    #         )
    #
    # def save_node_links(self, transitions: Iterable[TransitionSpec]):
    #     with functions.op(f"{self.dir}node_links.json", "w") as f:
    #         f.write(
    #             """[ """
    #             + ",".join(sorted(set(map(lambda t: t.to_node_link(), transitions))))
    #             + "]"
    #         )
