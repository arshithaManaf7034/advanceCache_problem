# AdvancedCache – Design & Implementation Notes

##  Objective

Implement a cache system that:

* Stores up to **200,000 key–value pairs**
* Supports **expiry (TTL-based eviction)**
* Provides **weighted quantile queries** based on remaining time-to-live

Each entry is stored as:

```
(key, value, expiry)
```

Weight used in quantile calculation:

```
weight = expiry - now
```

---

## ⚙️ Implementation Approaches

###  1. Basic Version (Sort on Query)

#### Approach

* Use a dictionary:

```
self.cache = { key: (value, expiry) }
```

* For `weighted_quantile(q, now)`:

  1. Filter non-expired items
  2. Compute weights
  3. Sort values
  4. Use cumulative weights to find quantile

#### Complexity

* add → O(1)
* get → O(1)
* evict_expired → O(n)
* weighted_quantile → O(n log n)

#### Pros

* Simple and easy to implement
* Clean logic
* Good for interviews (first approach)

#### Cons

* Sorting every query is expensive
* Not suitable for frequent quantile calls

#### Best Use Case

* When quantile queries are **rare**
* When simplicity is preferred

---

###  2. Optimized Version (Bisect + Sorted Structure)

#### Approach

Maintain two structures:

```
self.cache         # key → (value, expiry)
self.sorted_items  # sorted list of (value, key)
```

* Use `bisect.insort()` to maintain sorted order
* Remove elements using binary search (`bisect_left`)
* Avoid sorting during queries

#### Complexity

* add → O(n)
* get → O(1)
* evict_expired → O(n)
* weighted_quantile → O(n)

#### Pros

* Faster quantile queries (no sorting needed)
* Better for read-heavy workloads
* More efficient for repeated queries

#### Cons

* Insert/delete operations are slower (due to list shifting)
* More complex code
* Must maintain consistency between structures

#### Best Use Case

* When quantile is called **frequently**
* When performance matters more than simplicity

---

## 🔍 Key Design Difference

Basic approach:

```
Recompute everything during each query
```

Bisect approach:

```
Maintain sorted structure continuously for faster queries
```

---

## Trade-off Summary

| Feature          | Basic Version | Bisect Version |
| ---------------- | ------------- | -------------- |
| Insert speed     | Fast O(1)     | Slower O(n)    |
| Query speed      | Slow          | Faster         |
| Code complexity  | Low           | Medium         |
| Sorting overhead | Every query   | None           |

---

## When to Use Which?

* Use **Basic Version**:

  * When queries are infrequent
  * When implementing quickly (interview first pass)

* Use **Bisect Version**:

  * When queries are frequent
  * When optimizing performance

---





## Key Learnings

* Hash map for fast lookup
* Handling time-based expiration
* Weighted statistics (quantiles)
* Trade-offs between simplicity and performance
* Maintaining auxiliary data structures for optimization

---

##  Conclusion

* Basic version → best for simplicity and clarity
* Bisect version → better for performance and frequent queries
