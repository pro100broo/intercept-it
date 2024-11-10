import traceback


def std_formatter(message: str) -> str:
    traceback_message = traceback.format_list(traceback.extract_stack())[0].split(', in')[0].strip()
    return f"{traceback_message}: {message}"
