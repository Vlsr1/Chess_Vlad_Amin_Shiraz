import unittest
from chess_notchess import is_basic_valid_move


class messageTest(unittest.TestCase):
    
    def test_1(self):
        self.assertEqual(is_basic_valid_move('P',(3,6),(3,4),'White'),True)

    def test_2(self):     
        self.assertEqual(is_basic_valid_move('P',(3,6),(3,3),'White'),False)

    def test_3(self):     
        self.assertEqual(is_basic_valid_move('p',(3,6),(3,3),'Black'),False)

    def test_4(self):     
        self.assertEqual(is_basic_valid_move('p',(3,6),(1,3),'Black'),False)

    def test_5(self):
        self.assertEqual(is_basic_valid_move('q',(1,6),(3,4),'Black'),True)

    def test_6(self):
        self.assertEqual(is_basic_valid_move('q',(6,6),(6,5),'Black'),True)

    def test_6(self):
        self.assertEqual(is_basic_valid_move('N',(5,6),(6,4),'White'),True)




if __name__ == "__main__":
    unittest.main()