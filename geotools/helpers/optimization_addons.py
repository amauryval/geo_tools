from ..core.geotoolscore import GeoToolsCore

from concurrent.futures import ThreadPoolExecutor


class OptimizationAddons(GeoToolsCore):

    def __init__(self):
        super().__init__()

    def run_threads(self, processes, workers_number=4):

        with ThreadPoolExecutor(max_workers=workers_number) as executor:
            for process in processes:
                if isinstance(process, list):
                    executor.submit(*process)
                else:
                    executor.submit(process)