from prometheus_client import Gauge, Counter

class Metrics:
    __METRICS : dict[str, object] = {}

    def __init__(self):
        self.__METRICS = {}

    def build_metrics(self, metrics):
        for metric_def in metrics:
            name = metric_def["name"]
            desc = metric_def["description"]
            labels = metric_def["labels"]
            metric = None
            if metric_def["type"].strip().lower() == "gauge":
                metric = Gauge(name=name, 
                    documentation=desc,
                    labelnames=labels)
            if metric_def["type"].strip().lower() == "counter":
                metric = Counter(name=name, 
                    documentation=desc,
                    labelnames=labels)
            if metric is not None:
                self.__METRICS[name] = metric
    
    def get_metrics(self) -> dict[str, object]:
        return self.__METRICS