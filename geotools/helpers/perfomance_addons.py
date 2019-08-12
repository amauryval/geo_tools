
from concurrent.futures import ThreadPoolExecutor


class PerformanceAddons:
    """
    Class : PerformanceAddons
    """

    def run_with_threads(self, runners, threads_count=4):
        with ThreadPoolExecutor(max_workers=threads_count) as exec:
            for runner in runners:
                if isinstance(runner, list):
                    exec.submit(*runner)
                else:
                    exec.submit(runner)
