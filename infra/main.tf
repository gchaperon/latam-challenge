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

module "latam-challenge" {
  count  = var.deploy ? 1 : 0
  project_id = local.gcp_project_id
  source = "./modules/latam-challenge"

  docker_tag = var.docker_tag
}
