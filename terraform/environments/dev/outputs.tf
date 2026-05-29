output "dynamodb_table_name" {
  description = "DynamoDB table name — use this in your FastAPI app config"
  value       = module.dynamodb.table_name
}

output "dynamodb_table_arn" {
  description = "DynamoDB table ARN — use this in IAM policies when you add Lambda"
  value       = module.dynamodb.table_arn
}

output "dynamodb_table_id" {
  description = "DynamoDB table ID"
  value       = module.dynamodb.table_id
}