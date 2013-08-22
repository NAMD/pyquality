# coding: utf-8

import datetime

from render_report import convert_date


def test_convert_date():
    result = convert_date('"Sat Sep 10 01:32:14 2011 +0000"')
    expected = datetime.datetime(2011, 9, 10, 1, 32, 14)
    assert result == expected

    # should always return UTC time
    result = convert_date('"Sat Sep 10 01:32:14 2011 +0530"')
    expected = datetime.datetime(2011, 9, 9, 20, 2, 14)
    assert result == expected
    result = convert_date('"Sat Sep 10 01:32:14 2011 -0530"')
    expected = datetime.datetime(2011, 9, 10, 7, 02, 14)
    assert result == expected
