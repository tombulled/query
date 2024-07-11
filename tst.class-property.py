class ExpressionMeta(type):
    __key = "default"

    @property
    def key(self):
        print(f"Getting key from {self!r}")
        return self.__key

    @key.setter
    def key(self, key):
        print(f"Setting key on {self!r} to {key!r}")
        self.__key = key


class Expression(metaclass=ExpressionMeta):
    pass
    # key = "bob"

    @property
    def key(self):
        return type(self).key


class Exists(Expression):
    key = "exists"
