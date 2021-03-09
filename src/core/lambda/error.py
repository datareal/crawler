def handler(event: dict, context) -> None:
    error: dict = event.get('error')

    print(error)