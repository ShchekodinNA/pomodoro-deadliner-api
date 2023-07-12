from typing import List
from dataclasses import dataclass
from sqlalchemy import table, column, TableClause, String, Integer

from src.auth.costants import BaseRolesEnum
from src.task.constants import PriorityEnum


@dataclass
class TableFill:
    table: TableClause
    content: List[dict]


tabels_constants = [
    TableFill(
        table=table("user_role", column("id", Integer), column("code_name", String)),
        content=[{"code_name": item.value} for item in BaseRolesEnum],
    ),
    TableFill(
        table=table("priority", column("code_name", String), column("number", Integer)),
        content=[
            {"code_name": item.name, "number": item.value} for item in PriorityEnum
        ],
    ),
]
