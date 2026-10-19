/**
 * HASH-0001: Cache-Conscious Flat Hash Map with Linear Probing
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: Expected O(1) Time, O(N) Contiguous Space
 * Features: SplitMix64 Bit-Mixer, Power-of-Two Masking, Tombstone Recycling
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <optional>
#include <cassert>

namespace alg {

enum class SlotState : uint8_t {
    EMPTY = 0,
    OCCUPIED = 1,
    TOMBSTONE = 2
};

struct Entry {
    int64_t key{0};
    int64_t value{0};
    SlotState state{SlotState::EMPTY};
};

/**
 * High-Entropy SplitMix64 Bit-Mixer.
 */
constexpr uint64_t splitmix64(uint64_t x) noexcept {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

/**
 * Cache-Conscious Flat Hash Map using Open Addressing with Linear Probing.
 * Standard: ISO C++20.
 */
class FlatHashMap {
public:
    explicit FlatHashMap(size_t initial_capacity = 8) 
        : capacity_(next_power_of_two(initial_capacity)), size_(0), tombstone_count_(0) {
        table_.resize(capacity_);
    }

    bool insert(int64_t key, int64_t value) {
        if (static_cast<double>(size_ + tombstone_count_ + 1) / capacity_ > MAX_LOAD_FACTOR) {
            rehash(capacity_ * 2);
        }

        const size_t mask = capacity_ - 1;
        size_t idx = splitmix64(static_cast<uint64_t>(key)) & mask;
        std::optional<size_t> first_tombstone = std::nullopt;

        while (table_[idx].state != SlotState::EMPTY) {
            if (table_[idx].state == SlotState::OCCUPIED) {
                if (table_[idx].key == key) {
                    table_[idx].value = value; // Update existing key
                    return false;
                }
            } else if (table_[idx].state == SlotState::TOMBSTONE && !first_tombstone.has_value()) {
                first_tombstone = idx;
            }
            idx = (idx + 1) & mask;
        }

        // Write new key into first encountered tombstone (recycled) or empty slot
        size_t target_slot = first_tombstone.value_or(idx);
        if (table_[target_slot].state == SlotState::TOMBSTONE) {
            --tombstone_count_;
        }
        table_[target_slot].key = key;
        table_[target_slot].value = value;
        table_[target_slot].state = SlotState::OCCUPIED;
        ++size_;
        return true;
    }

    std::optional<int64_t> get(int64_t key) const noexcept {
        const size_t mask = capacity_ - 1;
        size_t idx = splitmix64(static_cast<uint64_t>(key)) & mask;

        while (table_[idx].state != SlotState::EMPTY) {
            if (table_[idx].state == SlotState::OCCUPIED && table_[idx].key == key) {
                return table_[idx].value;
            }
            idx = (idx + 1) & mask;
        }
        return std::nullopt;
    }

    bool remove(int64_t key) noexcept {
        const size_t mask = capacity_ - 1;
        size_t idx = splitmix64(static_cast<uint64_t>(key)) & mask;

        while (table_[idx].state != SlotState::EMPTY) {
            if (table_[idx].state == SlotState::OCCUPIED && table_[idx].key == key) {
                table_[idx].state = SlotState::TOMBSTONE;
                --size_;
                ++tombstone_count_;
                return true;
            }
            idx = (idx + 1) & mask;
        }
        return false;
    }

    size_t size() const noexcept { return size_; }
    size_t capacity() const noexcept { return capacity_; }

private:
    static constexpr double MAX_LOAD_FACTOR = 0.70;
    size_t capacity_;
    size_t size_;
    size_t tombstone_count_;
    std::vector<Entry> table_;

    static size_t next_power_of_two(size_t v) noexcept {
        size_t p = 1;
        while (p < v) p <<= 1;
        return (p < 8) ? 8 : p;
    }

    void rehash(size_t new_capacity) {
        std::vector<Entry> old_table = std::move(table_);
        capacity_ = new_capacity;
        size_ = 0;
        tombstone_count_ = 0;
        table_.assign(capacity_, Entry{});

        for (const auto& entry : old_table) {
            if (entry.state == SlotState::OCCUPIED) {
                insert(entry.key, entry.value);
            }
        }
    }
};

} // namespace alg

int main() {
    alg::FlatHashMap map(4);

    // Collision pair on small capacity
    assert(map.insert(5, 100) == true);
    assert(map.insert(9, 200) == true);
    assert(map.insert(5, 150) == false); // Update existing
    assert(map.size() == 2);

    assert(map.get(5).value() == 150);
    assert(map.get(9).value() == 200);

    // Tombstone deletion
    assert(map.remove(5) == true);
    assert(!map.get(5).has_value());
    assert(map.get(9).value() == 200); // Verify probe past tombstone

    // Reinsertion recycling tombstone
    assert(map.insert(13, 300) == true);
    assert(map.get(13).value() == 300);

    // Capacity growth across 50 elements
    for (int i = 0; i < 50; ++i) {
        map.insert(i * 100, i);
    }
    for (int i = 0; i < 50; ++i) {
        assert(map.get(i * 100).value() == i);
    }

    std::cout << "All C++20 assertions for HASH-0001 passed successfully." << std::endl;
    return 0;
}
