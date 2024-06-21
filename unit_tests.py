import unittest

from utils import find_first_diff

class TestStringDiff(unittest.TestCase):

    def test_find_first_diff(self):
        a = "hello"
        b = "hello world"
        index = find_first_diff(a, b)
        self.assertEqual(index, 5)

        a = "hello world"
        b = "hello"
        index = find_first_diff(a, b)
        self.assertEqual(index, 11)

        a = "hello sam"
        b = "hello sal"
        index = find_first_diff(a, b)
        self.assertEqual(index, 8)

        a = ""
        b = "hello"
        index = find_first_diff(a, b)
        self.assertEqual(index, 0)

        a = "hello"
        b = ""
        index = find_first_diff(a, b)
        self.assertEqual(index, 5)


if __name__ == '__main__':
    unittest.main()