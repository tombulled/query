from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import (
    Any,
    ClassVar,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    cast,
    final,
)

"""
Notes:
    * `path` refers to a field (referenced as a "field path", e.g. "path.to.something")
"""

T = TypeVar("T")
Value = Any
Document = Mapping[str, Any]


# Referred to as "operator type"
class MatchType(Enum):
    # tree types
    AND = auto()
    # OR = auto()

    # array types
    # ELEM_MATCH_OBJECT = auto()
    # ELEM_MATCH_VALUE = auto()
    # SIZE = auto()

    # leaf types
    EQ = auto()
    # LTE = auto()
    # LT = auto()
    # GT = auto()
    # GTE = auto()
    # REGEX = auto()
    # MOD = auto()
    # EXISTS = auto()
    # MATCH_IN = auto()
    # BITS_ALL_SET = auto()
    # BITS_ALL_CLEAR = auto()
    # BITS_ANY_SET = auto()
    # BITS_ANY_CLEAR = auto()

    # Negations.
    # NOT = auto()
    # NOR = auto()

    # special types
    # TYPE_OPERATOR = auto()
    # GEO = auto()
    # WHERE = auto()
    # EXPRESSION = auto()

    # Boolean expressions.
    ALWAYS_FALSE = auto()
    ALWAYS_TRUE = auto()

    # Things that we parse but cannot be answered without an index.
    # GEO_NEAR = auto()
    # TEXT = auto()

    # Expressions that are only created internally
    # INTERNAL_2D_POINT_IN_ANNULUS = auto()
    # INTERNAL_BUCKET_GEO_WITHIN = auto()

    # Used to represent expression language comparisons in a match expression tree, since $eq,
    # $gt, $gte, $lt and $lte in the expression language has different semantics than their
    # respective match expressions.
    # INTERNAL_EXPR_EQ = auto()
    # INTERNAL_EXPR_GT = auto()
    # INTERNAL_EXPR_GTE = auto()
    # INTERNAL_EXPR_LT = auto()
    # INTERNAL_EXPR_LTE = auto()

    # Used to represent the comparison to a hashed index key value.
    # INTERNAL_EQ_HASHED_KEY = auto()

    # JSON Schema expressions.
    # INTERNAL_SCHEMA_ALLOWED_PROPERTIES = auto()
    # INTERNAL_SCHEMA_ALL_ELEM_MATCH_FROM_INDEX = auto()
    # INTERNAL_SCHEMA_BIN_DATA_ENCRYPTED_TYPE = auto()
    # INTERNAL_SCHEMA_BIN_DATA_FLE2_ENCRYPTED_TYPE = auto()
    # INTERNAL_SCHEMA_BIN_DATA_SUBTYPE = auto()
    # INTERNAL_SCHEMA_COND = auto()
    # INTERNAL_SCHEMA_EQ = auto()
    # INTERNAL_SCHEMA_FMOD = auto()
    # INTERNAL_SCHEMA_MATCH_ARRAY_INDEX = auto()
    # INTERNAL_SCHEMA_MAX_ITEMS = auto()
    # INTERNAL_SCHEMA_MAX_LENGTH = auto()
    # INTERNAL_SCHEMA_MAX_PROPERTIES = auto()
    # INTERNAL_SCHEMA_MIN_ITEMS = auto()
    # INTERNAL_SCHEMA_MIN_LENGTH = auto()
    # INTERNAL_SCHEMA_MIN_PROPERTIES = auto()
    # INTERNAL_SCHEMA_OBJECT_MATCH = auto()
    # INTERNAL_SCHEMA_ROOT_DOC_EQ = auto()
    # INTERNAL_SCHEMA_TYPE = auto()
    # INTERNAL_SCHEMA_UNIQUE_ITEMS = auto()
    # INTERNAL_SCHEMA_XOR = auto()


class MatchCategory(Enum):
    # Expressions that are leaves on the AST, these do not have any children.
    LEAF = auto()
    # Logical Expressions such as $and, $or, etc. that do not have a path and may have
    # one or more children.
    LOGICAL = auto()
    # Expressions that operate on arrays only.
    ARRAY_MATCHING = auto()
    # Expressions that don't fall into any particular bucket.
    OTHER = auto()


class MatchExpression(Iterable["MatchExpression"]):
    __match_type: MatchType  # operator

    def __len__(self) -> int:
        return 0

    def __iter__(self) -> Iterator["MatchExpression"]:
        return iter(())

    def __getitem__(self, index: int) -> "MatchExpression":
        raise IndexError

    # def __eq__(self, )

    def __init__(self, match_type: MatchType) -> None:
        self.__match_type = match_type

    @property
    def match_type(self) -> MatchType:
        return self.__match_type

    # def optimise(self) -> None:
    #     pass

    # @final
    # @staticmethod
    # def sort(self) -> "MatchExpression":
    #     return self

    # def normalise(): ...
    # def parameterise(): ...
    # def unparameterise(): ...
    # def num_children(self) -> int:
    #     return 0
    # def get_child(self, index: int) -> Optional["MatchExpression"]:
    # def get_child(self, index: int) -> "MatchExpression":
    #     return None
    # def get_children(self) -> Sequence["MatchExpression"]:
    #     return ()
    def path(self) -> Optional[str]:
        return None

    # def field_ref(self) -> "FieldRef": ...
    def get_category(
        self,
    ) -> Optional[MatchCategory]:  # TODO: Should this be optional or abstract?
        return None

    # @abstractmethod
    # def __eq__(self, other: "MatchExpression") -> bool:
    #     raise NotImplementedError

    @abstractmethod
    def matches(self, document: Document) -> bool:
        raise NotImplementedError

    # def serialise(): ...
    # def is_trivially_false(): ...  # e.g. OR with no expressions
    # def is_trivially_true(): ...
    # def to_debug_string(): ...
    # def to_string(): ...

    @abstractmethod
    def serialise(self) -> Any:  # TODO: Type other than Any?
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def parse(self, v):
        raise NotImplementedError


"""
A PathMatchExpression is an expression that acts on a field path with syntax
like "path.to.something": {$operator: ...}. Many such expressions are leaves in
the AST, such as $gt, $mod, $exists, and so on. But expressions that are not
leaves, such as $_internalSchemaObjectMatch, may also match against a field
path.
"""


class PathMatchExpression(MatchExpression):
    __element_path: Optional[str]

    def __init__(self, match_type: MatchType, path: Optional[str]) -> None:
        super().__init__(match_type)

        self.__element_path = path

    @property
    def path(self) -> Optional[str]:
        return self.__element_path

    @path.setter
    def path(self, path: str) -> None:
        self.__element_path = path

    def serialise(self) -> Any:
        return {self.path: self.serialise_rhs()}

    @abstractmethod
    def serialise_rhs(self) -> Any:  # Change type?
        raise NotImplementedError


class LeafMatchExpression(PathMatchExpression):
    @staticmethod
    def get_category() -> MatchCategory:
        return MatchCategory.LEAF


class ComparisonMatchExpressionBase(ABC, LeafMatchExpression, Generic[T]):
    _rhs: T

    def __init__(self, match_type: MatchType, path: Optional[str], rhs: T) -> None:
        super().__init__(match_type, path)

        self._rhs = rhs

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.path!r}, {self._rhs!r})"

    def __eq__(self, other: MatchExpression, /) -> bool:
        if self.match_type != other.match_type:
            return False

        real_other = cast(ComparisonMatchExpressionBase, other)

        return self.path == real_other.path and self._rhs == other._rhs

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    # def get_data(self) -> "BSONElement":
    #     return self._rhs

    @property
    def data(self) -> T:
        return self._rhs

    # def set_data(self, elem: "BSONElement"):
    #     self._rhs = elem

    def serialise_rhs(self) -> Any:
        return {self.name(): self.data}


class ComparisonMatchExpression(ComparisonMatchExpressionBase[T], Generic[T]):
    @staticmethod
    def is_comparison_match_expression(expr: MatchType) -> bool:
        return expr in (
            # MatchType.LT,
            # MatchType.LTE,
            MatchType.EQ,
            # MatchType.GTE,
            # MatchType.GT,
        )

    @staticmethod
    def is_comparison_match_expression(expr: MatchExpression) -> bool:
        return ComparisonMatchExpression.is_comparison_match_expression(expr.match_type)


class EqualityMatchExpression(ComparisonMatchExpression[T], Generic[T]):
    k_name: ClassVar[str] = "$eq"

    def __init__(self, path: Optional[str], rhs: T) -> None:
        super().__init__(MatchType.EQ, path, rhs)

    def __str__(self) -> str:
        path: str = repr(self.path) if self.path is not None else "???"

        return f"{path}=={self.data!r}"

    @classmethod
    def name(cls) -> str:
        return cls.k_name

    def matches(self, document: Document) -> bool:
        return document[self.path] == self.data
    
    @staticmethod
    def parse(v):
        # return v
        return EqualityMatchExpression(path=None, rhs=v)


class ListOfMatchExpression(MatchExpression):
    __expressions: List[MatchExpression]

    def __init__(self, match_type: MatchType, expressions: List[MatchExpression]):
        super().__init__(match_type)

        self.__expressions = expressions

    def __len__(self) -> int:
        return len(self.__expressions)

    def __iter__(self) -> Iterator["MatchExpression"]:
        return iter(self.__expressions)

    def __getitem__(self, index: int) -> "MatchExpression":
        return self.__expressions[index]

    @staticmethod
    def get_category() -> MatchCategory:
        return MatchCategory.LOGICAL


class AndMatchExpression(ListOfMatchExpression):
    k_name: ClassVar[str] = "$and"

    def __init__(self, expressions: List[MatchExpression]):
        super().__init__(MatchType.AND, expressions)

    def matches(self, _: Document) -> bool:
        return NotImplemented

    def serialise(self) -> Any:
        return {self.k_name: [child.serialise() for child in self]}


class AlwaysBooleanMatchExpression(MatchExpression):
    __value: bool

    def __init__(self, match_type: MatchType, value: bool) -> None:
        super().__init__(match_type)

        self.__value = value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__value})"

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    def matches(self, _: Document) -> bool:
        return self.__value

    def serialise(self) -> Any:
        return {self.name(): {}}


class AlwaysFalseMatchExpression(AlwaysBooleanMatchExpression):
    k_name: ClassVar[str] = "$alwaysFalse"

    def __init__(self) -> None:
        super().__init__(MatchType.ALWAYS_FALSE, False)

    @classmethod
    def name(cls) -> str:
        return cls.k_name


class AlwaysTrueMatchExpression(AlwaysBooleanMatchExpression):
    k_name: ClassVar[str] = "$alwaysTrue"

    def __init__(self) -> None:
        super().__init__(MatchType.ALWAYS_TRUE, True)

    @classmethod
    def name(cls) -> str:
        return cls.k_name
