from result import Result, Ok, Err
from typing import Any

def try_wrap(func, error_msg, *args, **kwargs) -> Result[Any, str]:
    try:
        return Ok(func(*args, **kwargs))
    except Exception as e:
        return Err(error_msg + f"\n{e}")
        
def debug(input: str):
    print(input)
    return input
