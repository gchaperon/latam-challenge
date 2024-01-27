output "gcp_project" {
  value = local.gcp_project_id
}

output "docker_repository_location" {
  value = google_artifact_registry_repository.challenge_repo.location
}

output "docker_repository_id" {
  value = google_artifact_registry_repository.challenge_repo.repository_id
}

output "docker_tag_base" {
  value = join("/", [
    "${google_artifact_registry_repository.challenge_repo.location}-docker.pkg.dev",
    local.gcp_project_id,
    google_artifact_registry_repository.challenge_repo.repository_id,
    local.image_name,
  ])
}
