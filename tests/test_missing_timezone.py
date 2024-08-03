import ast

from lint_plugins.missing_timezone import TimezoneChecker


def run_checker(line):
    checker = TimezoneChecker(ast.parse(line))
    return list(checker.run())


def test_missing_timezone():
    good_line = (
        "timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)"
    )
    bad_line1 = (
        "timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False), nullable=True, default=None)"
    )
    bad_line2 = "timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True, default=None)"

    assert run_checker(good_line) == []

    bad_line1_result = run_checker(bad_line1)
    assert len(bad_line1_result) == 1
    assert bad_line1_result[0][2] == TimezoneChecker.error_template

    bad_line2_result = run_checker(bad_line2)
    assert len(bad_line2_result) == 1
    assert bad_line2_result[0][2] == TimezoneChecker.error_template
