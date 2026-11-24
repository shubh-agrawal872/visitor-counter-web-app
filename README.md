# Cloud Computing Project: Distributed Visitor Counter Web App (Flask + Redis)

> **Complete Project Implementation: Docker, Kubernetes, HPA Autoscaling, Hybrid Cloud Failover, and Cost Optimization**

---

## Project Structure Overview

```text
cloud project/
├── app.py                      # Flask Application with Redis, Health Checks & Stress Testing
├── requirements.txt            # Python dependencies (Flask, Redis, Gunicorn, Requests)
├── Dockerfile                  # Optimized lightweight multi-stage Dockerfile (python:3.11-slim)
├── .dockerignore               # Docker build exclusions
├── docker-compose.yml          # Multi-container orchestration (Flask + Redis)
├── k8s.yaml                    # Full Kubernetes Manifest (Namespace, ConfigMap, Deployments, Services)
├── hpa.yaml                    # HorizontalPodAutoscaler (50% CPU threshold, 2-10 replicas)
├── github_link.txt             # Public GitHub repository submission placeholder
├── ARCHITECTURE.md             # Detailed Mermaid Architecture & Flowchart Diagrams
├── COST_OPTIMIZATION_ANALYSIS.md# Cost comparison table & 3 optimization techniques
├── SCREENSHOTS_GUIDE.md        # Exact commands and outputs for all required screenshots
├── PROJECT_REPORT.md           # Full Academic Project Report & Submission Document
├── hybrid-cloud/
│   ├── onprem-cluster.yaml     # Cluster 1: On-Premises Primary Kubernetes Manifest
│   ├── cloud-cluster.yaml      # Cluster 2: Public Cloud Secondary Failover Manifest
│   ├── failover_proxy.py       # Automated intelligent failover reverse-proxy controller
│   └── nginx-failover.conf     # Nginx active-passive failover configuration
└── scripts/
    ├── deploy_single_cluster.bat / .sh  # Automated single cluster deploy & build script
    ├── simulate_hybrid_cloud.bat / .sh  # Dual Minikube hybrid cloud simulation script
    ├── load_test.py                     # Multi-threaded concurrent HPA CPU stress test
    └── test_self_healing.bat / .sh      # Pod deletion & automatic self-healing validation
```

---

## Quick Start Guide

### 1. Prerequisites
Install the following free tools on your machine:
- **Docker Desktop** (or Docker Engine)
- **Minikube**
- **kubectl**
- **Python 3.10+**

### 2. Task 1: Test with Docker & Docker Compose
```bash
# Start Flask + Redis locally with Docker Compose
docker compose up -d

# Check status
docker compose ps

# Open browser at http://localhost:5000
# To tear down:
docker compose down
```

### 3. Task 2 & 3: Deploy to Kubernetes with HPA
```bash
# Windows:
scripts\deploy_single_cluster.bat

# Linux / Mac:
chmod +x scripts/*.sh
./scripts/deploy_single_cluster.sh
```
Or manually run:
```bash
minikube start --driver=docker
minikube addons enable metrics-server
eval $(minikube docker-env) # or: minikube docker-env | Invoke-Expression in PowerShell
docker build -t visitor-counter-web:latest .
kubectl apply -f k8s.yaml
kubectl apply -f hpa.yaml
```

To test HPA under load:
```bash
# In Terminal 1: Watch HPA
kubectl get hpa -n visitor-counter -w

# In Terminal 2: Run load generator
python scripts/load_test.py
```

### 4. Task 4: Hybrid Cloud Simulation with Failover
```bash
# Run simulation setup script
scripts\simulate_hybrid_cloud.bat
```
Run the automated failover controller:
```bash
python hybrid-cloud/failover_proxy.py
```
Open `http://127.0.0.1:8080`. Notice the badge `🏢 On-Premises Private Cloud (Primary)`.  
Pause the primary cluster:
```bash
minikube pause -p onprem-cluster
```
Refresh `http://127.0.0.1:8080`. The traffic instantly routes to `☁️ Public Cloud AWS / GCP (Secondary / Failover)` without downtime!

---

## Submission Checklist

- [x] **Source Files:** `app.py`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `k8s.yaml`, `hpa.yaml`.
- [x] **Architecture Diagrams:** Documented in [ARCHITECTURE.md](file:///c:/Users/shubh/Downloads/cloud%20project/ARCHITECTURE.md).
- [x] **Cost Analysis:** Detailed comparison table in [COST_OPTIMIZATION_ANALYSIS.md](file:///c:/Users/shubh/Downloads/cloud%20project/COST_OPTIMIZATION_ANALYSIS.md).
- [x] **Screenshots Guide:** Complete command and output reference in [SCREENSHOTS_GUIDE.md](file:///c:/Users/shubh/Downloads/cloud%20project/SCREENSHOTS_GUIDE.md).
- [x] **GitHub Link:** Provided in [github_link.txt](file:///c:/Users/shubh/Downloads/cloud%20project/github_link.txt).
- [x] **Full Written Project Report:** Provided in [PROJECT_REPORT.md](file:///c:/Users/shubh/Downloads/cloud%20project/PROJECT_REPORT.md).
