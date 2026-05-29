

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-2"
}

variable "aws_profile" {
  description = "AWS CLI profile to use locally. Leave empty in CI/CD — IAM role is used instead"
  type        = string
  default     = ""
}



variable "project_name" {
  description = "Project name used as a prefix for all resources"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "project_name must be lowercase letters, numbers, and hyphens only."
  }
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "environment must be dev or prod."
  }
}



variable "common_tags" {
  description = "Additional tags applied to all resources"
  type        = map(string)
  default     = {}
}