variable "project_name" {
    description = "Project name, used as a prefix for the table name"
    type = string
}

variable "environment" {
    description = "Environment name (dev, prod)"
    type = string
}


variable "billing_mode" {
    description = "DynamoDB billing mode"
    type = string
    default = "PAY_PER_REQUEST"

    validation {
        condition = contains(["PAY_PER_REQUEST","PROVISIONED"], var.billing_mode)
        error_message = "billing_mode must be PAY_PER_REQUEST or PROVISIONED."
    }
}



variable "hash_key" {
    description = "Partition key attribute name"
    type = string
}

variable "hash_key_type" {
    description = "Partition key type: S (String), N (Number), B (Binary)"
    type = string
    default = "S"

    validation {
        condition = contains(["S", "N", "B"], var.hash_key_type)
        error_message = "hash_key_type must be S, N, B."
    }
}


variable "range_key" {
    description = "Sort key attribute name"
    type = string
}

variable "range_key_type" {
    description = "Sort key type: S (String), N (Number), B (Binary)"
    type = string
    default = "S"

    validation {
        condition = contains(["S", "N", "B"], var.range_key_type)
        error_message = "range_key_type must be S, N, B."
    }
}


variable "ttl_attribute" {
    description = "Attribute name to use for TTL (must be a Number type in your items)"
    type = string
    default = "expiresAt"
}


variable "point_in_time_recovery" {
    description = "Enable point_in_time_recovery (recommended for prod)"
    type = bool
    default = false
}


variable "tags" {
    description = "Additional tags to apply to the table"
    type = map(string)
    default = {}
}