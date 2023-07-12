from typing import Set, Tuple


def union_keys_for_m2m(lst1: list, lst2: list) -> Set[Tuple[any, any]]:
    list_of_task_tag = set()
    for itm1 in lst1:
        for itm2 in lst2:
            list_of_task_tag.add((itm1, itm2))
    return list_of_task_tag
