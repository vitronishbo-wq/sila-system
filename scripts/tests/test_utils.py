import unittest


def multiply(a, b):
    return a * b


class TestUtils(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(0, 5), 0)


if __name__ == "__main__":
    unittest.main()
