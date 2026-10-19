"""
Unit Test Suite for Problem MATH-0003
Validates amortized cost metrics for geometric vs arithmetic resizing.
"""

import unittest
from solutions.python.MATH_0003 import simulate_geometric_appends, simulate_arithmetic_appends


class TestMath0003(unittest.TestCase):
    def test_geometric_amortized_bound(self):
        # Amortized cost for geometric growth factor 2 must be strictly < 3.0
        for n in [10, 100, 1000, 50000]:
            metrics = simulate_geometric_appends(n)
            self.assertLess(metrics.amortized_cost_per_op, 3.0)
            self.assertLess(metrics.total_operations, 3 * n)

    def test_arithmetic_degradation(self):
        # With K = 10 and N = 10000, arithmetic cost per operation should explode
        metrics = simulate_arithmetic_appends(10000, 10)
        self.assertGreater(metrics.amortized_cost_per_op, 100.0)

    def test_boundary_zero_and_negative(self):
        self.assertEqual(simulate_geometric_appends(0).total_operations, 0)
        self.assertEqual(simulate_arithmetic_appends(0, 10).total_operations, 0)
        self.assertEqual(simulate_arithmetic_appends(100, 0).total_operations, 0)


if __name__ == "__main__":
    unittest.main()
