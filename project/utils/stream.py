import itertools
from builtins import StopIteration
from typing import (
    Callable, Generic, Iterable, List, Optional, Set, Tuple, TypeVar
)

T = TypeVar("T")
X = TypeVar("X")


class Stream(Generic[T]):
    def __init__(self, items: Iterable[T]):
        self.items: Iterable[T] = items

    @classmethod
    def of(self, items: Iterable[T]) -> 'Stream[T]':
        return Stream[T](items)

    def map(self, func: Callable[[T], X]) -> 'Stream[X]':
        self.items = map(func, self.items)
        return self

    def filter(self, func: Callable[[T], bool]) -> 'Stream[T]':
        self.items = filter(func, self.items)
        return self

    async def amap(self, func: Callable[[T], Iterable[X]]) -> 'Stream[X]':
        self.items = [await func(item) for item in self.items]
        return self

    async def afilter(self, func: Callable[[T], bool]) -> 'Stream[T]':
        self.items = [item for item in self.items if await func(item)]
        return self

    async def afilter_map(self, filter_func: Callable[[T], Iterable[T]], map_func: Callable[[T], Iterable[X]]) -> 'Stream[X]':
        self.items = [await map_func(item) for item in self.items if await filter_func(item)]
        return self

    def to_list(self) -> List[T]:
        return list(self.items)

    def to_set(self) -> Set[T]:
        return set(self.items)

    def to_tuple(self) -> Tuple[T]:
        return tuple(self.items)

    def one(self) -> T:
        if self.items:
            return self.items.__iter__().__next__()
        else:
            raise IndexError

    def one_or_none(self) -> Optional[T]:
        iterator = self.items.__iter__()
        try:
            return iterator.__next__()
        except StopIteration:
            return None

    def any(self, func: Callable) -> bool:
        return any(func(item) for item in self.items)

    def all(self, func: Callable) -> bool:
        return all(func(item) for item in self.items)

    def flat_map(self, func: Callable[[Iterable[T]], Iterable[X]]) -> 'Stream[X]':
        self.items = list(itertools.chain(*(func(item) for item in self.items)))
        return self

    def enumerate(self) -> 'Stream[Tuple[int, T]]':
        self.items = enumerate(self.items)
        return self
