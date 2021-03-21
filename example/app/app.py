from snappy import set_handler


@set_handler
def hello_world(name: str) -> str:
    return f"Hello {name}"
