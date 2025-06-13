import requests
from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource

# Configure tracing BEFORE instrumenting the app
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "app_b"})
    )
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://tempo:4318/v1/traces"))
)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)  # <- only after provider is set

tracer = trace.get_tracer(__name__)

@app.route('/')
def call_api_a():
    with tracer.start_as_current_span("call_to_app_a"):
        response = requests.get('http://app_a:8080/health')
        return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
