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

output "input_guardrail_name" {
    description = "Guardrail name"
    value = module.bedrock_guardrails.input_guardrail_name
}

output "input_guardrail_arn" {
    description = "Guardrail ARN - needed for IAM policies"
    value = module.bedrock_guardrails.input_guardrail_arn
}

output "input_guardrail_id" {
    description = "Guardrail ID"
    value = module.bedrock_guardrails.input_guardrail_id
}

output "input_guardrail_version" {
    description = "Guardrail version"
    value = module.bedrock_guardrails.input_guardrail_version
}
