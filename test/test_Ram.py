
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
        
    def test_put_values(self):
        pass
    
    
    def test_tick(self):
        pass
    
    def test_history(self):
        pass


if __name__ == '__main__':
    unittest.main()

