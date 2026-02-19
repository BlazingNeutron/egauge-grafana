import logging, os, json
from prometheus_client import start_http_server
from egauge import webapi
from metrics import Metrics


class Config:
    POLL_INTERVAL = 30
    MAX_WORKERS = 8
    __USER = os.environ.get("EGAUGE_USER", "user")
    __PASSWORD = os.environ.get("EGAUGE_PASSWORD", "fake_password")
    __token = None
    devices = None
    __metrics = None

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
        )

        with open("config.json") as f:
            config = json.load(f)

        self.POLL_INTERVAL = config.get("polling_interval", 30)
        self.MAX_WORKERS = config.get("workers", 8)
        self.devices = config["devices"]

        if self.devices is None or len(self.devices) == 0:
            logging.fatal("You need to config at least one device!")
            sys.exit("No devices found in config.json")

        metricsConfig = config["metrics"]
        if metricsConfig is None or len(metricsConfig) == 0:
            logging.fatal("You need to config at least one metric!")
            sys.exit("No metrics found in config.json")
        self.__metrics = Metrics()
        self.__metrics.build_metrics(config["metrics"])

        # Start Prometheus
        start_http_server(8000)

    def get_token(self):
        if self.__token is None:
            self.__token = webapi.JWTAuth(self.__USER, self.__PASSWORD)
        return self.__token

    def get_metrics(self) -> dic[str, object]:
        return self.__metrics.get_metrics()

    def get_url(self, id):
        # TODO make this a config.json prop
        return f"http://{id}.local:5000"
