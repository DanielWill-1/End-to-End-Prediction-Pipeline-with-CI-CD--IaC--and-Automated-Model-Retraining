

variable "gcp_project_id" {
  description = "The ID of your Google Cloud project."
  type        = string
  # Find this on your GCP dashboard
  default     = "aiops-mini-project" 
}

variable "gcp_region" {
  description = "The GCP region to deploy in."
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "The name for the Cloud Run service."
  type        = string
  default     = "diabetes-api-service"
}

variable "image_identifier" {
  description = "The full URI of the Docker image in GHCR."
  type        = string
  default     = "ghcr.io/danielwill-1/my-diabetes-api:latest"
}

variable "gcp_credentials_file" {
  description = "Path to the GCP service account JSON key."
  type        = string
  default     = "gcp-credentials.json"
}

