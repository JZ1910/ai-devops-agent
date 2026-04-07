from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter("app_requests_total", "Total number of app requests")
HEALTH_CHECK_COUNT = Counter("app_health_checks_total", "Total number of health checks")

app_failed = False


@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({"message": "AI DevOps demo app is running"})


@app.route("/health")
def health():
    global app_failed
    HEALTH_CHECK_COUNT.inc()

    if app_failed:
        return jsonify({"status": "unhealthy"}), 500

    return jsonify({"status": "healthy"})


@app.route("/fail")
def fail():
    global app_failed
    app_failed = True
    return jsonify({"message": "App has been set to unhealthy mode"})


@app.route("/recover")
def recover():
    global app_failed
    app_failed = False
    return jsonify({"message": "App has been set back to healthy mode"})


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)