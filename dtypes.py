from typing import Literal, TypeAlias

Commands: TypeAlias = Literal[
    "help",
    "list",
    "post",
    "bash_completion",
    "styles",
    "styles-demo",
    "random"
    ]

Options: TypeAlias = Literal[
    "q",
    "T",
    "Q"
]

SearchOpts: TypeAlias = Literal[
    "b",
    "i",
    "r"
]


