# Landing Zone VPC Network Configuration
resource "aws_vpc" "landing_zone" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "genai-landing-zone-vpc-${var.environment}"
  }
}

resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.landing_zone.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, 1)
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "genai-private-subnet-a-${var.environment}"
  }
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.landing_zone.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, 2)
  availability_zone = "${var.aws_region}b"

  tags = {
    Name = "genai-private-subnet-b-${var.environment}"
  }
}

# KMS Encryption Key for Enterprise Context Store
resource "aws_kms_key" "context_key" {
  description             = "KMS Key for Context Store and Secret Encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name = "context-engineering-kms-${var.environment}"
  }
}

# Secrets Manager for API Keys & DB Credentials
resource "aws_secretsmanager_secret" "context_secrets" {
  name                    = "genai/context-engineering/config-${var.environment}"
  kms_key_id              = aws_kms_key.context_key.id
  recovery_window_in_days = 0
}

# IAM Role for Context Engineering Microservice
resource "aws_iam_role" "microservice_role" {
  name = "genai-context-engineering-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy attachment for KMS & Secrets Manager access
resource "aws_iam_policy" "secrets_access" {
  name        = "genai-secrets-policy-${var.environment}"
  description = "Access policy for KMS and Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "kms:Decrypt"
        ]
        Resource = [
          aws_secretsmanager_secret.context_secrets.arn,
          aws_kms_key.context_key.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_secrets" {
  role       = aws_iam_role.microservice_role.name
  policy_arn = aws_iam_policy.secrets_access.arn
}
