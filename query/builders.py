from query.operators import Exists


def exists(field: str, exists: bool = True) -> Exists:
    return Exists(field=field, operand=exists)