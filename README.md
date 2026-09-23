# End-to-End Prediction Pipeline with CI/CD, IaC, and Automated Model Retraining

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-orange)
![Machine Learning](https://img.shields.io/badge/ML-RandomForest-green)
![Infrastructure](https://img.shields.io/badge/Infrastructure-Terraform%20%26%20GCP-red)
![Containerization](https://img.shields.io/badge/Docker-Containerized-lightblue)

An educational MLOps project that demonstrates the full machine-learning model lifecycle: automated retraining, model artifact generation, model serving via FastAPI, containerization with Docker, and deployment through GitHub Actions CI/CD and Terraform infrastructure-as-code on Google Cloud Platform.

The diabetes classifier in this project is intentionally simple and lightweight. The real subject of this project is not model sophistication; it is learning what happens after an ML model is trained — how new data triggers retraining, how a trained model is packaged as an artifact, served through an API, containerized, and deployed.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Learning Goals](#learning-goals)
3. [Problem Statement](#problem-statement)
4. [Project Architecture](#project-architecture)
5. [End-to-End Flow](#end-to-end-flow)
6. [Features](#features)
7. [Project Structure](#project-structure)
8. [Installation & Setup](#installation--setup)
9. [Usage](#usage)
10. [API Documentation](#api-documentation)
11. [Model Training & Performance](#model-training--performance)
12. [CI/CD Pipeline](#cicd-pipeline)
13. [Deployment & Infrastructure](#deployment--infrastructure)
14. [Security](#security)
15. [Future Improvements](#future-improvements)
16. [Contributing](#contributing)
17. [License](#license)

---

## Project Overview

This repository is a production-oriented, end-to-end MLOps learning pipeline. It walks the complete journey an ML model takes from training data to a live inference API:

- a lightweight diabetes classifier is retrained from a tracked dataset
- the trained model and scaler are saved as joblib artifacts
- a FastAPI service loads those artifacts and serves predictions
- a Docker image packages the application
- GitHub Actions trains, builds, deploys, and smoke-tests the service whenever the training data changes
- Terraform provisions the Google Cloud resources (Artifact Registry and Cloud Run)

The emphasis is on the engineering workflow, not the modeling.

---

## Learning Goals

This project was designed to teach the concepts and mechanics of operating an ML model after it has been trained:

- what happens after model training
- model serialization and artifact management (joblib)
- loading trained artifacts inside an inference service
- FastAPI-based model serving with automatic API documentation
- Dockerizing an ML application
- CI/CD for machine learning workflows
- automated model retraining triggered by data changes
- infrastructure-as-code with Terraform
- cloud deployment to Google Cloud Run
- connecting source control, training, packaging, and deployment into one workflow

---

## Problem Statement

### The Engineering Problem

A team has a trained ML model. New training data is periodically added to the repository. Every meaningful change should be able to trigger the full pipeline automatically: retrain the model, build a new container image, deploy it to a cloud service, and confirm the new version responds correctly.

This project answers a practical question: how do you take a model and make it continuously deliverable?

### The Example Application

Diabetes prediction on the Pima Indians Diabetes Database is used as the demonstration application. It is a well-known, small public dataset suitable for learning the pipeline without the overhead of a large modeling effort.

The dataset contains:

- 768 patient records
- 8 features: Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, Diabetes Pedigree Function, Age
- a binary target (Outcome): presence or absence of diabetes

### Scope

The project implements and deploys the full training-to-serving workflow end to end. It is not a clinically validated product and makes no medical claims (see the [Healthcare Disclaimer](#healthcare-disclaimer)).

---

## Project Architecture

The central story of the architecture is the ML lifecycle:

```
New Data -> Git Commit -> CI/CD -> Retrain -> Save Model -> Build Image -> Deploy (Terraform) -> FastAPI Inference
```

```
                data/diabetes.csv (tracked training data)
                              │
                              ▼  change pushed to main
                     GitHub Actions (ci-cd.yml)
        ┌───────────────────────┼───────────────────────┐
        ▼                                              │
  Job 1: Retrain and Build                            │
    python scripts/train.py                           │
    diabetes_model.joblib + scaler.joblib             │
    docker build & push -> Artifact Registry           │
        └───────────────────────┬─────────────────────┘
                                ▼
                 Job 2: Deploy to Cloud Run
                   Terraform init + apply
                   cloud run v2 service
                                │
                                ▼
                 Job 3: Smoke Test
                   curl / and /predict (expect 200)
                                │
                                ▼
                        FastAPI Inference
                      (app/main.py, port 8000)
```

The model and scaler are loaded from `artifacts/` at application startup in `app/main.py`. The training pipeline lives in `scripts/train.py`.

---

## End-to-End Flow

The flow follows the actual implementation in the repository:

1. Training data (`data/diabetes.csv`) is updated.
2. The change is committed and pushed to the `main` branch.
3. The GitHub Actions workflow `ci-cd.yml` is triggered, filtered on changes to `data/diabetes.csv`.
4. The retraining job installs dependencies and runs `scripts/train.py`.
5. The model and scaler are retrained and saved as joblib artifacts.
6. A Docker image is built and pushed to Google Artifact Registry (tagged with both `latest` and the commit SHA).
7. Terraform initializes and applies, updating the Cloud Run service with the new image.
8. A smoke-test job calls the live `GET /` and `POST /predict` endpoints and fails the pipeline on a non-200 response.
9. The updated model is served by FastAPI on Cloud Run.

All steps listed above are implemented. Planned or aspirational capabilities are called out separately under [Future Improvements](#future-improvements).

---

## Features

### ML
- Random Forest Classifier with GridSearchCV hyperparameter tuning (`n_estimators`, `max_depth`, `min_samples_split`, 5-fold cross-validation)
- Median imputation of placeholder zero values and `StandardScaler` normalization
- Trained model and scaler artifacts, saved with joblib

### Model Serving
- FastAPI application with a health-check endpoint (`GET /`) and a prediction endpoint (`POST /predict`)
- Pydantic input validation and automatic OpenAPI documentation (`/docs`, `/redoc`)
- JSON responses with class prediction and probability score

### Containerization
- Multi-step-free Dockerfile based on `python:3.11-slim`
- Application and artifacts baked into the image; served by uvicorn on port 8000
- `.dockerignore` to keep build context clean

### CI/CD
- GitHub Actions workflow (`ci-cd.yml`) that retrains, rebuilds, redeploys, and smoke-tests the service on every relevant data change
- Smoke tests on the live endpoint as a release gate

### Infrastructure
- Terraform-managed Google Cloud resources: a Docker Artifact Registry, a Cloud Run v2 service, and a public invoker IAM binding

---

## Project Structure

```
project-root/
│
├── README.md                          # This documentation
├── LICENSE                            # MIT license
├── Dockerfile                         # Docker container definition
├── requirements.txt                   # Python dependencies
├── pred.py                            # Standalone training/prediction notebook-style script
├── .gitignore                         # Ignored files (incl. gcp-credentials.json)
│
├── app/                               # FastAPI application
│   ├── __init__.py
│   └── main.py                        # API endpoints and artifact loading
│
├── scripts/                           # Training
│   ├── __init__.py
│   └── train.py                       # ML training pipeline (load, preprocess, train, evaluate, save)
│
├── data/
│   └── diabetes.csv                   # Pima Indians Diabetes Database
│
├── artifacts/                         # Trained model and preprocessing artifacts
│   ├── diabetes_model.joblib          # RandomForest model
│   └── scaler.joblib                  # StandardScaler
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml                  # Retrain, rebuild, redeploy, and smoke-test pipeline
│
└── terraform/                         # Infrastructure as Code (GCP)
    ├── main.tf                        # Artifact Registry, Cloud Run service, IAM
    ├── variables.tf                   # Input variables
    ├── outputs.tf                     # cloud_run_url output
    └── .terraform.lock.hcl            # Provider lock file
```

Note: this structure reflects the current state of the repository. There is no `tests/` directory and no `docs/` folder at present.

---

## Installation & Setup

### Prerequisites

- Python 3.11+
- Git
- Docker (optional, for local containerization)
- A Google Cloud Platform account (optional, for cloud deployment)
- Terraform CLI (optional, for local infrastructure runs)

### Local Setup

#### 1. Clone and Enter the Repository

```bash
git clone <repository-url>
cd End-to-End-Prediction-Pipeline-with-CI-CD--IaC--and-Automated-Model-Retraining
```

#### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Train the Model (Optional, First Time)

```bash
python scripts/train.py
```

This regenerates `diabetes_model.joblib` and `scaler.joblib`. In normal operation the committed artifacts in `artifacts/` are already usable.

---

## Usage

### Running the API Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Building and Running with Docker

```bash
docker build -t diabetes-api:latest .
docker run -p 8000:8000 diabetes-api:latest
```

### Accessing the API

- Health check: http://localhost:8000/
- Interactive docs (Swagger UI): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Making a Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Pregnancies": 6,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
  }'
```

Response:

```json
{
  "prediction": 1,
  "probability": 0.87
}
```

Note: the API expects the data structure used by the deployed model. When running locally, ensure `artifacts/diabetes_model.joblib` and `artifacts/scaler.joblib` are present (run `python scripts/train.py` first if they are missing).

---

## API Documentation

### Endpoint: `POST /predict`

Predict diabetes risk from eight patient health metrics.

Request body:

```json
{
  "Pregnancies": 6,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 0,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
}
```

Response `200 OK`:

```json
{
  "prediction": 0 | 1,
  "probability": 0.0-1.0
}
```

The interactive OpenAPI documentation generated by FastAPI is the authoritative reference for the request and response schemas.

---

## Model Training & Performance

### Training Process

`scripts/train.py` implements the training pipeline:

1. Load `data/diabetes.csv` (Pima Indians Diabetes Database)
2. Replace placeholder zeroes with NaN and impute with column medians
3. Split into train/test (80/20, stratified)
4. Standardize features with `StandardScaler`
5. Train a Random Forest Classifier with GridSearchCV and 5-fold cross-validation
6. Evaluate on the held-out test set
7. Save the best model and scaler as joblib artifacts

### Demonstration Results

These metrics are examples that document the trained demonstration model. They are not evidence of clinical usefulness (see the [Healthcare Disclaimer](#healthcare-disclaimer)) and accuracy is not the headline of the project.

| Metric                | Value |
|-----------------------|-------|
| Accuracy              | 82.5% |
| Precision (Diabetes)  | 73%   |
| Recall (Diabetes)     | 57%   |
| F1-Score              | 0.64  |

### Retraining

Two paths exist:

- Automated: pushing a change to `data/diabetes.csv` on `main` triggers the CI/CD workflow, which retrains the model, rebuilds the image, and redeploys.
- Manual: run `python scripts/train.py` locally to regenerate artifacts by hand.

More sophisticated or scheduled retraining triggers are intentionally not implemented and are listed under [Future Improvements](#future-improvements).

---

## CI/CD Pipeline

The repository contains a single GitHub Actions workflow at `.github/workflows/ci-cd.yml` named `CI/CD - Retrain, Rebuild, and Redeploy`. It runs on pushes to `main` that change `data/diabetes.csv` and consists of three jobs:

1. Retrain and Build: checks out the code, installs dependencies, runs `scripts/train.py`, authenticates to Google Cloud using the `GCP_SA_KEY` secret, builds the Docker image, and pushes it to Artifact Registry with `latest` and a commit-SHA tag.
2. Deploy to Cloud Run: authenticates to Google Cloud, runs `terraform init` and `terraform apply` (passing the current image tag), and reads the resulting `cloud_run_url` output.
3. Smoke Test Live Endpoint: calls the live `GET /` root endpoint and `POST /predict`, failing the pipeline if either returns anything other than a 200 status.

There is no separate `deploy.yml`; the workflow file already exists. Unit and integration test suites are not part of the repository today — the release gate is the smoke test job above.

---

## Deployment & Infrastructure

### Terraform

Terraform is used to learn and practice infrastructure-as-code. The configuration in `terraform/` manages:

- `google_artifact_registry_repository` — a Docker Artifact Registry for image storage
- `google_cloud_run_v2_service` — the serverless Cloud Run service running the API container on port 8000
- `google_cloud_run_v2_service_iam_member` — a public invoker binding (`allUsers`) for the Cloud Run service

To apply locally:

```bash
cd terraform
terraform init
terraform plan
terraform apply -var="docker_image_name=my-diabetes-api:latest"
```

Set your GCP project and region via `-var` flags or `terraform.tfvars` (which is gitignored). The `cloud_run_url` output exposes the deployed service URL.

In the CI/CD pipeline, Terraform applies with the SHA-tagged image built in the previous job, so each deployment corresponds to a specific commit.

When running locally, credentials are expected via the `gcp_credentials_file` variable (default `gcp-credentials.json`) or the [standard Google application-default-credentials flow](https://cloud.google.com/docs/authentication). See the [Security](#security) section before placing any credentials on disk.

### Docker

```bash
# Build
docker build -t diabetes-api:latest .

# Run locally
docker run -p 8000:8000 diabetes-api:latest
```

---

## Security

- Credentials must never be committed. `gcp-credentials.json` is listed in `.gitignore` and should stay outside version control. At the time of writing, the tracked files under `terraform/` do not include the credentials file.
- Google Cloud service-account keys should be managed via the GitHub secret `GCP_SA_KEY` (used by the CI/CD workflow) and referenced, not checked in.
- Terraform state (`terraform/terraform.tfstate`) may contain sensitive configuration and infrastructure details. It is currently tracked in this repository; treat it carefully and consider storing it in a remote backend for real deployments.
- Secrets should be supplied through appropriate secret and environment mechanisms (e.g., GitHub Actions secrets for CI/CD, the standard GCP credential flow for local runs) rather than embedded in source files.

---

## Healthcare Disclaimer

This is an educational engineering and MLOps learning project. The diabetes model is built from a small, public dataset (the Pima Indians Diabetes Database). It is not intended for clinical diagnosis, treatment, or any medical decision-making. It should not be used as a substitute for professional medical advice.

---

## Future Improvements

The following are intentional gaps, listed here as future learning goals rather than existing functionality:

- a proper model registry
- experiment tracking (e.g., MLflow or similar)
- model and data drift detection
- more sophisticated monitoring and alerting
- staged / canary deployments
- model promotion and rollback workflows
- more advanced retraining triggers (scheduling, data-volume thresholds, accuracy-based retraining)
- improved observability (structured logs, tracing, dashboards)

These are deliberately outside the current scope and are identified as areas to explore next in the ML-to-production journey.

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Guidelines: keep changes focused, follow the existing code style, and update this README when relevant. Note that the CI/CD workflow currently triggers only on changes to `data/diabetes.csv`; feature changes to application code will not re-deploy until the trigger path is extended.

---

## License

MIT License — see the [LICENSE](LICENSE) file for details.