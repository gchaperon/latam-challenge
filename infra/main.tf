terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.74.0"
    }
  }
  backend "gcs" {
    bucket = "terraform-states-18e96eb9"
  }

  required_version = ">= 1.2.0"
}

locals {
  gcp_project_id = "latam-challenge-412300"
  image_name = "latam-challenge"
  default_image = "us-docker.pkg.dev/cloudrun/container/hello"
}
locals {
  docker_image_base = join("/", [
    "${google_artifact_registry_repository.challenge_repo.location}-docker.pkg.dev",
    local.gcp_project_id,
    google_artifact_registry_repository.challenge_repo.repository_id,
    local.image_name,
  ])
}

locals {
  docker_image = var.docker_tag == null ? local.default_image : "${local.docker_image_base}:${var.docker_tag}"
}

provider "google" {
  project = local.gcp_project_id
}

resource "google_artifact_registry_repository" "challenge_repo" {
  location      = "us-central1"
  repository_id = "latam-challenge"
  description   = "Repo storing docker images for my solution to the LATAM Challenge"
  format        = "DOCKER"

  docker_config {
    immutable_tags = true
  }
}

resource "google_cloud_run_v2_service" "default" {
  name     = "latam-challenge"
  location = "us-central1"
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      max_instance_count = 10
      min_instance_count = 1
    }

    containers {
      image = local.docker_image
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "member" {
  project = google_cloud_run_v2_service.default.project
  location = google_cloud_run_v2_service.default.location
  name = google_cloud_run_v2_service.default.name
  role = "roles/run.invoker"
  member = "allUsers"
}
