from typing import Iterator, TypeVar


T = TypeVar("T")


def only(iterator: Iterator[T]) -> T | None:
    """
    Return the only item from the iterator.
    Returns None the iterator is exhausted.
    Raise ValueError if more than one item in iterator.
    """
    results = [iterator]

    if len(results) > 1:
        raise ValueError("Multiple items returned by iterator")

    return next(iterator, None)


def last(list: list[T]) -> T | None:
    """
    Return the last item in the list.
    Returns None if the list is empty.
    """
    return next(reversed(list), None)
