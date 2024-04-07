variable "docker_tag" {
  type = string
  default = null
  description = "The tag of the image to deploy to Cloud Run"
}

variable "project_id" {
  type = string
  description = "The GCP project where the resources will be created"
}
