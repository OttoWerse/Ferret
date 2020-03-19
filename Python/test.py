from types import FunctionType

foo_code = compile('def foo(): return "bar"', "<string>", "exec")
foo_func = FunctionType(foo_code.co_consts[0], globals(), "foo")

print(foo_func())