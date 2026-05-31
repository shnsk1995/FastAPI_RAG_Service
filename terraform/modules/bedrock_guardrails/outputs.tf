output "input_guardrail_name" {
    description = "Guardrail name"
    value = aws_bedrock_guardrail.this.name
}

output "input_guardrail_arn" {
    description = "Guardrail ARN - needed for IAM policies"
    value = aws_bedrock_guardrail.this.guardrail_arn
}

output "input_guardrail_id" {
    description = "Guardrail ID"
    value = aws_bedrock_guardrail.this.guardrail_id
}

output "input_guardrail_version" {
    description = "Guardrail version"
    value = aws_bedrock_guardrail.this.version
}