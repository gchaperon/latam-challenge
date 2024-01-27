output "gcp_project" {
  value = local.gcp_project_id
}

output "docker_repository_location" {
  value = google_artifact_registry_repository.challenge_repo.location
}

output "docker_repository_id" {
  value = google_artifact_registry_repository.challenge_repo.repository_id
}

output "docker_image_name" {
  value = local.image_name
}

output "docker_tag_base" {
  value = local.docker_image_base
}

output "app_uri" {
  value = google_cloud_run_v2_service.default.uri
}
