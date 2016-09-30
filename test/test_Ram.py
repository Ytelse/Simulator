
import unittest
from Ram import Ram
import numpy as np


class TestRam(unittest.TestCase):
    def setUp(self):
        self.test_matrix = np.array([
                        [1,2,3],
                        [4,5,6],
                        [7,8,9]
                        ])
        
        self.test_vector = np.array([10,11,12,13,14])
        self.write_vector = np.array([15,16,17,18,19])
        
        self.ram = Ram()
        self.matrix_offset = self.ram.add_content(self.test_matrix.flatten())
        self.test_vector_offset = self.ram.add_content(self.test_vector)
        self.write_vector_offset = self.ram.add_content(self.write_vector)

    def test_add_content(self):
        #Test that offset is calculated correct
        self.assertEqual(self.matrix_offset,0)
        self.assertEqual(self.test_vector_offset,9)
        self.assertEqual(self.write_vector_offset,14)
        
        #test that memory elements are placed correctly
        matrix = self.ram.get_values(self.matrix_offset,9)
        self.assertTrue((matrix == np.array([1,2,3,4,5,6,7,8,9])).all())
        matrix = self.ram.get_values(0,19)
        self.assertTrue((matrix == np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])).all())
        vector = self.ram.get_values(9,5)
        self.assertTrue((vector == [10,11,12,13,14]).all())
        vector = self.ram.get_values(14,5)
        self.assertTrue((vector == [15,16,17,18,19]).all())
        
    def test_put_values_1(self):
        self.ram.put_values(self.matrix_offset,np.array([20,21,22,23]))
        self.assertTrue((self.ram.get_values(0,10) == np.array([20,21,22,23,5,6,7,8,9,10])).all())
    
    def test_put_values_2(self):
        self.ram.put_values(self.write_vector_offset,np.array([20,21,22,23]))
        self.assertTrue((self.ram.get_values(self.write_vector_offset,4) == np.array([20,21,22,23])).all())
    
    def test_history_1(self):
        self.assertEqual(self.ram.get_history(),[[]])
        self.ram.get_values(0,9)
        self.ram.put_values(4,[20,21,22,23,24,25,26])
        self.ram.tick()
        self.ram.get_values(9,3)
        self.ram.put_values(5,[27,28,29,30,31,32,33])
        self.assertEqual(self.ram.get_history(),[[("read",0,9),("write",4,7)],[("read",9,3),("write",5,7)]])

    def test_clear_history_1(self):
        self.assertEqual(self.ram.get_history(),[[]])
        self.ram.get_values(0,9)
        self.ram.put_values(4,[20,21,22,23,24,25,26])
        self.ram.tick()
        self.ram.get_values(9,3)
        self.ram.put_values(5,[27,28,29,30,31,32,33])
        self.assertEqual(self.ram.get_history(),[[("read",0,9),("write",4,7)],[("read",9,3),("write",5,7)]])
        
        self.ram.clear_history()
        self.assertEqual(self.ram.get_history(),[[]])


if __name__ == '__main__':
    unittest.main()

