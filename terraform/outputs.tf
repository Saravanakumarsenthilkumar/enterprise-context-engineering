output "vpc_id" {
  value       = aws_vpc.landing_zone.id
  description = "The ID of the GenAI Landing Zone VPC"
}

output "kms_key_arn" {
  value       = aws_kms_key.context_key.arn
  description = "The ARN of the KMS Encryption Key for Context Engine"
}

output "secrets_manager_arn" {
  value       = aws_secretsmanager_secret.context_secrets.arn
  description = "The ARN of Secrets Manager configuration entry"
}

output "iam_role_arn" {
  value       = aws_iam_role.microservice_role.arn
  description = "IAM Role ARN assumed by Context Engineering microservice"
}
