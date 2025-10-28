# terraform/outputs.tf

output "api_service_url" {
  description = "The public URL of the deployed FastAPI service."
  value       = google_cloud_run_v2_service.api_service.uri
}