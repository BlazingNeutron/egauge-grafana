# eGauge to Grafana

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Collecting eGauge device's instantaneous output into Grafana's powerful Dashboard and reporting capabilities.

This Python code connects eGauge output to Prometheus and Grafana to visualize and record the eGauge output in a more powerful data reporting ecosystem.

This repository contains:

1. Python code to poll eGauge devices and push that data to Prometheus.
2. A docker compose to help setup a production instance.
3. An example of [config.json](config.json) - a file to configure Prometheus metrics and eGauge devices.
4. A mock eGauge device to run against your set up to work out any issues with the rest of the setup.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
    - [Configuration options with config.json](#configuration)
- [License](#license)

## Background

[eGauge](https://www.egauge.net/) devices provide an API to monitor electrical appliances. These devices provide many options for viewing the data provided, however, by exposing the data to Grafana you are provided with many more options.

- Dashboard for multiple devices
- Alerting systems to email, SMS, group chats & more

## Install

This project uses [Python](https://www.python.org/), [eGauge](https://www.egauge.net/)'s python library [egauge-python](https://pypi.org/project/egauge-python/), [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). It is recommended that you start with the [docker-compose.yml](docker/docker-compose.yml) file and expand to suite your needs.

The `docker-compose.yml` provided includes a mock eGauge device.

Get started with the following commands:

```sh
git clone https://github.com/BlazingNeutron/egauge-grafana.git
cd egauge-grafana/docker/
```

Make a copy of the `.env.sample` then start the demo docker compose services.
```sh
cp .env.sample .env
docker compose up
```

## Usage

In this repo's [docker compose](docker/docker-compose.yml) the services are provided and their default ports are:

- [Prometheus](https://prometheus.io/)
- Prometheus' [AlertManager](https://github.com/prometheus/alertmanager)
- [Grafana](https://grafana.com/)
- [InBucket](https://inbucket.org/) - for testing alerts via email
- [Postgres](https://www.postgresql.org/) database
- [Mock eGauge device](tests/mock_egauge_server.py) built into a Docker image
- [eGauge polling service](egaugepolling)

These are the URLs when using the default configuration:

- Prometheus - http://localhost:9090/
- Prometheus' AlertManager - http://localhost:9093/
- Grafana - http://localhost:3000/
- InBucket - http://localhost:9000/
- Mock eGauge device - http://localhost:5000/

### Environment parameters

You can use the sample [`.env.sample`](docker/.env.sample) copied to `.env` file and that will start the debug/demo services. Create or customize your own `.env` with the following parameters.

|Env Param|Description|Default|
|:--------|:----|:----|
|`COMPOSE_PROFILES`|Remove or set to blank to not start Mock eGauge device and InBucket|`debug`|
|`GRAFANA_USER`|Grafana UI Admin username|`admin`|
|`GRAFANA_PASSWORD`|Grafana UI Admin password|`secretpassword`|
|`EGAUGE_USER`|eGauge Device username - from mock device any username will do|`user`|
|`EGAUGE_PASSWORD`|eGauge Device password - mock device ignores this|`password`|
|`GRAFANA_DB_USER`|Grafana Postgres DB username|`grafana`|
|`GRAFANA_DB_PASSWORD`|Grafana Postgres DB password|`grafana`|
|`GRAFANA_PORT`|Grafana Web UI Port #|`3000`|
|`PROMETHEUS_PORT`|Prometheus Web UI Port #|`9090`|
|`ALERT_MANAGER_PORT`|AlertManager Web UI Port #|`9093`|
|`SMTP_PORT`|InBucket SMTP Port #|`2500`|
|`MAIL_UI_PORT`|InBucket Web UI Port #|`9000`|
|`POP3_PORT`|InBucket POP3 Port #|`1100`|


### Config.json Overview

|Property|Description|Example|
|:---:|:------|:---|
|`polling_interval`|How often the eGauge Polling software queries the eGauge CT device in seconds|`5`|
|`workers`|Maximum threads for the eGauge Polling software to run. Should be limited by CPU Cores, polling over network can be a long process|`8`|
|`url`|A URL template which substitues in the device `id`. For example a device with `id` of `egauge000001` and a `"url": "http://{}.local:5000"` will result in a URL to the egauge-python WebAPI of `"http://egauge000001.local:5000"`|`"https://{}.egauge.io/"`|
|`metrics`|Array of JSON Objects describing Prometheus metrics - id, type, name, description and labels are available|See example [metric](#sample-metric)|
|`devices`|Array of JSON Object describing the eGauge CT device and link to `metrics` ids to submit to Prometheus for this device| See example [device](#sample-device)|

### Sample Metric
```json
"metrics": [
    {
        "id": "egauge_voltage",     // Prometheus acceptable metric id
        "type": "gauge",            // Prometheus metric type (Gauge, Counter, etc.)
        "name": "eGauge Voltage",
        "description": "Voltage reading",
        "labels": [
            "device",               // device.name
            "id"                    // device.id
        ]
    },
    ...
],
```
### Sample Device
```json
"devices":[
    {
        "name": "Device 1",
        "id": "egauge000001",
        "metrics": [
            {
                "id": "egauge_voltage",
                "value": "V1"       // eGauge device register type
            },
            {
                "id": "egauge_temperature",
                "value": "temp"
            }
        ]
    },
    ...
],
```

## License

[MIT](LICENSE) Copyright (c) 2026 BlazingNeutron
