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

## Implementation Approaches

Basic version (simple approach):
I store everything in a dictionary. When I need the quantile, I filter out expired items, calculate weights based on remaining time, sort them, and then find the value using cumulative weights. It’s simple but slower if used frequently.

Bisect version (optimized approach):
I keep the values sorted all the time using a separate list. So instead of sorting during every query, I just scan the sorted data to compute the quantile. This makes queries faster but insertions slightly slower.

difference:
The basic version recomputes everything each time, while the bisect version maintains order to make queries faster.
Basic version has faster inserts (O(1)) but slower queries.
Bisect version has slower inserts (O(n)) but faster repeated queries.
