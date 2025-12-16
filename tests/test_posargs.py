"""Tests for position arguments ({posargs}) feature."""

from uvtx.variables import interpolate_posargs


class TestInterpolatePosargs:
    """Test the interpolate_posargs function."""

    def test_posargs_with_args(self) -> None:
        """Test {posargs} with provided arguments."""
        result = interpolate_posargs("pytest {posargs}", ["tests/unit", "-v"])
        assert result == "pytest tests/unit -v"

    def test_posargs_without_args(self) -> None:
        """Test {posargs} without arguments (empty string)."""
        result = interpolate_posargs("pytest {posargs}", None)
        assert result == "pytest "

    def test_posargs_with_default(self) -> None:
        """Test {posargs:default} without arguments."""
        result = interpolate_posargs("pytest {posargs:tests/}", None)
        assert result == "pytest tests/"

    def test_posargs_with_default_overridden(self) -> None:
        """Test {posargs:default} with provided arguments."""
        result = interpolate_posargs("pytest {posargs:tests/}", ["tests/unit"])
        assert result == "pytest tests/unit"

    def test_posargs_empty_default(self) -> None:
        """Test {posargs:} with empty default."""
        result = interpolate_posargs("pytest {posargs:}", None)
        assert result == "pytest "

    def test_posargs_empty_list(self) -> None:
        """Test {posargs} with empty list (no args)."""
        result = interpolate_posargs("pytest {posargs:tests/}", [])
        assert result == "pytest tests/"

    def test_multiple_posargs_same_value(self) -> None:
        """Test multiple {posargs} in same string get same replacement."""
        result = interpolate_posargs("cmd {posargs} and {posargs}", ["arg1"])
        assert result == "cmd arg1 and arg1"

    def test_posargs_in_middle(self) -> None:
        """Test {posargs} in middle of command."""
        result = interpolate_posargs("pytest {posargs:tests/} -v --strict", ["tests/unit"])
        assert result == "pytest tests/unit -v --strict"

    def test_posargs_multiple_args_joined(self) -> None:
        """Test {posargs} joins multiple args with spaces."""
        result = interpolate_posargs("pytest {posargs}", ["tests/unit", "-k", "fast"])
        assert result == "pytest tests/unit -k fast"

    def test_no_posargs_placeholder(self) -> None:
        """Test string without {posargs} is unchanged."""
        result = interpolate_posargs("pytest tests/", ["arg1"])
        assert result == "pytest tests/"

    def test_posargs_with_special_chars_in_default(self) -> None:
        """Test {posargs} with special characters in default value."""
        result = interpolate_posargs("echo {posargs:hello world!}", None)
        assert result == "echo hello world!"

    def test_posargs_with_path_default(self) -> None:
        """Test {posargs} with path-like default."""
        result = interpolate_posargs("pytest {posargs:tests/unit/test_*.py}", None)
        assert result == "pytest tests/unit/test_*.py"

    def test_posargs_with_colon_in_args(self) -> None:
        """Test {posargs} handles colons in actual arguments."""
        result = interpolate_posargs("cmd {posargs}", ["key:value"])
        assert result == "cmd key:value"

    def test_posargs_multiple_defaults_same_replacement(self) -> None:
        """Test multiple {posargs:default} with different defaults but same args."""
        result = interpolate_posargs("{posargs:def1} and {posargs:def2}", ["arg1"])
        assert result == "arg1 and arg1"

    def test_posargs_empty_string_input(self) -> None:
        """Test {posargs} with empty string."""
        result = interpolate_posargs("", None)
        assert result == ""

    def test_posargs_no_space_after_prefix(self) -> None:
        """Test command starting immediately after posargs."""
        result = interpolate_posargs("pytest{posargs}", ["tests/"])
        assert result == "pytesttests/"
