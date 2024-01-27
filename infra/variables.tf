variable "docker_image" {
  type = string
  default = "us-docker.pkg.dev/cloudrun/container/hello"
  description = "The image to deploy using Cloud Run"
}
