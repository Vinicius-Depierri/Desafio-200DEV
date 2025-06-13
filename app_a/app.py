from flask import Flask, jsonify
from prometheus_client import start_http_server, Counter, generate_latest
import logging
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "app_a"})
    )
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://tempo:4318/v1/traces"))
)

REQUEST_COUNT = Counter('http_requests_total', 'total of requests received', ['method'])

log_folder = '/app'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig(
    filename=os.path.join(log_folder, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET').inc()
    app.logger.info('Health check called')
    return jsonify(status="UP")

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)