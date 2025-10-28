# terraform/outputs.tf

output "api_service_url" {
  description = "https://diabetes-api-service-645615724525.us-central1.run.app"
  value = google_cloud_run_service.default.status[0].url
}