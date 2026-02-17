#!/usr/bin/env python3
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from egauge import webapi
from egauge.webapi.device import PhysicalQuantity, Register, UnitSystem

import requests
from prometheus_client import start_http_server, Gauge, Counter

POLL_INTERVAL = 30
MAX_WORKERS = 8

voltage_gauge = Gauge(
    "egauge_voltage_volts",
    "Voltage reading per phase",
    ["device", "phase"]
)

current_gauge = Gauge(
    "egauge_current_amperes",
    "Current reading per phase",
    ["device", "phase"]
)

power_gauge = Gauge(
    "egauge_power_watts",
    "Real power per phase",
    ["device", "phase"]
)

energy_counter = Gauge(
    "egauge_energy_wh",
    "Cumulative energy (watt-hours)",
    ["device"]
)

def poll_device():
    """Retrieve JSON from an eGauge unit and push values to Prometheus."""
    dev = webapi.device.Device("http://127.0.0.1:5000", webapi.JWTAuth("user", "password"))
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
        if regname == "V1":
            voltage_gauge.labels("device_name1", "phase_id1").set(rate.value)
        if regname == "grid":
            current_gauge.labels("device_name1", "phase_id1").set(rate.value)
        if regname == "temp":
            power_gauge.labels("device_name1", "phase_id1").set(rate.value)
        if regname == "mask":
            energy_counter.labels("device_name1").set(rate.value)
        print(line)


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    # Start Prometheus
    start_http_server(8000)

    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    while True:
        futures = {executor.submit(poll_device)}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                logging.error("Unexpected error polling %s: %s", dev, exc)

        logging.info("Polling complete - sleeping %ss", POLL_INTERVAL)
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()