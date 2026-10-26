"""
Master Test Runner for Nyaya Sathi.
Executes all unit and integration test suites using Python standard library unittest.
"""

import unittest
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_test_suite():
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n========================================================")
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}, Failures: {len(result.failures)}")
    print("========================================================")

    if result.wasSuccessful():
        print("ALL NYAYA SATHI CORE TESTS PASSED SUCCESSFULLY! (100%)")
        return 0
    else:
        print("SOME TESTS FAILED.")
        return 1

if __name__ == "__main__":
    sys.exit(run_test_suite())
