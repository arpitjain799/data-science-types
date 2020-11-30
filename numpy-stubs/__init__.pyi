"""Public API of numpy"""
import os
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    IO,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
    Iterable,
)
from typing_extensions import Protocol, Literal
from pathlib import Path
import builtins

from . import testing, random, ma, linalg

from pandas import Series

_T = TypeVar("_T")

_Scalar = TypeVar("_Scalar", bound=void)

# void is the base class of all the types that an ndarray can have
class void:
    @property
    def dtype(self: _DTypeObj) -> _dtype[_DTypeObj]: ...
    def astype(self, dtype: Type[_DType]) -> _DType: ...
    def copy(self: _Scalar) -> _Scalar: ...

# a smaller-bit integer can act like a bigger integer in the sense that if you add an int16 and an
# int64, then numpy will upgrade the int16 to an int64 and add them
# and this is why we let int32 be a subclass of int64; and similarly for float32 and float64
# the same logic applies when adding unsigned and signed values (uint + int -> int)

# this would be the correct definition, but it makes `int` conflict with `float`
# class float64(void, float): ...
class float64(void, int):
    def __float__(self) -> float: ...

class float32(float64): ...
class float16(float32): ...

floating = float64
number = float64

class int64(float64): ...
class int32(int64, float64): ...
class int16(int32, float32): ...
class int8(int16, float16): ...
class uint64(int64): ...
class uint32(uint64, int32): ...
class uint16(uint32, int16): ...
class uint8(uint16, int8): ...
class bool_(int8): ...
class str_(void, str): ...
class object_(void): ...

integer = int64

_DType = TypeVar(
    "_DType",
    bool_,
    float16,
    float32,
    float64,
    int8,
    int16,
    int32,
    int64,
    str_,
    uint8,
    uint16,
    uint32,
    uint64,
    covariant=True,
)
_DType2 = TypeVar(
    "_DType2",
    bool_,
    float16,
    float32,
    float64,
    int8,
    int16,
    int32,
    int64,
    str_,
    uint8,
    uint16,
    uint32,
    uint64,
    covariant=True,
)
_DTypeObj = TypeVar("_DTypeObj", bound=Union[void, int, float])
_ShapeType = Union[int, Tuple[int, ...], List[int]]
_AxesType = Union[int, Tuple[int, ...], List[int]]
_InterpolationType = Literal["linear", "lower", "higher", "midpoint", "nearest"]
_OrderType = Union[str, Sequence[str]]
_ScalarLike = Union[_DType, str, int, float]
_ConditionType = Union[ndarray[bool_], bool_, bool]
newaxis: None = ...

_AnyNum = Union[int, float, bool]
# generic types that are only allowed to take on dtype values

_Float = TypeVar("_Float", float16, float32, float64)
_FloatLike = TypeVar("_FloatLike", bound=Union[float64, float])
_Int = TypeVar("_Int", bool_, int8, int16, int32, int64, uint8, uint16, uint32, uint64)
_IntLike = TypeVar("_IntLike", bound=Union[int64, int])
_BoolLike = TypeVar("_BoolLike", bound=Union[bool_, bool])

_NestedList = Union[List[_T], List[List[_T]], List[List[List[_T]]], List[List[List[List[_T]]]]]

class dtype(Generic[_DTypeObj]):
    @overload
    def __init__(self: dtype[_DTypeObj], obj: Type[_DTypeObj]) -> None: ...
    @overload
    def __init__(self, obj: str) -> None: ...
    @property
    def type(self) -> Type[_DTypeObj]: ...

_dtype = dtype

class ndarray(Generic[_DType]):
    """
    The main object in the numpy library.
    """

    #
    # Array-like structures attributes
    #
    dtype: _dtype[_DType]
    size: int
    ndim: int
    shape: Tuple[int, ...]

    #
    # Array-like methods
    #
    def __init__(
        self,
        shape: Tuple[int, ...],
        dtype: Optional[Type[_DType]] = ...,
        buffer: Optional[Any] = ...,
        offset: Optional[int] = ...,
        strides: Optional[Tuple[int, ...]] = ...,
        order: Optional[str] = ...,
    ) -> None: ...
    def all(self, axis: Optional[_AxesType] = ..., keepdims: bool = ...) -> ndarray[_DType]: ...
    def any(self, axis: Optional[_AxesType] = ..., keepdims: bool = ...) -> ndarray[_DType]: ...
    def argmax(self, axis: Optional[int] = ...) -> ndarray[_DType]: ...
    def argmin(self, axis: Optional[int] = ...) -> ndarray[_DType]: ...
    # def argpartition(self, kth: Union[int, Sequence[int]], axis: Optional[int]=-1,
    #                  kind: str='introselect', order: _OrderType=None) -> ndarray[_DType]: ...
    def argsort(
        self, axis: Optional[int] = ..., kind: str = ..., order: Optional[_OrderType] = ...
    ) -> ndarray[_DType]: ...
    # _DType has to be split up like this for some reason; I don't fully understand it
    @overload
    def astype(self, dtype: Type[_Int], copy: bool = ...) -> ndarray[_Int]: ...
    @overload
    def astype(self, dtype: Type[_Float], copy: bool = ...) -> ndarray[_Float]: ...
    @overload
    def astype(self, dtype: Type[str_], copy: bool = ...) -> ndarray[str_]: ...
    # the bool overload has to come before the int overload because bool is a subclass of int
    @overload
    def astype(self, dtype: Type[bool], copy: bool = ...) -> ndarray[bool_]: ...
    @overload
    def astype(self, dtype: Type[int], copy: bool = ...) -> ndarray[int64]: ...
    @overload
    def astype(self, dtype: Type[float], copy: bool = ...) -> ndarray[float64]: ...
    @overload
    def astype(self, dtype: Type[str], copy: bool = ...) -> ndarray[str_]: ...
    def byteswap(self, inplace: bool = ...) -> ndarray[_DType]: ...
    def choose(self, choices: Sequence[ndarray[_DType]], mode: str = ...) -> ndarray[_DType]: ...
    def clip(self, a_min: _AnyNum, a_max: _AnyNum) -> ndarray[_DType]: ...
    def compress(self, condition: Sequence[bool], axis: Optional[int] = ...) -> ndarray[_DType]: ...
    def conj(self) -> ndarray[_DType]: ...
    def conjugate(self) -> ndarray[_DType]: ...
    def copy(self, order: str = ...) -> ndarray[_DType]: ...
    def cumprod(self, axis: Optional[int] = ..., dtype: Optional[Any] = ...) -> ndarray[_DType]: ...
    def cumsum(
        self, axis: Optional[int] = ..., dtype: Optional[Type[_DType]] = ...
    ) -> ndarray[_DType]: ...
    def diagonal(
        self, offset: int = ..., axis1: int = ..., axis2: int = ...
    ) -> ndarray[_DType]: ...
    def dot(self, b: ndarray[_DType]) -> ndarray[_DType]: ...
    def dump(self, file: str) -> None: ...
    def dumps(self) -> str: ...
    # def fill(self, value: _S) -> None: ...
    def flatten(self, order: str = ...) -> ndarray[_DType]: ...
    def getfield(self, dtype: Type[_DType], offset: int = ...) -> ndarray[_DType]: ...
    def item(self) -> _DType: ...
    def itemset(self, arg0: Union[int, Tuple[int, ...]], arg1: Optional[Any] = ...) -> None: ...
    def max(self) -> _DType: ...
    @overload
    def mean(self: ndarray[float32]) -> float32: ...
    @overload
    def mean(self: ndarray[float32], axis: _AxesType) -> ndarray[float32]: ...
    @overload
    def mean(self) -> float64: ...
    @overload
    def mean(self, axis: _AxesType) -> ndarray[float64]: ...
    def min(self) -> _DType: ...
    def newbyteorder(self, new_order: str = ...) -> ndarray[_DType]: ...
    def nonzero(self) -> Tuple[ndarray[int64], ...]: ...
    def partition(
        self, kth: _AxesType, axis: int = ..., kind: str = ..., order: Optional[_OrderType] = ...
    ) -> None: ...
    def prod(
        self,
        axis: Optional[_AxesType] = ...,
        dtype: Optional[Type[_DType]] = ...,
        keepdims: bool = ...,
    ) -> ndarray[_DType]: ...
    def ptp(self, axis: Optional[int] = ...) -> ndarray[_DType]: ...
    def put(self, ind: ndarray[_DType], v: ndarray[_DType], mode: str = ...) -> None: ...
    def ravel(self, order: str = ...) -> ndarray[_DType]: ...
    def repeat(
        self, repeats: Union[int, Sequence[int]], axis: Optional[int] = ...
    ) -> ndarray[_DType]: ...
    @overload
    def reshape(self, *newshape: int) -> ndarray[_DType]: ...
    @overload
    def reshape(
        self, newshape: Union[Tuple[int, ...], List[int]], order: str = ...
    ) -> ndarray[_DType]: ...
    def resize(self, new_shape: _ShapeType, refcheck: bool = ...) -> None: ...
    def round(self, decimals: int = ...) -> ndarray[_DType]: ...
    # def searchsorted(self, v: Union[_S, ndarray[_DType]], side: str='left',
    #                  sorter: ndarray[_DType]=None) -> ndarray[_DType]: ...
    def setfield(self, val: Any, dtype: Type[_DType], offset: int = ...) -> None: ...
    def setflags(
        self, write: Optional[bool] = ..., align: Optional[bool] = ..., uic: Optional[bool] = ...
    ) -> None: ...
    def sort(self, axis: int = ..., kind: str = ..., order: Optional[_OrderType] = ...) -> None: ...
    def squeeze(self, axis: Optional[_AxesType] = ...) -> ndarray[_DType]: ...
    @overload
    def std(self: ndarray[float32]) -> float32: ...
    @overload
    def std(self) -> float64: ...
    @overload
    def std(
        self,
        axis: _AxesType,
        dtype: Optional[Type[_DType]] = ...,
        ddof: int = ...,
        keepdims: bool = ...,
    ) -> ndarray[_DType]: ...
    @overload
    def sum(self) -> _DType: ...
    @overload
    def sum(self, axis: Optional[_AxesType], keepdims: bool = ...) -> ndarray[_DType]: ...
    def swapaxes(self, axis1: int, axis2: int) -> ndarray[_DType]: ...
    def take(
        self, indices: Sequence[int], axis: Optional[int] = ..., mode: str = ...
    ) -> ndarray[_DType]: ...
    def tobytes(self, order: str = ...) -> bytes: ...
    def tofile(
        self,
        fid: object,
        sep: str = ...,  # TODO fix fid definition (There's a bug in mypy io's namespace https://github.com/python/mypy/issues/1462)
        format: str = ...,
    ) -> None: ...
    # for some reason, you can not use _Float to narrow down the type of ndarray here:
    @overload
    def tolist(
        self: Union[ndarray[bool_], ndarray[int8], ndarray[int16], ndarray[int32], ndarray[int64]]
    ) -> Sequence[int]: ...
    @overload
    def tolist(self: Union[ndarray[float32], ndarray[float64]]) -> Sequence[float]: ...
    @overload
    def tolist(self: ndarray[str_]) -> Sequence[str]: ...
    def tostring(self, order: str = ...) -> bytes: ...
    def trace(
        self,
        offset: int = ...,
        axis1: int = ...,
        axis2: int = ...,
        dtype: Optional[Type[_DType]] = ...,
    ) -> ndarray[_DType]: ...
    def transpose(self, axes: Optional[_AxesType] = ...) -> ndarray[_DType]: ...
    def var(
        self,
        axis: Optional[_AxesType] = ...,
        dtype: Optional[Type[_DType]] = ...,
        ddof: int = ...,
        keepdims: bool = ...,
    ) -> ndarray[_DType]: ...
    def view(
        self,
        dtype: Optional[Union[Type[_DType], Type[ndarray[_DType]]]] = ...,
        type: Optional[type] = ...,
    ) -> ndarray[_DType]: ...
    #
    # Magic methods
    #
    def __abs__(self) -> ndarray[_DType]: ...
    @overload
    def __add__(self, value: ndarray[_DType]) -> ndarray[_DType]: ...
    @overload
    def __add__(self, value: _DType) -> ndarray[_DType]: ...
    @overload
    def __add__(self, value: float) -> ndarray[float64]: ...
    def __and__(self, value: object) -> ndarray[_DType]: ...
    @overload
    def __array__(self) -> ndarray[_DType]: ...
    @overload
    def __array__(self, dtype: Type[_DType2]) -> ndarray[_DType2]: ...
    def __array_prepare__(self, context: Optional[object] = ...) -> ndarray[_DType]: ...
    def __array_wrap__(self, context: Optional[object] = ...) -> ndarray[_DType]: ...
    def __bool__(self) -> bool: ...
    def __complex__(self) -> complex: ...
    def __contains__(self, key: object) -> bool: ...
    def __copy__(self) -> ndarray[_DType]: ...
    def __deepcopy__(self) -> ndarray[_DType]: ...
    def __delattr__(self, name: str) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __dir__(self) -> List[str]: ...
    def __divmod__(self, value: object) -> Tuple[ndarray[_DType], ndarray[_DType]]: ...
    def __eq__(self, value: object) -> ndarray[bool_]: ...  # type: ignore
    def __float__(self) -> float: ...
    def __floordiv__(self, value: object) -> ndarray[_DType]: ...
    def __ge__(self, value: object) -> ndarray[bool_]: ...
    def __getattribute__(self, name: str) -> Any: ...
    @overload
    def __getitem__(self, key: Union[int, Tuple[int, ...]]) -> _DType: ...
    @overload
    def __getitem__(
        self,
        key: Union[
            None,
            slice,
            str,
            ndarray[_Int],
            List[int],
            Tuple[int, Union[slice, ellipsis, None]],
            Tuple[Union[slice, ellipsis, None], int],
            Tuple[Union[slice, ellipsis, None], Union[slice, ellipsis, None], int],
            Tuple[Union[ndarray[_Int], slice, ellipsis, None], ...],
        ],
    ) -> ndarray[_DType]: ...
    def __gt__(self, value: object) -> ndarray[bool_]: ...
    @overload
    def __iadd__(self, value: ndarray[_DType]) -> ndarray[_DType]: ...
    @overload
    def __iadd__(self, value: _DType) -> ndarray[_DType]: ...
    @overload
    def __iadd__(self, value: float) -> ndarray[float64]: ...
    def __iand__(self, value: object) -> ndarray[bool_]: ...
    def __ifloordiv__(self, value: object) -> None: ...
    def __ilshift__(self, value: object) -> None: ...
    def __imatmul__(self, value: ndarray[_DType]) -> None: ...
    def __imod__(self, value: object) -> None: ...
    def __imul__(self, value: object) -> None: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> ndarray[_DType]: ...
    def __ior__(self, value: object) -> None: ...
    def __ipow__(self, value: object) -> None: ...
    def __irshift__(self, value: object) -> None: ...
    def __isub__(self, value: object) -> None: ...
    def __iter__(self) -> Iterator[_DType]: ...
    def __itruediv__(self, value: object) -> ndarray[float64]: ...
    def __ixor__(self, value: object) -> None: ...
    def __le__(self, value: object) -> ndarray[_DType]: ...
    def __len__(self) -> int: ...
    def __lshift__(self, value: object) -> ndarray[_DType]: ...
    def __lt__(self, value: object) -> ndarray[_DType]: ...
    def __matmul__(self, value: ndarray[_DType]) -> ndarray[_DType]: ...
    def __mod__(self, value: object) -> ndarray[_DType]: ...
    def __mul__(self, value: object) -> ndarray[_DType]: ...
    def __ne__(self, value: object) -> ndarray[_DType]: ...  # type: ignore
    def __neg__(self) -> ndarray[_DType]: ...
    def __or__(self, value: object) -> ndarray[_DType]: ...
    def __pos__(self) -> ndarray[_DType]: ...
    def __pow__(self, value: object) -> ndarray[_DType]: ...
    @overload
    def __radd__(self, value: ndarray[_DType]) -> ndarray[_DType]: ...
    @overload
    def __radd__(self, value: _DType) -> ndarray[_DType]: ...
    def __rand__(self, value: object) -> ndarray[_DType]: ...
    def __rdivmod__(self, value: object) -> Tuple[ndarray[_DType], ndarray[_DType]]: ...
    def __rfloordiv__(self, value: object) -> ndarray[_DType]: ...
    def __rlshift__(self, value: object) -> ndarray[_DType]: ...
    def __rmatmul__(self, value: object) -> ndarray[_DType]: ...
    def __rmod__(self, value: object) -> ndarray[_DType]: ...
    def __rmul__(self, value: object) -> ndarray[_DType]: ...
    def __ror__(self, value: object) -> ndarray[_DType]: ...
    def __rpow__(self, value: object) -> ndarray[_DType]: ...
    def __rrshift__(self, value: object) -> ndarray[_DType]: ...
    def __rshift__(self, value: object) -> ndarray[_DType]: ...
    def __rsub__(self, value: object) -> ndarray[_DType]: ...
    @overload
    def __rtruediv__(
        self: ndarray[float32], value: Union[ndarray[float32], float32, float]
    ) -> ndarray[float32]: ...
    @overload
    def __rtruediv__(self, value: object) -> ndarray[float64]: ...
    def __rxor__(self, value: object) -> ndarray[_DType]: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __setitem__(self, key: Any, value: Any) -> None: ...
    def __str__(self) -> str: ...
    def __sub__(self, value: object) -> ndarray[_DType]: ...
    @overload
    def __truediv__(
        self: ndarray[float32], value: Union[ndarray[float32], float32, float]
    ) -> ndarray[float32]: ...
    @overload
    def __truediv__(self, value: object) -> ndarray[float64]: ...
    def __xor__(self, value: object) -> ndarray[_DType]: ...

class Array(Protocol[_DType]):
    def __array__(self) -> Union[ndarray[_DType], Sequence[Sequence[_DType]]]: ...

_ArrayLike = Union[Array[_DType], Sequence[_DType]]
_Coercable = Union[_ArrayLike, _DTypeObj]

######
# numpy's scalar hierarchy (http://docs.scipy.org/doc/numpy/reference/arrays.scalars.html#scalars)
######
# class bool_: ...
# class number: ...
# class integer(number, int): ...
# class signedinteger(integer): ...
# class byte(signedinteger): ...
# class short(signedinteger): ...
# class intc(signedinteger): ...
# class int_(signedinteger): ...
# class longlong(signedinteger): ...
# class int8(signedinteger): ...
# class int16(signedinteger): ...
# class int32(signedinteger): ...
# class int64(signedinteger): ...
# class unsignedinteger(integer): ...
# class ubyte(unsignedinteger): ...
# class ushort(unsignedinteger): ...
# class uintc(unsignedinteger): ...
# class uint(unsignedinteger): ...
# class ulonglong(unsignedinteger): ...
# class uint8(signedinteger): ...
# class uint16(signedinteger): ...
# class uint32(signedinteger): ...
# class uint64(signedinteger): ...
# class inexact(number[float]): ...
# class floating(inexact): ...
# class half(floating): ...
# class single(floating): ...
# class float_(floating): ...
# class longfloat_(floating): ...
# class float16(floating): ...
# class float64(floating): ...
# class float128(floating): ...
# class complexfloating(inexact): ...
# class csingle(complexfloating): ...
# class complex_(complexfloating): ...
# class clongfloat(complexfloating): ...
# class complex64(complexfloating): ...
# class complex128(complexfloating): ...
# class complex256(complexfloating): ...
# class flexible(generic[_Scalar], Generic[_Scalar]): ...
# class character(flexible[str]): ...
# class str_(character): ...
# class unicode_(character): ...
# class void(flexible[None]): ...

#
# Array creation routines
#
# np.array: first check if the dtype has been set explicitly
@overload
def array(
    object: Union[_NestedList[Any], Iterable[ndarray], ndarray], dtype: Type[_DType]
) -> ndarray[_DType]: ...
@overload
def array(
    object: Union[_NestedList[Any], Iterable[ndarray], ndarray], dtype: Type[int]
) -> ndarray[int64]: ...
@overload
def array(
    object: Union[_NestedList[Any], Iterable[ndarray], ndarray], dtype: Type[float]
) -> ndarray[float64]: ...

# np.array: then check if it is a list of some type. check the most specific first
@overload
def array(object: _NestedList[bool]) -> ndarray[bool_]: ...
@overload
def array(object: _NestedList[_Int]) -> ndarray[_Int]: ...
@overload
def array(object: _NestedList[_Float]) -> ndarray[_Float]: ...
@overload
def array(object: _NestedList[int]) -> ndarray[int64]: ...
@overload
def array(object: _NestedList[float]) -> ndarray[float64]: ...
@overload
def array(object: _NestedList[str]) -> ndarray[str_]: ...
@overload
def array(object: str) -> ndarray[str_]: ...
@overload
def array(object: Union[ndarray[_DType], _NestedList[ndarray[_DType]]]) -> ndarray[_DType]: ...
@overload
def array(object: Tuple) -> ndarray[bool_]: ...
@overload
def arange(start: float, stop: float = ..., step: float = ...) -> ndarray[float64]: ...
@overload
def arange(start: int, stop: int = ..., step: int = ...) -> ndarray[int64]: ...
@overload
def arange(range_: int, dtype: Type[_DType]) -> ndarray[_DType]: ...
@overload
def arange(range_: float) -> ndarray[float64]: ...
def ascontiguousarray(a: Any, dtype: Optional[Type[_DType]] = ...) -> ndarray: ...
def copy(a: Any, order: Optional[str] = ...) -> ndarray: ...
def cumsum(
    a: ndarray[_DType], axis: Optional[int] = ..., dtype: Optional[Type[_DType]] = ...
) -> ndarray[_DType]: ...
def delete(
    arr: ndarray[_DType], object: Union[int, List[int], slice], axis: Optional[int] = ...
) -> ndarray[_DType]: ...
@overload
def empty(shape: _ShapeType, dtype: Type[_Int]) -> ndarray[_Int]: ...
@overload
def empty(shape: _ShapeType, dtype: Type[_Float]) -> ndarray[_Float]: ...
@overload
def empty(shape: _ShapeType, dtype: Type[str_]) -> ndarray[str_]: ...
@overload
def empty(shape: _ShapeType, dtype: Type[bool]) -> ndarray[bool_]: ...
@overload
def empty(shape: _ShapeType, dtype: Type[int]) -> ndarray[int64]: ...
@overload
def empty(shape: _ShapeType, dtype: Type[float] = ...) -> ndarray[float64]: ...
@overload
def empty(shape: _ShapeType, dtype: Type[str]) -> ndarray[str_]: ...
def empty_like(
    a: Any, dtype: Optional[Any] = ..., order: str = ..., subok: bool = ...
) -> ndarray: ...
def eye(N: int, M: Optional[int] = ..., k: int = ..., dtype: Type[_DType] = ...) -> ndarray: ...
def flatnonzero(a: ndarray[_DType]) -> ndarray[int64]: ...
def full(
    shape: _ShapeType, fill_value: Any, dtype: Optional[Type[_DType]] = ..., order: str = ...
) -> ndarray: ...
def full_like(
    a: Any,
    fill_value: Any,
    dtype: Optional[Type[_DType]] = ...,
    order: str = ...,
    subok: bool = ...,
) -> ndarray: ...

# def fromfunction(
#     function: Callable[..., _S], shape: _ShapeType, dtype: Type[_DType] = float
# ) -> ndarray[_S]: ...
def fromiter(iterable: Iterator, dytpe: Type[_DType], count: int = ...) -> ndarray: ...
def fromstring(
    string: str, dtype: Type[_DType] = ..., count: int = ..., sep: str = ...
) -> ndarray: ...
def histogramdd(
    a: ndarray,
    bins: Optional[Union[ndarray, Series, List, int]],
    range: Optional[List[Tuple[number, number]]] = ...,
    density: bool = ...,
    normed: bool = ...,
    weights: Optional[Union[ndarray, Series, List[number]]] = ...,
) -> Tuple[ndarray, List[number]]: ...
def identity(n: int, dtype: Optional[Type[_DType]] = ...) -> ndarray: ...
def insert(arr: ndarray[_DType], index: int, value: _DType) -> ndarray[_DType]: ...
@overload
def linspace(
    start: float, stop: float, num: int = ..., endpoint: bool = ...
) -> ndarray[float64]: ...
@overload
def linspace(
    start: float, stop: float, *, dtype: Type[_DType], num: int = ..., endpoint: bool = ...
) -> ndarray[_DType]: ...
def load(file: Union[str, os.PathLike, IO], encoding: str = ...) -> Dict[str, ndarray]: ...
def loadtxt(
    fname: Any,
    dtype: Type[_DType] = ...,
    comments: Union[str, Sequence[str]] = ...,
    delimiter: Optional[str] = ...,
    converters: Optional[Dict[int, Callable[[Any], float]]] = ...,
    skiprows: int = ...,
    usecols: Optional[Sequence[int]] = ...,
    unpack: bool = ...,
    ndmin: int = ...,
) -> ndarray: ...
@overload
def ones(shape: _ShapeType, order: str = ...) -> ndarray[float64]: ...
@overload
def ones(shape: _ShapeType, dtype: Type[_DType] = ..., order: str = ...) -> ndarray[_DType]: ...
@overload
def ones_like(a: ndarray[_DType], subok: bool = ...) -> ndarray[_DType]: ...
@overload
def ones_like(a: ndarray, dtype: Type[_DType], subok: bool = ...) -> ndarray[_DType]: ...
@overload
def repeat(a: _DType, repeats: _IntLike) -> ndarray[_DType]: ...
@overload
def repeat(a: int, repeats: _IntLike) -> ndarray[int64]: ...
@overload
def repeat(a: float, repeats: _IntLike) -> ndarray[float64]: ...
@overload
def repeat(a: ndarray[_DType], repeats: _IntLike) -> ndarray[_DType]: ...
@overload
def zeros(shape: _ShapeType, order: str = ...) -> ndarray[float64]: ...
@overload
def zeros(shape: _ShapeType, dtype: Type[_DType] = ..., order: str = ...) -> ndarray[_DType]: ...
@overload
def zeros_like(a: ndarray[_DType], order: str = ..., subok: bool = ...) -> ndarray[_DType]: ...
@overload
def zeros_like(a: ndarray, dtype: Type[_DType], subok: bool = ...) -> ndarray[_DType]: ...

#
# Array transformation routines
#
def abs(x: ndarray[_DType]) -> ndarray[_DType]: ...
def add(x1: ndarray[_DType], x2: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def all(a: ndarray[_DType]) -> bool_: ...
@overload
def all(a: ndarray[_DType], axis: _AxesType) -> ndarray[bool_]: ...
@overload
def amax(a: ndarray[_DType]) -> _DType: ...
@overload
def amax(a: ndarray[_DType], axis: _AxesType) -> ndarray[_DType]: ...
def append(a: _ArrayLike, b: _ArrayLike, axis: _AxesType = ...) -> ndarray: ...
@overload
def argmin(a: Sequence, axis: _AxesType = ...) -> int64: ...
@overload
def argmin(
    a: ndarray[_DType], axis: _AxesType = ..., out: Optional[ndarray[_DType]] = ...
) -> ndarray[int64]: ...
@overload
def argmax(a: Sequence, axis: _AxesType = ...) -> int64: ...
@overload
def argmax(
    a: ndarray[_DType], axis: _AxesType = ..., out: Optional[ndarray[_DType]] = ...
) -> ndarray[int64]: ...
def argsort(a: ndarray[_DType], axis: _AxesType = ...) -> ndarray[_DType]: ...
def array_equal(a1: ndarray[_DType], a2: ndarray[_DType]) -> bool: ...
def array_split(
    ary: ndarray[_DType], indices_or_sections: Union[int, List[int]], axis: int = ...
) -> List[ndarray[_DType]]: ...
def asscaler(x: _Int) -> int: ...

# np.asarray
@overload
def asarray(a: ndarray, dtype: Type[_Int]) -> ndarray[_Int]: ...
@overload
def asarray(a: ndarray, dtype: Type[_Float]) -> ndarray[_Float]: ...
@overload
def asarray(a: ndarray, dtype: Type[str_]) -> ndarray[str_]: ...

# the bool overload has to come before the int overload because bool is a subclass of int
@overload
def asarray(a: ndarray, dtype: Type[bool]) -> ndarray[bool_]: ...
@overload
def asarray(a: ndarray, dtype: Type[int]) -> ndarray[int64]: ...
@overload
def asarray(a: ndarray, dtype: Type[float]) -> ndarray[float64]: ...
@overload
def asarray(a: ndarray, dtype: Type[str]) -> ndarray[str_]: ...
@overload
def atleast_2d(ary: _Coercable) -> ndarray: ...
@overload
def atleast_2d(ar: _Coercable, *ary: _Coercable) -> List[ndarray]: ...
@overload
def ceil(a: _FloatLike) -> _FloatLike: ...
@overload
def ceil(a: ndarray[_DType]) -> ndarray[_DType]: ...
def clip(a: ndarray[_DType], a_min: _DType, a_max: _DType) -> ndarray[_DType]: ...
def concatenate(arrays: Sequence[_ArrayLike[_DType]], axis: _AxesType = ...) -> ndarray[_DType]: ...
def corrcoef(
    x: ndarray[_DType], y: Optional[ndarray[_DType]] = ..., rowvar: Optional[bool] = ...
) -> ndarray[float64]: ...
def cos(
    x: Union[_DType, ndarray[_DType], int, float, List[int], List[float]],
    out: Optional[Union[ndarray[_DType], Tuple[ndarray[_DType], None]]] = ...,
    where: Optional[_ArrayLike] = ...,
) -> Union[_DType, ndarray[_DType]]: ...
def cov(m: ndarray[_DType], rowvar: Optional[bool]) -> ndarray[float64]: ...
def deg2rad(
    x: Union[_DType, ndarray[_DType], int, float, List[int], List[float]],
    out: Optional[Union[ndarray[_DType], Tuple[ndarray[_DType], None]]] = ...,
    where: Optional[_ArrayLike] = ...,
) -> Union[_DType, ndarray[_DType]]: ...
def diag(a: ndarray[_DType]) -> ndarray[_DType]: ...
def diff(
    a: ndarray[_DType],
    n: _IntLike = ...,
    axis: _AxesType = ...,
    prepend: ndarray[_DType] = ...,
    append: ndarray[_DType] = ...,
) -> ndarray[_DType]: ...
def digitize(x: ndarray[_DType], bins: ndarray[_DType], right: bool = ...) -> ndarray[_DType]: ...
@overload
def divide(x1: float32, x2: float32) -> float32: ...
@overload
def divide(x1: _DTypeObj, x2: _DTypeObj) -> float64: ...
@overload
def divide(x1: ndarray[float32], x2: Union[ndarray[float32], float32]) -> ndarray[float32]: ...
@overload
def divide(x1: ndarray, x2: Union[ndarray, _DTypeObj]) -> ndarray[float64]: ...
@overload
def divide(x1: Sequence[_AnyNum], x2: _DTypeObj) -> ndarray[float64]: ...
@overload
def dot(x1: _Int, x2: _Int) -> _Int: ...
@overload
def dot(x1: ndarray, x2: ndarray) -> ndarray: ...
@overload
def exp(a: _DTypeObj) -> _DTypeObj: ...
@overload
def exp(a: ndarray[_DType]) -> ndarray[_DType]: ...
def expand_dims(a: ndarray[_DType], axis: _AxesType) -> ndarray[_DType]: ...
def fill_diagonal(a: ndarray[_DType], val: _FloatLike, wrap: bool = ...) -> None: ...
@overload
def floor(x: _FloatLike) -> _FloatLike: ...
@overload
def floor(x: ndarray[_Float]) -> ndarray[_Float]: ...
def hstack(tup: Union[List[ndarray[_DType]], Tuple[ndarray[_DType], ...]]) -> ndarray[_DType]: ...
def isclose(
    a: _ArrayLike, b: _ArrayLike, rtol: float = ..., atol: float = ..., equal_nan: bool = ...
) -> ndarray: ...
def in1d(
    ar1: ndarray[_DType], ar2: ndarray[_DType], assume_unique: bool = ..., inverse: bool = ...
) -> ndarray[bool_]: ...
def interp(
    x: _ArrayLike,
    xp: Sequence[float],
    fp: Sequence[Union[float, complex]],
    left: Optional[Union[float, complex]] = ...,
    right: Optional[Union[float, complex]] = ...,
    period: Optional[float] = ...,
) -> ndarray: ...
def isin(element: Sequence[_DType], test_element: _DType) -> ndarray[_DType]: ...
@overload
def isnan(x: float64) -> bool: ...
@overload
def isnan(x: ndarray[_DType]) -> ndarray[bool_]: ...
@overload
def ix_(x: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def ix_(x1: ndarray[_DType], x2: ndarray[_DType]) -> Tuple[ndarray[_DType], ndarray[_DType]]: ...
@overload
def log(a: _FloatLike) -> _FloatLike: ...
@overload
def log(a: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def log2(a: _FloatLike) -> _FloatLike: ...
@overload
def log2(a: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def log10(a: _FloatLike) -> _FloatLike: ...
@overload
def log10(a: ndarray[_DType]) -> ndarray[_DType]: ...
def logical_and(x1: ndarray[bool_], x2: ndarray[bool_]) -> ndarray[bool_]: ...
def matmul(a: ndarray[_DType], b: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def max(a: ndarray[_DType], axis: None = ...) -> _DType: ...
@overload
def max(a: ndarray[_DType], axis: _AxesType, keepdims: bool = ...) -> ndarray[_DType]: ...
def maximum(a: ndarray[_DType], b: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def mean(a: ndarray[_Float]) -> _Float: ...
@overload
def mean(a: ndarray[_Float], axis: _AxesType, keepdims: bool = ...) -> ndarray[_Float]: ...
def median(
    a: ndarray,
    axis: _IntLike = ...,
    out: ndarray = ...,
    overwrite_input: bool = ...,
    keepdims: bool = ...,
) -> ndarray[float64]: ...
@overload
def min(a: ndarray[_DType], axis: None = ...) -> _DType: ...
@overload
def min(a: ndarray[_DType], axis: _AxesType, keepdims: bool = ...) -> ndarray[_DType]: ...
def minimum(a: ndarray[_DType], b: ndarray[_DType]) -> ndarray[_DType]: ...
def nan_to_num(
    x: ndarray[_DType],
    copy: bool = ...,
    nan: _AnyNum = ...,
    posinf: _AnyNum = ...,
    neginf: _AnyNum = ...,
) -> ndarray[_DType]: ...
def nonzero(a: ndarray) -> Tuple[ndarray[int64], ...]: ...
def outer(a: ndarray[_DType], b: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def percentile(
    a: ndarray[_DType],
    q: _FloatLike,
    interpolation: _InterpolationType = ...,
    axis: _AxesType = ...,
) -> _DType: ...
@overload
def percentile(
    a: ndarray[_DType],
    q: _ArrayLike,
    interpolation: _InterpolationType = ...,
    axis: _AxesType = ...,
) -> ndarray[_DType]: ...
def power(x1: ndarray[_DType], x2: Union[_AnyNum, ndarray[_DType]]) -> ndarray[_DType]: ...
@overload
def prod(a: ndarray[_DType], axis: None = ...) -> _DType: ...
@overload
def prod(a: ndarray[_DType], axis: _AxesType, keepdims: bool = ...) -> ndarray[_DType]: ...
def ravel(a: ndarray[_DType]) -> ndarray[_DType]: ...
def reshape(a: ndarray[_DType], newshape: _ShapeType) -> ndarray[_DType]: ...
def round(a: ndarray[_DType], decimals: _IntLike = ...) -> ndarray[_DType]: ...
def save(
    file: Union[str, os.PathLike, IO],
    arr: ndarray,
    allow_pickle: bool = ...,
    fix_imports: bool = ...,
) -> None: ...
@overload
def searchsorted(a: ndarray[_DType], v: _DType, side: str = ...) -> int64: ...
@overload
def searchsorted(a: ndarray[_DType], v: ndarray[_DType], side: str = ...) -> ndarray[int64]: ...
def setdiff1d(
    ar1: Union[ndarray[_DType], List[_ScalarLike]],
    ar2: Union[ndarray[_DType], List[_ScalarLike]],
    assume_unique: bool = ...,
) -> ndarray[_DType]: ...
def sin(
    x: Union[_DType, ndarray[_DType], int, float, List[int], List[float]],
    out: Optional[Union[ndarray[_DType], Tuple[ndarray[_DType], None]]] = ...,
    where: Optional[_ArrayLike] = ...,
) -> Union[_DType, ndarray[_DType]]: ...
def sign(x: ndarray[_DType]) -> ndarray[_DType]: ...
def sort(a: ndarray[_DType]) -> ndarray[_DType]: ...
def split(
    ary: ndarray[_DType], indices_or_sections: Union[int, List[int]], axis: int = ...
) -> List[ndarray[_DType]]: ...
def square(x: ndarray[_DType]) -> ndarray[_DType]: ...
def squeeze(a: ndarray[_DType], axis: _AxesType = ...) -> ndarray[_DType]: ...
@overload
def sqrt(a: float) -> float: ...
@overload
def sqrt(a: ndarray) -> ndarray[float64]: ...
def stack(arrays: List[ndarray[_DType]], axis: _AxesType = ...) -> ndarray[_DType]: ...
@overload
def std(a: ndarray[_Float]) -> _Float: ...
@overload
def std(a: ndarray[_Float], axis: _AxesType, keepdims: bool = ...) -> ndarray[_Float]: ...
def subtract(
    x1: ndarray[_DType], x2: ndarray[_DType], axis: Optional[int] = ...
) -> ndarray[_DType]: ...
@overload
def sum(a: ndarray[_DType], axis: None = ...) -> _DType: ...
@overload
def sum(a: ndarray[_DType], axis: _AxesType, keepdims: bool = ...) -> ndarray[_DType]: ...
def take(a: ndarray[_DType], indices: ndarray[_Int], axis: _AxesType = ...) -> ndarray[_DType]: ...
def take_along_axis(
    arr: ndarray[_DType], indices: ndarray[_Int], axis: _AxesType = ...
) -> ndarray[_DType]: ...
def tan(
    x: Union[_DType, ndarray[_DType], int, float, List[int], List[float]],
    out: Optional[Union[ndarray[_DType], Tuple[ndarray[_DType], None]]] = ...,
    where: Optional[_ArrayLike] = ...,
) -> Union[_DType, ndarray[_DType]]: ...
def tile(a: ndarray[_DType], reps: Union[_NestedList[int], ndarray[_Int]]) -> ndarray[_DType]: ...
def trace(a: ndarray[_DType]) -> _DType: ...
def transpose(a: ndarray[_DType]) -> ndarray[_DType]: ...
def tril(m: ndarray[_DType], k: Optional[int] = ...) -> ndarray[_DType]: ...
def tril_indices(n: _IntLike, k: _IntLike = ..., m: _IntLike = ...) -> Tuple[ndarray, ndarray]: ...
def triu(m: ndarray[_DType], k: Optional[int] = ...) -> ndarray[_DType]: ...
@overload
def unique(a: ndarray[_DType], axis: Optional[int] = ...) -> ndarray[_DType]: ...
@overload
def unique(
    a: ndarray[_DType], return_counts: bool = ..., axis: Optional[int] = ...
) -> Tuple[ndarray[_DType], ndarray[_DType]]: ...
@overload
def unique(
    a: ndarray[_DType], return_inverse: bool = ..., axis: Optional[int] = ...
) -> Tuple[ndarray[_DType], ndarray[_DType]]: ...
def vstack(tup: Sequence[ndarray[_DType]]) -> ndarray[_DType]: ...
@overload
def where(condition: _ConditionType, x: ndarray[_DType], y: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def where(condition: _ConditionType, x: _ScalarLike, y: ndarray[_DType]) -> ndarray[_DType]: ...
@overload
def where(condition: _ConditionType, x: ndarray[_DType], y: _ScalarLike) -> ndarray[_DType]: ...
@overload
def where(condition: _ConditionType, x: _DType, y: _DType) -> ndarray[_DType]: ...
@overload
def where(condition: _ConditionType, x: int, y: int) -> ndarray[int64]: ...
@overload
def where(condition: _ConditionType, x: float, y: float) -> ndarray[float64]: ...
@overload
def where(condition: _ConditionType) -> Tuple[ndarray[int64], ...]: ...

#
# nan series methods
#
nancumsum = cumsum
nanmean = mean
nanstd = std
nansum = sum

#
# Saving methods
#
def savetxt(
    fname: str,
    X: ndarray,
    *,
    header: str = ...,
    delimiter: str = ...,
    newline: str = ...,
    comments: str = ...,
) -> None: ...
def savez(file: Path, *args: ndarray, **kwds: ndarray) -> None: ...
def savez_compressed(file: Path, *args: ndarray, **kwds: ndarray) -> None: ...

#
# weird classes
#
class matrix:
    def __init__(self, data: Union[List, str], dtype: Type[_DType] = ..., copy: bool = ...): ...
    def reshape(self, shape: _ShapeType) -> matrix: ...

class finfo(Generic[_Float]):
    eps: _Float
    resolution: _Float
    min: _Float
    max: _Float
    dtype: _Float
    @overload
    def __init__(self, dtype: _Float): ...
    @overload
    def __init__(self, dtype: Type[_Float]): ...
    @overload
    def __init__(self: finfo[float64], dtype: Union[float, Type[float]]): ...

#
# module functions
#
def set_printoptions(
    precision: Any = ...,
    threshold: Any = ...,
    edgeitems: Any = ...,
    linewidth: Any = ...,
    suppress: Any = ...,
    nanstr: Any = ...,
    infstr: Any = ...,
    formatter: Any = ...,
    sign: Any = ...,
    floatmode: Any = ...,
    *,
    legacy: Any = ...,
) -> None: ...

#
# Specific values
#
e: float
inf: float
nan: float
NaN: float
NAN: float
pi: float

# Local Variables:
# blacken-line-length: 100
# blacken-allow-py36: t
# blacken-skip-string-normalization: t
# End:
