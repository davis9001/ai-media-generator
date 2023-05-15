import unittest
import video_trailer_clipper_combiner as vtcc

class TestCreateStartTimes(unittest.TestCase):

    def test_one(self):
        self.assertEqual(vtcc.create_start_times(5,60), 
        [0, 9, 19, 8, 38], 
        "Start times array return is broken")

if __name__ == '__main__':
    unittest.main()
