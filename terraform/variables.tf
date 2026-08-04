variable "aws_region" {
  type        = string
  description = "AWS region for infrastructure provisioning"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Deployment environment (dev, staging, production)"
  default     = "production"
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the landing zone VPC"
  default     = "10.100.0.0/16"
}

variable "container_cpu" {
  type        = number
  description = "CPU units for context engineering container app"
  default     = 1024
}

variable "container_memory" {
  type        = number
  description = "Memory (in MB) for context engineering container app"
  default     = 2048
}

variable "enable_vector_db" {
  type        = bool
  description = "Provision dedicated OpenSearch/Vector DB cluster"
  default     = true
}
