#!/usr/bin/env python3

'''
`py.test`-driven unit test suite for the `@beartype` decorator, implementing a
rudimentary subset of PEP 484-style type checking based on Python 3.x function
annotations.

Usage
----------
These tests assume the `@beartype` decorator and all utility functions (e.g.,
`_check_type_annotation()`) and globals (e.g., `_PARAMETER_KIND_IGNORED`)
required by this decorator to reside in a top-level module named `beartype`. If
this is the case, these tests may be run as is with:

    $ py.test -k test_beartype

See Also
----------
https://stackoverflow.com/a/37961120/2809027
    Stackoverflow answer introducing the `@beartype` decorator.
'''
from unittest import TestCase

import pytest
import typing

from testfixtures import should_raise

from fl.datamigration.tools.beartype.beartype import beartype


class TestBearyype(TestCase):
    def test_beartype_noop(self) -> None:
        '''
        Test bear typing of a function with no function annotations, reducing to
        _no_ type checking.
        '''

        # Unannotated function to be type checked.
        @beartype
        def khorne(gork, mork):
            return gork + mork

        # Call this function and assert the expected return value.
        assert khorne('WAAAGH!', '!HGAAAW') == 'WAAAGH!!HGAAAW'

    # ....................{ TESTS ~ pass : param               }....................
    def test_beartype_pass_param_keyword_and_positional(self) -> None:
        '''
        Test bear typing of a function call successfully passed both annotated
        positional and keyword parameters.
        '''

        # Function to be type checked.
        @beartype
        def slaanesh(daemonette: str, keeper_of_secrets: str) -> str:
            return daemonette + keeper_of_secrets

        # Call this function with both positional and keyword arguments and assert
        # the expected return value.
        assert slaanesh(
            'Seeker of Decadence', keeper_of_secrets="N'Kari") == (
            "Seeker of DecadenceN'Kari")


    def test_beartype_pass_param_keyword_only(self) -> None:
        '''
        Test bear typing of a function call successfully passed an annotated
        keyword-only parameter following an `*` or `*args` parameter.
        '''

        # Function to be type checked.
        @beartype
        def changer_of_ways(sky_shark: str, *, chaos_spawn: str) -> str:
            return sky_shark + chaos_spawn

        # Call this function with keyword arguments and assert the expected return
        # value.
        assert changer_of_ways(
            'Screamers', chaos_spawn="Mith'an'driarkh") == (
            "ScreamersMith'an'driarkh")


    def test_beartype_pass_param_tuple(self) -> None:
        '''
        Test bear typing of a function call successfully passed a parameter
        annotated as a tuple.
        '''

        # Function to be type checked.
        @beartype
        def genestealer(tyranid: str, hive_fleet: (str, int)) -> str:
            return tyranid + str(hive_fleet)

        # Call this function with each of the two types listed in the above tuple.
        assert genestealer(
            'Norn-Queen', hive_fleet='Behemoth') == 'Norn-QueenBehemoth'
        assert genestealer(
            'Carnifex', hive_fleet=0xDEADBEEF) == 'Carnifex3735928559'


    def test_type_check_pass_param_custom(self) -> None:
        '''
        Test bear typing of a function call successfully passed a parameter
        annotated as a user-defined rather than builtin type.
        '''

        # User-defined type.
        class CustomTestStr(str):
            pass

        # Function to be type checked.
        @beartype
        def hrud(gugann: str, delphic_plague: CustomTestStr) -> str:
            return gugann + delphic_plague

        # Call this function with each of the two types listed in the above tuple.
        assert hrud(
            'Troglydium hruddi', delphic_plague=CustomTestStr('Delphic Sink')) == (
            'Troglydium hruddiDelphic Sink')


    def test_type_check_pass_typing_module(self) -> None:
        '''
        Test bear typing of a function call successfully passed a parameter
        annotated with an abstract type from the typing module.
        '''

        MyMap = typing.Mapping

        @beartype
        def function(par: MyMap, ameter: MyMap) -> MyMap:
            result = par.copy()
            result.update(ameter)
            return result

        assert function({1:1}, {2:2}) == {1:1, 2:2}


    def test_type_check_pass_parameterized_typing_module(self) -> None:
        '''
        Test bear typing of a function call successfully passed a parameter
        annotated with a parametirized abstract type from the typing module.
        '''
        MyMap = typing.Mapping

        @beartype
        def function(par: MyMap, ameter: MyMap) -> MyMap:
            result = par.copy()
            result.update(ameter)
            return result

        assert function({1:1}, {2:2}) == {1:1, 2:2}


    # ....................{ TESTS ~ pass : return              }....................
    def test_type_check_pass_return_none(self) -> None:
        '''
        Test bear typing of a function call successfully returning `None` and
        annotated as such.
        '''

        # Function to be type checked.
        @beartype
        def xenos(interex: str, diasporex: str) -> None:
            interex + diasporex

        # Call this function and assert no value to be returned.
        assert xenos(
            'Luna Wolves', diasporex='Iron Hands Legion') is None

    # ....................{ TESTS ~ fail                       }....................
    def test_beartype_fail_keyword_unknown(self) -> None:
        '''
        Test bear typing of an annotated function call passed an unrecognized
        keyword parameter.
        '''

        # Annotated function to be type checked.
        @beartype
        def tau(kroot: str, vespid: str) -> str:
            return kroot + vespid

        # Call this function with an unrecognized keyword parameter and assert the
        # expected exception.
        with pytest.raises(TypeError) as exception:
            tau(kroot='Greater Good', nicassar='Dhow')

        # For readability, this should be a "TypeError" synopsizing the exact issue
        # raised by the Python interpreter on calling the original function rather
        # than a "TypeError" failing to synopsize the exact issue raised by the
        # wrapper type-checking the original function. Since the function
        # annotations defined above guarantee that the exception message of the
        # latter will be suffixed by "not a str", ensure this is *NOT* the case.
        assert not str(exception.value).endswith('not a str')


    def test_beartype_fail_param_name(self) -> None:
        '''
        Test bear typing of a function accepting a parameter name reserved for
        use by the `@beartype` decorator.
        '''

        # Define a function accepting a reserved parameter name and assert the
        # expected exception.
        @beartype
        @should_raise(NameError)
        def jokaero(weaponsmith: str, __beartype_func: str) -> str:
            return weaponsmith + __beartype_func

    # ....................{ TESTS ~ fail : type                }....................
    def test_beartype_fail_param_type(self) -> None:
        '''
        Test bear typing of an annotated function call failing a parameter type
        check.
        '''


        # Annotated function to be type checked.
        @beartype
        def eldar(isha: str, asuryan: (str, int)) -> str:
            return isha + asuryan

        # Call this function with an invalid type and assert the expected exception.
        with pytest.raises(TypeError):
            eldar('Mother of the Eldar', 100.100)


    def test_beartype_fail_return_type(self) -> None:
        '''
        Test bear typing of an annotated function call failing a return type
        check.
        '''

        # Annotated function to be type checked.
        @beartype
        def necron(star_god: str, old_one: str) -> str:
            return 60e6

        # Call this function and assert the expected exception.
        with pytest.raises(TypeError):
            necron("C'tan", 'Elder Thing')

    # ....................{ TESTS ~ fail : annotation          }....................
    def test_beartype_fail_annotation_param(self) -> None:
        '''
        Test bear typing of a function with an unsupported parameter annotation.
        '''

        # Assert the expected exception from attempting to type check a function
        # with a parameter annotation that is *NOT* a type.
        with pytest.raises(TypeError):
            @beartype
            def nurgle(nurgling: str, great_unclean_one: 'Bringer of Poxes') -> str:
                return nurgling + great_unclean_one


    def test_beartype_fail_annotation_return(self) -> None:
        '''
        Test bear typing of a function with an unsupported return annotation.
        '''

        # Assert the expected exception from attempting to type check a function
        # with a return annotation that is *NOT* a type.
        with pytest.raises(TypeError):
            @beartype
            def tzeentch(disc: str, lord_of_change: str) -> 'Player of Games':
                return disc + lord_of_change