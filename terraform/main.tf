# terraform/main.tf

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# --- 1. ADD THIS BLOCK ---
# Read the email address from the credentials file
locals {
  gcp_credentials       = jsondecode(file(var.gcp_credentials_file))
  service_account_email = local.gcp_credentials.client_email
}
# --- END OF ADDITION ---


# Configure the Google Provider
provider "google" {
  project     = var.gcp_project_id
  region      = var.gcp_region
  credentials = file(var.gcp_credentials_file)
}

# 2. Create the Google Cloud Run Service
resource "google_cloud_run_v2_service" "api_service" {
  name     = var.service_name
  location = var.gcp_region

  template {
    # --- 3. ADD THIS LINE ---
    # Tell Cloud Run to use its own creator's identity
    service_account = local.service_account_email
    # --- END OF ADDITION ---

    containers {
      image = var.image_identifier
      
      ports {
        container_port = 8000 # The port your Dockerfile EXPOSEs
      }
    }
  }
}

# 4. This resource makes the service public
resource "google_cloud_run_v2_service_iam_binding" "public_access" {
  project  = google_cloud_run_v2_service.api_service.project
  location = google_cloud_run_v2_service.api_service.location
  name     = google_cloud_run_v2_service.api_service.name

  role    = "roles/run.invoker"
  members = ["allUsers"]
}