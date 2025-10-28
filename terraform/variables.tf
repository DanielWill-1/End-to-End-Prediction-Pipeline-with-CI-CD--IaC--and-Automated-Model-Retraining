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