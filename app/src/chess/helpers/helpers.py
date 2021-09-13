from typing import Iterator, TypeVar, Union


T = TypeVar('T')


# TODO - move these into helper file
def only(iterator: Iterator[T], error_message: str = "") -> Union[T, None]:
    results = [iterator]

    if len(results) > 1:
        raise RuntimeError(error_message)

    return next(iterator, None)


def last(list: list[T]) -> Union[T, None]:
    return next(reversed(list), None)
