terraform {

    required_version = ">= 1.5.0"

    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 5.0"
        }
    }


    backend "s3" {
        bucket = "fastapi-rag-backend-terraform-state"
        key = "dev/terraform.tfstate"
        region = "us-east-2"
        use_lockfile = true
        encrypt = true
    }

}


provider "aws" {

    region = var.aws_region
    profile = var.aws_profile

    default_tags {
        tags = {
            Project = var.project_name
            Environment = var.environment
            ManagedBy = "terraform"
        }
    }

}




module "dynamodb" {
    source = "../../modules/dynamodb"

    project_name = var.project_name
    environment = var.environment


    hash_key = "conversation_id"
    hash_key_type = "S"
    range_key = "created_at"
    range_key_type = "S"

    billing_mode = "PAY_PER_REQUEST"
    point_in_time_recovery = false
    ttl_attribute = "expiresAt"

    tags = var.common_tags
}