resource "aws_dynamodb_table" "this"{

    name = "${var.project_name}-${var.environment}"
    billing_mode = var.billing_mode
    hash_key = var.hash_key
    range_key = var.range_key


    attribute {
        name = var.hash_key
        type = var.hash_key_type
    }

    attribute {
        name = var.range_key
        type = var.range_key_type
    }

    ttl {
        attribute_name = var.ttl_attribute
        enabled = true
    }

    point_in_time_recovery {
        enabled = var.point_in_time_recovery
    }


    tags = merge(
        {
            Name = "${var.project_name}-${var.environment}-users"
            Environment = var.environment
            ManagedBy = "terraform"
        },
        var.tags
    )

}