# terraform/main.tf

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project     = var.gcp_project_id
  region      = var.gcp_region

}

# 1. Create the Artifact Registry
resource "google_artifact_registry_repository" "registry" {
  location      = var.gcp_region
  repository_id = var.registry_name
  description   = "Docker registry for the diabetes API"
  format        = "DOCKER" # This tells it to be a Docker registry
}

# 2. Create the Cloud Run v2 Service
resource "google_cloud_run_v2_service" "api_service" {
  name     = var.cloud_run_service_name
  location = var.gcp_region

  # This section defines the container to run
  template {
    containers {
      # This pulls the image from the Artifact Registry you just created
      image = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.registry.repository_id}/${var.docker_image_name}"

      ports {
        container_port = 8000 # Change this if your FastAPI/Flask app runs on a different port
      }
    }
  }

  # This ensures the service isn't created until the registry exists
  depends_on = [
    google_artifact_registry_repository.registry
  ]
}

# 3. Make the Cloud Run service publicly accessible
resource "google_cloud_run_v2_service_iam_member" "allow_public" {
  name     = google_cloud_run_v2_service.api_service.name
  location = google_cloud_run_v2_service.api_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}