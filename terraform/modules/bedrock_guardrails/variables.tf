variable "project_name" {
    description = "Project name, used as a prefix for the guardrail name"
    type = string
}

variable "environment" {
    description = "Environment name (dev, prod)"
    type = string
}


variable "blocked_input_messaging" {
    description = "Message to return if an input is blocked"
    type = string
}

variable "blocked_outputs_messaging" {
    description = "Message to return if an output is blocked"
    type = string
}

variable "aws_region" {
    description = "The region of the AWS"
    type = string
}

variable "aws_account_id" {
    description = "AWS account ID"
    type = string
}