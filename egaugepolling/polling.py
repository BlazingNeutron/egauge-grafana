import sys, time, logging, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from egauge.webapi.device import PhysicalQuantity, Register, UnitSystem
from egauge import webapi
from config import Config
from metrics import Metrics

config = None

def poll_device(device):
    global config
    """Retrieve JSON from an eGauge unit and push values to Prometheus."""
    dev = webapi.device.Device(config.get_url(device["id"]), config.get_token())
    
    # Straight from the eGauge examples - get all registers
    ret = Register(dev, {"rate": "", "time": "now,som"})
    if ret.ts is None:
        logging.fatal(f"Failed to get register data for device: {device['name']}.")

    for regname in ret.regs:
        rate = ret.pq_rate(regname)
        if rate is None:
            logging.fatal(f"Failed to get rate for register {regname}.")
            continue
            #sys.exit(1)

        logging.debug(f"Polling on {device['name']} returned {regname} with {rate.value:12.3f} {rate.unit}")
        for metric in device["metrics"]:
            reg_name = metric["value"]
            if regname == reg_name:
                logging.info(f"Found '{metric['name']}' metric for {device['name']} - set {rate.value}")
                config.get_metrics()[metric["name"]].labels(device["name"]).set(rate.value)
                    

def main_loop(executor):
    futures = {
        executor.submit(poll_device, device)
        for device in config.devices
    }
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as exc:
            logging.error("Unexpected error polling: %s", exc)

    logging.info("Polling complete - sleeping %ss", config.POLL_INTERVAL)
    time.sleep(config.POLL_INTERVAL)

def main():
    global config
    config = Config()

    executor = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)
    while True:
        # TODO check for config changes and reapply
        main_loop(executor)


if __name__ == "__main__":
    main()
