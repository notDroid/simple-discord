import asyncio

class Metrics:
    def __init__(self):
        self.requests = 0
        self.errors = 0
        self.latencies = []
        self.action_counts = {}

    def record(self, action: str, latency: float, error: bool = False, error_type: str = None):
        self.requests += 1
        if error:
            self.errors += 1
        else:
            self.latencies.append(latency)
        
        self.action_counts[action] = self.action_counts.get(action, 0) + 1

    def summary(self):
        print(f"\n--- Results ---")
        print(f"Total Requests: {self.requests}")
        print(f"Total Errors:   {self.errors}")
        print("Actions:", self.action_counts)

class SafeMetrics:
    """Wraps the Metrics data class with a lock for concurrent workers."""
    def __init__(self):
        self._metrics = Metrics()
        self._lock = asyncio.Lock()

    async def record(self, action: str, latency: float, error: bool = False):
        async with self._lock:
            self._metrics.record(action, latency, error)

    async def get_summary_str(self) -> str:
        async with self._lock:
            m = self._metrics
            avg_lat = (sum(m.latencies) / len(m.latencies)) if m.latencies else 0
            return (
                f"Requests: {m.requests} | "
                f"Errors: {m.errors} | "
                f"Avg Latency: {avg_lat:.4f}s"
            )
            
    async def final_report(self):
        async with self._lock:
            print("\n=== FINAL METRICS ===")
            print(f"Total Requests: {self._metrics.requests}")
            print(f"Total Errors:   {self._metrics.errors}")
            print("Action Breakdown:")
            for act, count in self._metrics.action_counts.items():
                print(f"  - {act}: {count}")