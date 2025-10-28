# terraform/variables.tf

variable "gcp_project_id" {
  description = "The ID of your Google Cloud project."
  type        = string
  default     = "aiops-mini-project" # Make sure this matches your GCP project ID
}

variable "gcp_region" {
  description = "The GCP region to deploy in."
  type        = string
  default     = "us-central1"
}

variable "gcp_credentials_file" {
  description = "Path to the GCP service account JSON key."
  type        = string
  default     = "gcp-credentials.json"
}

variable "registry_name" {
  description = "The name for the new Artifact Registry."
  type        = string
  default     = "my-app-registry"
}

# -----------------------------------------------------
# ADD THESE NEW VARIABLES
# -----------------------------------------------------

variable "cloud_run_service_name" {
  description = "The name for the Cloud Run API service."
  type        = string
  default     = "diabetes-api-service"
}

variable "docker_image_name" {
  description = "The name and tag of the Docker image to deploy (e.g., 'my-image:latest')."
  type        = string
  default     = "my-api:latest" # <-- IMPORTANT: You MUST change this
}