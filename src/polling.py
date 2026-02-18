import sys, os, json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from egauge import webapi
from egauge.webapi.device import PhysicalQuantity, Register, UnitSystem

import requests
from prometheus_client import start_http_server, Gauge, Counter

POLL_INTERVAL = 30
MAX_WORKERS = 8
USER = os.environ.get('EGAUGE_USER', "user")
PASSWORD = os.environ.get('EGAUGE_PASSWORD', "fake_password")

METRICS : dict[str, object] = {}

def build_metrics(metrics):
    for metric_def in metrics:
        name = metric_def["name"]
        desc = metric_def["description"]
        labels = metric_def["labels"]
        if metric_def["type"].strip().lower() == "gauge":
            metric = Gauge(name=name, 
                documentation=desc,
                labelnames=labels)
        METRICS[name] = metric

def poll_device(device):
    """Retrieve JSON from an eGauge unit and push values to Prometheus."""
    # TODO device URL changes per device in format http://{device_id}.local/
    dev = webapi.device.Device("http://" + device["id"] + ".local:5000", webapi.JWTAuth(USER, PASSWORD))
    print(device)
    ret = Register(dev, {"rate": "", "time": "now,som"})
    ts = ret.ts
    if ts is None:
        print("Failed to get register data.", file=sys.stderr)
        sys.exit(1)

    for regname in ret.regs:
        line = f"  {regname}"
        if len(line) < 32:
            line += (32 - len(line)) * " "
        rate = ret.pq_rate(regname)
        if rate is None:
            print(f"Failed to get rate for register {regname}.", file=sys.stderr)
            sys.exit(1)
        line += f" {rate.value:12.3f} {rate.unit}"

        for metric in device["metrics"]:
            reg_name = metric["value"]
            if regname == reg_name:
                METRICS[metric["name"]].labels(device["name"]).set(rate.value)
                    
        print(line)


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    
    with open('config.json') as f:
        config = json.load(f)
    
    POLL_INTERVAL = config.get("polling_interval", 30)
    MAX_WORKERS = config.get("workers", 8)
    devices = config["devices"]
    # TODO if devices is null exit
    if devices is None or len(devices) == 0:
        logging.error("You need to config at least one device!")
        sys.exit("No devices found in config.json")
    else:
        print(devices)

    build_metrics(config["metrics"])

    # Start Prometheus
    start_http_server(8000)

    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    while True:
        futures = {
            executor.submit(poll_device, device)
            for device in devices
        }
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                logging.error("Unexpected error polling %s: %s", dev, exc)

        logging.info("Polling complete - sleeping %ss", POLL_INTERVAL)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
