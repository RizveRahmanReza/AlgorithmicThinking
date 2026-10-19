/**
 * MATH-0003: Amortized Analysis of Dynamic Array Geometric Growth
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Demonstrates: O(1) Amortized Geometric Resizing vs O(N) Arithmetic Degradation
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <stdexcept>
#include <cassert>

struct SimulationMetrics {
    int64_t total_operations;
    int64_t total_copies;
    double amortized_cost_per_op;

    bool operator==(const SimulationMetrics& other) const = default;
};

/**
 * Simulates dynamic array append workload under Geometric Growth (factor 2).
 * Conforms to ISO C++20 standard.
 */
SimulationMetrics simulate_geometric_appends(size_t n) {
    if (n == 0) return {0, 0, 0.0};

    size_t capacity = 1;
    size_t size = 0;
    int64_t total_ops = 0;
    int64_t total_copies = 0;

    for (size_t i = 0; i < n; ++i) {
        if (size == capacity) {
            total_copies += size;
            total_ops += size; // Copy overhead
            capacity *= 2;
        }
        total_ops += 1;
        size += 1;
    }

    return SimulationMetrics{
        .total_operations = total_ops,
        .total_copies = total_copies,
        .amortized_cost_per_op = static_cast<double>(total_ops) / static_cast<double>(n)
    };
}

/**
 * Simulates dynamic array append workload under Arithmetic Growth (+K).
 */
SimulationMetrics simulate_arithmetic_appends(size_t n, size_t k) {
    if (n == 0 || k == 0) return {0, 0, 0.0};

    size_t capacity = k;
    size_t size = 0;
    int64_t total_ops = 0;
    int64_t total_copies = 0;

    for (size_t i = 0; i < n; ++i) {
        if (size == capacity) {
            total_copies += size;
            total_ops += size;
            capacity += k;
        }
        total_ops += 1;
        size += 1;
    }

    return SimulationMetrics{
        .total_operations = total_ops,
        .total_copies = total_copies,
        .amortized_cost_per_op = static_cast<double>(total_ops) / static_cast<double>(n)
    };
}

int main() {
    const size_t N = 100000;

    // Geometric growth should exhibit O(1) amortized cost (< 3.0)
    auto geom = simulate_geometric_appends(N);
    assert(geom.amortized_cost_per_op < 3.0);
    assert(geom.total_operations < 3 * static_cast<int64_t>(N));

    // Arithmetic growth (+100) should exhibit O(N) amortized cost (>> 100)
    auto arith = simulate_arithmetic_appends(N, 100);
    assert(arith.amortized_cost_per_op > 100.0);

    std::cout << "All C++20 assertions for MATH-0003 passed.\n"
              << "Geometric Amortized Cost: " << geom.amortized_cost_per_op << " ops/insert\n"
              << "Arithmetic (+100) Amortized Cost: " << arith.amortized_cost_per_op << " ops/insert" << std::endl;
    return 0;
}
