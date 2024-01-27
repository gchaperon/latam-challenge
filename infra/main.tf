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
    containers {
      image = var.docker_image
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
