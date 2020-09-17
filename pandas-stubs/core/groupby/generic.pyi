from typing import overload, Union, List, Dict, Iterator
from typing_extensions import Literal
import numpy as _np

from pandas.core.frame import DataFrame
from pandas.core.series import Series
from ..frame import _FunctionLike

_str = str  # needed because Series has a property called "str"...

class GroupBy: ...

class SeriesGroupBy(GroupBy):
    def __getitem__(self, item: _str) -> Series: ...
    def count(self) -> Series: ...
    def head(self, n: int = ...) -> Series: ...
    def max(self) -> Series: ...
    def mean(self) -> Series: ...
    def median(self) -> Series: ...
    def min(self) -> Series: ...
    def nunique(self, dropna: bool = ...) -> Series: ...
    def quantile(self, q: float = ..., interpolation: str = ...) -> Series: ...
    def rank(
        self,
        method: Literal["average", "min", "max", "first", "dense"] = ...,
        ascending: bool = ...,
        na_option: Literal["keep", "top", "bottom"] = ...,
        pct: bool = ...,
    ) -> Series: ...
    def std(self, ddof: int = ...) -> Series: ...
    def sum(self) -> Series: ...
    def tail(self, n: int = ...) -> Series: ...
    def unique(self) -> Series[_np.ndarray]: ...
    def var(self, ddof: int = ...) -> Series: ...

class DataFrameGroupBy(GroupBy):
    @overload
    def __getitem__(self, item: _str) -> SeriesGroupBy: ...
    @overload
    def __getitem__(self, item: List[_str]) -> "DataFrameGroupBy": ...
    def __getattr__(self, name: _str) -> SeriesGroupBy: ...
    def __iter__(self) -> Iterator: ...
    def aggregate(
        self, func: Union[_FunctionLike, List[_FunctionLike], Dict[_str, _FunctionLike]]
    ) -> DataFrame: ...
    agg = aggregate
    def count(self) -> DataFrame: ...
    def head(self, n: int = ...) -> DataFrame: ...
    def max(self) -> DataFrame: ...
    def mean(self) -> DataFrame: ...
    def median(self) -> DataFrame: ...
    def min(self) -> DataFrame: ...
    def nunique(self, dropna: bool = ...) -> DataFrame: ...
    def quantile(self, q: float = ..., interpolation: str = ...) -> DataFrame: ...
    def rank(
        self, method: str, ascending: bool, na_option: str, pct: bool, axis: int
    ) -> DataFrame: ...
    def std(self, ddof: int = ...) -> DataFrame: ...
    def sum(self) -> DataFrame: ...
    def tail(self, n: int = ...) -> DataFrame: ...
    def var(self, ddof: int = ...) -> DataFrame: ...
