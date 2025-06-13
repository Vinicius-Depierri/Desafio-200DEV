# Monitoring & Observability Test

Welcome! This test is designed to evaluate your understanding of monitoring and observability practices using real applications and common open-source tools (Prometheus, Grafana, Loki, and Tempo).  
The goal is not to assess development skills, but your ability to connect and validate logs, metrics, and traces across a running stack.

---

## Objective

Your mission is to validate whether all observability signals (metrics, logs, traces) are being correctly generated, collected, and exposed for monitoring through Grafana.

---

## System Overview

### `app_a`
- A simple Flask application exposing:
  - `GET /health` → responds with `{"status": "UP"}`
  - `GET /metrics` → exposes Prometheus metrics
- Writes logs to a file: `/app/app.log`
- Instrumented with:
  - Prometheus metrics (`http_requests_total`)
  - OpenTelemetry Tracing (`service.name = app_a`)

### `app_b`
- A Flask application that:
  - Exposes `GET /` → makes an HTTP call to `app_a:/health`
  - Traces the outgoing request using OpenTelemetry (`service.name = app_b`)

Trace Export (app_a / app_b)
Both applications (app_a and app_b) are instrumented with OpenTelemetry and are configured to send their traces to Tempo using the following OTLP HTTP endpoint:

`http://tempo:4318/v1/traces`

---

## Observability Pipeline

| Signal     | From      | Collected by        | Viewed in Grafana via |
|------------|-----------|---------------------|------------------------|
| Metrics    | app_a, app_b | Prometheus         | Dashboards / Explore   |
| Logs       | app_a (file) | Grafana Alloy → Loki | Explore (Loki)         |
| Traces     | app_a, app_b     | OpenTelemetry → Tempo | Explore (Tempo)        |

---

## Tasks

Using **Docker Compose**, bring up the following observability components:

* **Prometheus**
* **Grafana**
* **Loki**
* **Alloy** (or **Fluent Bit**, if preferred)
* **Tempo**

The applications `app_a` and `app_b` are already instrumented to emit metrics, logs, and traces — your responsibility is to ensure that the infrastructure is up and running and that these signals are correctly visualized in Grafana.

Validation checklist:


- Launch the environment using Docker Compose
- Access `app_b` via `http://localhost:8081/`

In Grafana, confirm that:

  - Metrics from both apps are visible (via Prometheus)
  - Logs from `app_a` are visible (via Loki)
  - Traces from `app_a` and `app_b` are visible (via Tempo)

---

## Test Validation Criteria

This test is considered successful when you:
- Demonstrate that observability signals are available and correctly correlated
- Show ability to troubleshoot and verify signal ingestion
- Use Grafana Explore effectively for each signal type

---

Good luck and enjoy the test!