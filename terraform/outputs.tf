# This name MUST match what's in your GitHub workflow
output "cloud_run_url" {
  
  # The description is just a human-readable string, not the value
  description = "The URL of the deployed Cloud Run service"
  
  # This correctly gets the URL from the resource named "api_service" in your main.tf
  value       = google_cloud_run_v2_service.api_service.uri
}