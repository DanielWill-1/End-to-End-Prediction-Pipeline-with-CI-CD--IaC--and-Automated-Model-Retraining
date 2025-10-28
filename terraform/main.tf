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
  credentials = file(var.gcp_credentials_file)
}

# 1. Create the Artifact Registry
resource "google_artifact_registry_repository" "registry" {
  location      = var.gcp_region
  repository_id = var.registry_name
  description   = "Docker registry for the diabetes API"
  format        = "DOCKER" # This tells it to be a Docker registry
}