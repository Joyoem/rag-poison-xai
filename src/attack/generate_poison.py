from typing import Literal


PoisonMode = Literal["naive", "targeted"]


def generate_poison_set(mode: PoisonMode = "naive") -> str:
    return f"{mode} poison generation placeholder"
