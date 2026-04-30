import time
import bisect

class AdvancedCache:
    def __init__(self):
        self.cache = {}
        self.sorted_items = []  # [(value, key)]

    def add(self, key: str, value: float, expiry: int) -> None:
        if not isinstance(key, str):
            raise ValueError("Key must be string")

        if key in self.cache:
            old_value, _ = self.cache[key]
            self._remove_from_sorted(old_value, key)

        self.cache[key] = (value, expiry)
        bisect.insort(self.sorted_items, (value, key))

    def get(self, key: str):
        now = int(time.time() * 1000)
        item = self.cache.get(key)

        if item is None:
            return None

        value, expiry = item

        if expiry <= now:
            self._remove(key, value)
            return None

        return value

    def evict_expired(self, now: int) -> None:
        to_remove = [
            (key, value)
            for key, (value, expiry) in self.cache.items()
            if expiry <= now
        ]

        for key, value in to_remove:
            self._remove(key, value)

    def weighted_quantile(self, q: float, now: int):
        if not 0 <= q <= 1:
            raise ValueError("q must be between 0 and 1")

        total_weight = 0
        valid = []

        for value, key in self.sorted_items:
            item = self.cache.get(key)
            if item is None:
                continue

            _, expiry = item

            if expiry > now:
                weight = expiry - now
                valid.append((value, weight))
                total_weight += weight

        if total_weight == 0:
            return None

        target = q * total_weight
        cumulative = 0

        for value, weight in valid:
            cumulative += weight
            if cumulative >= target:
                return value

        return valid[-1][0]

    # ---------- helpers ----------

    def _remove(self, key, value):
        self.cache.pop(key, None)
        self._remove_from_sorted(value, key)

    def _remove_from_sorted(self, value, key):
        idx = bisect.bisect_left(self.sorted_items, (value, key))
        if idx < len(self.sorted_items) and self.sorted_items[idx] == (value, key):
            self.sorted_items.pop(idx)