import time

class AdvancedCache:
    def __init__(self):
        self.cache = {}

    def add(self, key: str, value: float, expiry: int) -> None:
        if not isinstance(key, str):
            raise ValueError("Key must be string")
        self.cache[key] = (value, expiry)

    def get(self, key: str):
        now = int(time.time() * 1000)
        item = self.cache.get(key)

        if item is None:
            return None

        value, expiry = item

        if expiry <= now:
            self.cache.pop(key, None)
            return None

        return value

    def evict_expired(self, now: int) -> None:
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if expiry <= now
        ]

        for key in expired_keys:
            del self.cache[key]

    def weighted_quantile(self, q: float, now: int):
        # collect valid (value, weight)
        items = []
        for value, expiry in self.cache.values():
            if expiry > now:
                weight = expiry - now
                items.append((value, weight))

        # no valid items
        if not items:
            return None

        # sort by value
        items.sort(key=lambda x: x[0])

        # total weight
        total_weight = sum(weight for _, weight in items)

        target = q * total_weight

        cumulative = 0

        for value, weight in items:
            cumulative += weight
            if cumulative >= target:
                return value

        return items[-1][0]  # fallback


# TESTING
if __name__ == "__main__":
    cache = AdvancedCache()

    now = int(time.time() * 1000)

    # Test add + get
    cache.add("a", 10.5, now + 5000)
    cache.add("b", 20.3, now - 1000)

    print("get(a):", cache.get("a"))  # 10.5
    print("get(b):", cache.get("b"))  # None

    # Test eviction
    cache.cache = {
        "a": (10.0, 100),
        "b": (20.0, 200),
        "c": (30.0, 300),
    }

    cache.evict_expired(200)
    print("after eviction:", cache.cache)  # {'c': (30.0, 300)}

    
    cache.cache = {
        "a": (10.0, 200),
        "b": (20.0, 150),
        "c": (30.0, 110),
    }

    now = 100

    print("q=0.5:", cache.weighted_quantile(0.5, now))  # ~10
    print("q=0.8:", cache.weighted_quantile(0.8, now))  # ~20
