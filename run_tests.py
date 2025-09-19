import unittest
import sys
import os

def run_unit_tests():
    """Run unit tests only"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Load specific unit test modules
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add unit tests
    from tests.test_analyzer import TestMatchAnalyzer
    from tests.test_data_manager import TestDataManager
    from tests.test_riot_api import TestRiotAPI
    from tests.test_visualizer import TestDataVisualizer
    
    suite.addTest(loader.loadTestsFromTestCase(TestMatchAnalyzer))
    suite.addTest(loader.loadTestsFromTestCase(TestDataManager))
    suite.addTest(loader.loadTestsFromTestCase(TestRiotAPI))
    suite.addTest(loader.loadTestsFromTestCase(TestDataVisualizer))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit_code = run_unit_tests()
    sys.exit(exit_code)