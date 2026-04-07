import time
import requests
import subprocess
from datetime import datetime

BASE_URL = "http://127.0.0.1:50335"   # ✅ UPDATED
HEALTH_URL = f"{BASE_URL}/health"
METRICS_URL = f"{BASE_URL}/metrics"

CHECK_INTERVAL = 10  # seconds


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def check_health() -> bool:
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "healthy"
        return False
    except Exception as e:
        log(f"Health check error: {e}")
        return False


def fetch_metrics() -> str:
    try:
        response = requests.get(METRICS_URL, timeout=5)
        if response.status_code == 200:
            return response.text
        return ""
    except Exception as e:
        log(f"Metrics fetch error: {e}")
        return ""


def get_pod_name():
    try:
        result = subprocess.run(
            [
                "kubectl",
                "get",
                "pods",
                "-l",
                "app=ai-devops-app",
                "-o",
                "jsonpath={.items[0].metadata.name}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        pod_name = result.stdout.strip()
        return pod_name if pod_name else None
    except subprocess.CalledProcessError as e:
        log(f"Error getting pod name: {e.stderr}")
        return None


def restart_pod():
    pod_name = get_pod_name()
    if not pod_name:
        log("No pod found to restart.")
        return

    try:
        log(f"Deleting pod: {pod_name}")
        subprocess.run(
            ["kubectl", "delete", "pod", pod_name],
            check=True,
            capture_output=True,
            text=True,
        )
        log("✅ Recovery action executed: unhealthy pod deleted.")
        log("🚀 Kubernetes will recreate the pod automatically.")
    except subprocess.CalledProcessError as e:
        log(f"Failed to delete pod: {e.stderr}")


def decide_action(is_healthy: bool, metrics_text: str) -> str:
    if not is_healthy:
        return "restart_pod"

    if "app_requests_total" in metrics_text:
        return "do_nothing"

    return "inspect_metrics"


def execute_action(action: str):
    if action == "restart_pod":
        log("⚠️ Decision: restart_pod")
        restart_pod()
    elif action == "inspect_metrics":
        log("⚠️ Decision: inspect_metrics")
        log("Metrics endpoint needs inspection.")
    else:
        log("✅ Decision: do_nothing")
        log("System healthy. No action needed.")


def run_agent():
    log("🤖 AI DevOps agent started.")
    while True:
        log("Checking application health...")
        healthy = check_health()
        metrics = fetch_metrics()
        action = decide_action(healthy, metrics)
        execute_action(action)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run_agent()