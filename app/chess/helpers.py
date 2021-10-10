from typing import Iterator, TypeVar


T = TypeVar('T')


def only(iterator: Iterator[T], error_message: str = "") -> T | None:
    """
    Return the only item from the iterator. 
    Returns None the iterator is exhausted. 
    Raise RuntimeError with optional error message if more than item in iterator.
    """
    results = [iterator]

    if len(results) > 1:
        raise RuntimeError(error_message)

    return next(iterator, None)


def last(list: list[T]) -> T | None:
    """
    Return the last item in the list.
    Returns None if the list is empty. 
    """
    return next(reversed(list), None)

# TODO - can we get rid of this and use a library?
def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [val for sublist in list_of_lists for val in sublist]
