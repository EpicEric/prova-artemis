import math
import unittest

from cached_property import cached_property
from last_lines import last_lines
from reconcile_accounts import reconcile_accounts


class TestReconcileAccounts(unittest.TestCase):
    def test_second_list_empty(self):
        transactions_1 = [
            ["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
            ["2020-12-05", "Tecnologia", "50.00", "AWS"],
        ]
        transactions_2 = []
        out_1, out_2 = reconcile_accounts(transactions_1, transactions_2)
        self.assertEqual(
            out_1,
            [
                ["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "MISSING"],
                ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "MISSING"],
                ["2020-12-05", "Tecnologia", "50.00", "AWS", "MISSING"],
            ],
        )
        self.assertEqual(out_2, [])

    def test_almost_all_matches(self):
        transactions_1 = [
            ["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
            ["2020-12-05", "Tecnologia", "50.00", "AWS"],
        ]
        transactions_2 = [
            ["2020-12-04", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-05", "Tecnologia", "49.99", "AWS"],
            ["2020-12-04", "Jurídico", "60.00", "LinkSquares"],
        ]
        out_1, out_2 = reconcile_accounts(transactions_1, transactions_2)
        self.assertEqual(
            out_1,
            [
                ["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"],
                ["2020-12-05", "Tecnologia", "50.00", "AWS", "MISSING"],
            ],
        )
        self.assertEqual(
            out_2,
            [
                ["2020-12-04", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                ["2020-12-05", "Tecnologia", "49.99", "AWS", "MISSING"],
                ["2020-12-04", "Jurídico", "60.00", "LinkSquares", "FOUND"],
            ],
        )

    def test_date_precedence(self):
        transactions_1 = [
            ["2020-12-01", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-02", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-07", "Tecnologia", "16.00", "Bitbucket"],
        ]
        transactions_2 = [
            ["2020-12-01", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-02", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-11-30", "Tecnologia", "16.00", "Bitbucket"],
            ["2020-12-08", "Tecnologia", "16.00", "Bitbucket"],
        ]
        out_1, out_2 = reconcile_accounts(transactions_1, transactions_2)
        self.assertEqual(
            out_1,
            [
                ["2020-12-01", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                ["2020-12-02", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                ["2020-12-07", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
            ],
        )
        self.assertEqual(
            out_2,
            [
                ["2020-12-01", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                ["2020-12-02", "Tecnologia", "16.00", "Bitbucket", "MISSING"],
                ["2020-11-30", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
                ["2020-12-08", "Tecnologia", "16.00", "Bitbucket", "FOUND"],
            ],
        )


class TestLastLines(unittest.TestCase):
    def test_single_line(self):
        lines = last_lines("test_data/test_single_line.txt")
        self.assertEqual(next(lines), "Single line\n")
        # Assert iterator is finished
        try:
            next(lines)
            self.fail("iterator wasn't finished")
        except StopIteration:
            pass

    def test_multiple_lines(self):
        lines = last_lines("test_data/test_multiple_lines.txt")
        self.assertEqual(next(lines), "And this is line 3\n")
        self.assertEqual(next(lines), "This is line 2\n")
        self.assertEqual(next(lines), "This is a file\n")
        # Assert iterator is finished
        try:
            next(lines)
            self.fail("iterator wasn't finished")
        except StopIteration:
            pass


class TestCachedProperty(unittest.TestCase):
    def test_simple_cache(self):
        class Vector:
            def __init__(self, x, y, z, color=None):
                self.x, self.y, self.z = x, y, z
                self.color = color
                self.magnitude_calls = 0

            @cached_property("x", "y", "z")
            def magnitude(self):
                self.magnitude_calls += 1
                return math.sqrt(self.x**2 + self.y**2 + self.z**2)

        v = Vector(9, 2, 6)
        self.assertEqual(v.magnitude_calls, 0)
        self.assertEqual(v.magnitude, 11.0)
        self.assertEqual(v.magnitude_calls, 1)
        v.color = "red"
        self.assertEqual(v.magnitude, 11.0)
        self.assertEqual(v.magnitude_calls, 1)
        v.y = 18
        self.assertEqual(v.magnitude, 21.0)
        self.assertEqual(v.magnitude_calls, 2)
        self.assertEqual(v.magnitude, 21.0)
        self.assertEqual(v.magnitude_calls, 2)

    def test_multiple_obejcts(self):
        class Vector:
            def __init__(self, x, y, z, color=None):
                self.x, self.y, self.z = x, y, z
                self.color = color
                self.magnitude_calls = 0

            @cached_property("x", "y", "z")
            def magnitude(self):
                self.magnitude_calls += 1
                return math.sqrt(self.x**2 + self.y**2 + self.z**2)

        v1 = Vector(9, 2, 6)
        v2 = Vector(9, 18, 6)
        self.assertEqual(v1.magnitude_calls, 0)
        self.assertEqual(v1.magnitude, 11.0)
        self.assertEqual(v1.magnitude_calls, 1)
        self.assertEqual(v2.magnitude_calls, 0)
        self.assertEqual(v2.magnitude, 21.0)
        self.assertEqual(v2.magnitude_calls, 1)
        self.assertEqual(v1.magnitude_calls, 1)
        v1.x = 0
        v1.y = 3
        v1.z = 4
        self.assertEqual(v1.magnitude, 5.0)
        self.assertEqual(v1.magnitude_calls, 2)
        self.assertEqual(v2.magnitude_calls, 1)
        v2.y = 2
        self.assertEqual(v2.magnitude, 11.0)
        self.assertEqual(v1.magnitude_calls, 2)
        self.assertEqual(v2.magnitude_calls, 2)
