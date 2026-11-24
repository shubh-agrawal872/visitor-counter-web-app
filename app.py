import os
import socket
import time
import math
from flask import Flask, render_template_string, jsonify, request
import redis

app = Flask(__name__)

# Configuration from Environment Variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
ENVIRONMENT = os.getenv("ENVIRONMENT", "Local Development")
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "Cluster-Default")
COLOR_THEME = os.getenv("COLOR_THEME", "#2563eb") # Default blue

# Redis Connection with Retry
def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2
    )

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Visitor Counter - {{ environment }}</title>
    <style>
        :root {
            --primary: {{ theme_color }};
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --success: #10b981;
            --warning: #f59e0b;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }
        .container {
            width: 100%;
            max-width: 720px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }
        .header {
            padding: 2rem;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
            border-bottom: 1px solid var(--border);
            text-align: center;
            position: relative;
        }
        .badge {
            display: inline-block;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background-color: {{ theme_color }};
            color: #ffffff;
            margin-bottom: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
        }
        h1 {
            font-size: 1.85rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            color: var(--text-muted);
            font-size: 0.95rem;
        }
        .counter-section {
            padding: 2.5rem 2rem;
            text-align: center;
            border-bottom: 1px solid var(--border);
        }
        .counter-label {
            font-size: 1rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.75rem;
        }
        .counter-value {
            font-size: 4.5rem;
            font-weight: 800;
            color: #38bdf8;
            text-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
            line-height: 1;
        }
        .details-grid {
            padding: 1.5rem 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.25rem;
        }
        .detail-item {
            background: rgba(15, 23, 42, 0.6);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        .detail-item .label {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }
        .detail-item .value {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-main);
            word-break: break-all;
        }
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            margin-right: 6px;
        }
        .footer {
            padding: 1.25rem 2rem;
            background: rgba(15, 23, 42, 0.8);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: var(--text-muted);
        }
        .actions {
            display: flex;
            gap: 0.5rem;
        }
        .btn {
            background: var(--border);
            color: var(--text-main);
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            font-size: 0.8rem;
            transition: all 0.2s ease;
        }
        .btn:hover {
            background: #475569;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="badge">{{ environment }}</div>
            <h1>Cloud Computing Visitor Counter</h1>
            <p class="subtitle">Distributed High-Availability Architecture with Docker, Kubernetes & Failover</p>
        </div>

        <div class="counter-section">
            <div class="counter-label">Total Visits Tracked in Redis</div>
            <div class="counter-value">{{ count }}</div>
        </div>

        <div class="details-grid">
            <div class="detail-item">
                <div class="label">Pod Hostname</div>
                <div class="value">{{ hostname }}</div>
            </div>
            <div class="detail-item">
                <div class="label">Pod / Host IP</div>
                <div class="value">{{ pod_ip }}</div>
            </div>
            <div class="detail-item">
                <div class="label">Active Cluster</div>
                <div class="value">{{ cluster_name }}</div>
            </div>
            <div class="detail-item">
                <div class="label">Redis Backend Status</div>
                <div class="value">
                    <span class="status-dot"></span>{{ redis_status }}
                </div>
            </div>
        </div>

        <div class="footer">
            <span>Flask v3.0.3 + Redis v7.2</span>
            <div class="actions">
                <a href="/stress?duration=2" class="btn" title="Simulate CPU spike for HPA verification">Trigger CPU Spike</a>
                <a href="/healthz" class="btn" target="_blank">Health Check</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    hostname = socket.gethostname()
    try:
        pod_ip = socket.gethostbyname(hostname)
    except Exception:
        pod_ip = "127.0.0.1"

    count = 0
    redis_status = "Connected"
    try:
        r = get_redis_client()
        count = r.incr("visitor_count")
    except Exception as e:
        count = "Unavailable (Redis connection failed)"
        redis_status = f"Error: {str(e)[:25]}"

    return render_template_string(
        HTML_TEMPLATE,
        count=count,
        hostname=hostname,
        pod_ip=pod_ip,
        environment=ENVIRONMENT,
        cluster_name=CLUSTER_NAME,
        redis_status=redis_status,
        theme_color=COLOR_THEME
    )

@app.route("/healthz")
def healthz():
    """Liveness and Readiness probe endpoint for Kubernetes and Failover Controller."""
    try:
        r = get_redis_client()
        r.ping()
        return jsonify({
            "status": "healthy",
            "cluster": CLUSTER_NAME,
            "environment": ENVIRONMENT,
            "hostname": socket.gethostname(),
            "timestamp": time.time()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "cluster": CLUSTER_NAME,
            "environment": ENVIRONMENT
        }), 503

@app.route("/api/count")
def api_count():
    try:
        r = get_redis_client()
        count = r.get("visitor_count") or 0
        return jsonify({"visitor_count": int(count)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stress")
def stress():
    """
    CPU load endpoint to test Kubernetes Horizontal Pod Autoscaler (HPA).
    Generates intensive computation for the specified duration (default: 3 seconds).
    """
    duration = float(request.args.get("duration", 3.0))
    # Cap duration at 10 seconds per request to prevent accidental denial of service
    duration = min(duration, 10.0)
    end_time = time.time() + duration
    iterations = 0
    while time.time() < end_time:
        # CPU-intensive calculation
        _ = math.sqrt(math.factorial(150))
        iterations += 1

    return jsonify({
        "message": "CPU stress simulation completed",
        "duration_seconds": duration,
        "iterations": iterations,
        "hostname": socket.gethostname()
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
