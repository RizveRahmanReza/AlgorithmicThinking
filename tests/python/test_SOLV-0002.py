"""
Unit Test Suite for Problem SOLV-0002
Tests sweep-line interval resource auditing.
"""

import unittest
from solutions.python.SOLV_0002 import audit_resource_allocation, JobRequest, AllocationAudit


class TestSolv0002(unittest.TestCase):
    def test_standard_feasible(self):
        jobs = [JobRequest(1, 5, 10), JobRequest(2, 8, 4), JobRequest(5, 9, 3)]
        res = audit_resource_allocation(jobs, 15)
        self.assertEqual(res, AllocationAudit(True, 14, None))

    def test_abutting_no_overlap(self):
        jobs = [JobRequest(1, 5, 10), JobRequest(5, 10, 10)]
        res = audit_resource_allocation(jobs, 10)
        self.assertEqual(res, AllocationAudit(True, 10, None))

    def test_capacity_violation(self):
        jobs = [JobRequest(1, 5, 10), JobRequest(2, 6, 5)]
        res = audit_resource_allocation(jobs, 12)
        self.assertEqual(res, AllocationAudit(False, 15, 2))

    def test_invalid_job_bounds_raise(self):
        with self.assertRaises(ValueError):
            audit_resource_allocation([JobRequest(5, 5, 10)], 20)
        with self.assertRaises(ValueError):
            audit_resource_allocation([JobRequest(6, 4, 10)], 20)
        with self.assertRaises(ValueError):
            audit_resource_allocation([JobRequest(1, 5, 0)], 20)

    def test_large_timestamps(self):
        jobs = [JobRequest(0, 10**9, 50), JobRequest(10**9, 2 * 10**9, 50)]
        res = audit_resource_allocation(jobs, 50)
        self.assertEqual(res, AllocationAudit(True, 50, None))


if __name__ == "__main__":
    unittest.main()
