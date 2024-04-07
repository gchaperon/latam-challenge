variable "docker_tag" {
  type        = string
  default     = null
  description = "The tag of the image to deploy to Cloud Run"
}

variable "deploy" {
  type        = bool
  default     = true
  description = "Boolean flag that controls whether the project should be deployed or not."
}
