"""Tests for pt.executor."""

from uvtx.executor import UvCommand


class TestUvCommand:
    """Tests for UvCommand class."""

    def test_basic_script(self) -> None:
        cmd = UvCommand(script="script.py")
        result = cmd.build()
        assert result == ["uv", "run", "script.py"]

    def test_script_with_args(self) -> None:
        cmd = UvCommand(script="script.py", args=["--verbose", "-n", "4"])
        result = cmd.build()
        assert result == ["uv", "run", "script.py", "--verbose", "-n", "4"]

    def test_script_with_dependencies(self) -> None:
        cmd = UvCommand(
            script="script.py",
            dependencies=["requests", "pydantic>=2.0"],
        )
        result = cmd.build()
        assert result == [
            "uv",
            "run",
            "--with",
            "requests",
            "--with",
            "pydantic>=2.0",
            "script.py",
        ]

    def test_script_with_python_version(self) -> None:
        cmd = UvCommand(script="script.py", python="3.11")
        result = cmd.build()
        assert result == ["uv", "run", "--python", "3.11", "script.py"]

    def test_cmd_mode(self) -> None:
        cmd = UvCommand(cmd="python -c 'print(1)'")
        result = cmd.build()
        assert result == ["uv", "run", "python", "-c", "print(1)"]

    def test_cmd_with_dependencies(self) -> None:
        cmd = UvCommand(
            cmd="ruff check src/",
            dependencies=["ruff"],
        )
        result = cmd.build()
        assert "--with" in result
        assert "ruff" in result
        assert "check" in result

    def test_full_command(self) -> None:
        cmd = UvCommand(
            script="test.py",
            args=["--verbose"],
            dependencies=["pytest", "pytest-cov"],
            python="3.12",
        )
        result = cmd.build()
        assert result == [
            "uv",
            "run",
            "--python",
            "3.12",
            "--with",
            "pytest",
            "--with",
            "pytest-cov",
            "test.py",
            "--verbose",
        ]

    def test_build_env(self) -> None:
        cmd = UvCommand(
            script="test.py",
            env={"DEBUG": "1", "LOG_LEVEL": "info"},
        )
        env = cmd.build_env()

        assert env["DEBUG"] == "1"
        assert env["LOG_LEVEL"] == "info"
        # Should also include current env
        assert "PATH" in env  # Standard env var

    def test_ignore_failure_cmd_prefix(self) -> None:
        """Test that '- ' prefix in cmd sets ignore_failure and strips prefix."""
        cmd = UvCommand(cmd="- rm -rf temp/")
        assert cmd.ignore_failure is True
        assert cmd.cmd == "rm -rf temp/"
        # Verify command builds correctly without prefix
        result = cmd.build()
        assert "rm" in result
        assert "-rf" in result

    def test_ignore_failure_script_prefix(self) -> None:
        """Test that '- ' prefix in script sets ignore_failure and strips prefix."""
        cmd = UvCommand(script="- cleanup.py")
        assert cmd.ignore_failure is True
        assert cmd.script == "cleanup.py"

    def test_no_ignore_failure_without_prefix(self) -> None:
        """Test that commands without prefix have ignore_failure=False."""
        cmd = UvCommand(cmd="pytest tests/")
        assert cmd.ignore_failure is False
        assert cmd.cmd == "pytest tests/"

    def test_ignore_failure_explicit(self) -> None:
        """Test explicitly setting ignore_failure flag."""
        cmd = UvCommand(cmd="rm temp/", ignore_failure=True)
        assert cmd.ignore_failure is True
        assert cmd.cmd == "rm temp/"  # No prefix stripping

    def test_cmd_with_dash_but_no_space(self) -> None:
        """Test that dash without space is not treated as prefix."""
        cmd = UvCommand(cmd="-v --verbose")
        assert cmd.ignore_failure is False
        assert cmd.cmd == "-v --verbose"
