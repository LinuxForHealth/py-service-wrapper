import unittest
from inspect import Parameter
from typing import Union

from ..utils import path_builder


class TestPathBuilder(unittest.TestCase):
    def setUp(self) -> None:
        def test_func(a: str, b: int, *, k: bool, d: float = 10.0):
            return True

        def test_func_union(a: str, b: Union[str, int], *, k: bool, d: float = 10.0):
            return True

        self.func = test_func
        self.func_union = test_func_union

    def test_build_path_not_callable_func_fails(self):
        with self.assertRaises(TypeError) as ex_check:
            path_builder.build_path(func='not a func')
        self.assertEqual(str(ex_check.exception), 'not a func is not a callable object.')

    def test_build_param_not_simple_type(self):
        expected_path = 'test_func_union/{a:str}/{b}/{k:bool}'
        path = path_builder.build_path(self.func_union)
        self.assertEqual(path, expected_path)

    def test_build_path_with_base_name(self):
        expected_path = 'base/{a:str}/{b:int}/{k:bool}'
        path = path_builder.build_path(self.func, 'base')
        self.assertEqual(path, expected_path)

    def test_build_path_without_base_name(self):
        expected_path = 'test_func/{a:str}/{b:int}/{k:bool}'
        path = path_builder.build_path(self.func)
        self.assertEqual(path, expected_path)

    def test_build_path_with_param_kind(self):
        expected_path = 'test_func/{k:bool}'
        path = path_builder.build_path(self.func, param_kinds=[Parameter.KEYWORD_ONLY])
        self.assertEqual(path, expected_path)
