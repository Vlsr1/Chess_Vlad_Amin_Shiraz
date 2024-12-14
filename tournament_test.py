import unittest
from tournament import calculate_buchholz_and_berger
from tournament import calculate_swiss_rounds


class messageTest(unittest.TestCase):
    
    def test_1(self):
        self.assertEqual(calculate_swiss_rounds(2),1)

    def test_2(self):
        self.assertEqual(calculate_swiss_rounds(3),3)

    def test_3(self):
        self.assertEqual(calculate_swiss_rounds(5),4)

    def test_4(self):
        self.assertEqual(calculate_swiss_rounds(8191),15)

    def test_5(self):
        self.assertEqual(calculate_swiss_rounds(1024),12)

    def test_6(self):
        self.assertEqual(calculate_swiss_rounds(100000),19)
   
    def test_7(self):
        self.assertEqual(calculate_swiss_rounds(100000100000100000),59)

    def test_invalid_input_1(self):
        with self.assertRaises(ValueError) as context:
            calculate_swiss_rounds(1)
        self.assertEqual(str(context.exception), "В турнире не может быть менее 2 участников")

    def test_invalid_input_2(self):
        with self.assertRaises(ValueError) as context:
            calculate_swiss_rounds('c')
        self.assertEqual(str(context.exception), "Неправильный формат ввода")

    def test_invalid_input_3(self):
        with self.assertRaises(ValueError) as context:
            calculate_swiss_rounds(1.13)
        self.assertEqual(str(context.exception), "Неправильный формат ввода")


if __name__ == "__main__":
    unittest.main()