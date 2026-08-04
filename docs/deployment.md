# Deployment Guide - Enterprise Context Engineering

This guide details how to deploy the Context Engineering infrastructure and application microservices across enterprise environments.

## Deployment Stages

1. **Infrastructure Provisioning**: Terraform IaC script execution.
2. **Container Build & Push**: Docker multi-stage image build pushed to Enterprise Container Registry (ECR / ACR).
3. **App Deployment**: Kubernetes (EKS/AKS) or Container App deployment.

## Terraform Provisioning

### Environment Variables Preparation

Copy `terraform/terraform.tfvars.example` to `terraform.tfvars` and set target variables:

```hcl
environment       = "production"
aws_region        = "us-east-1"
vpc_cidr          = "10.100.0.0/16"
enable_vector_db  = true
container_cpu     = 1024
container_memory  = 2048
```

### Terraform Commands

```bash
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

## Docker Container Deployment

Build and push the production container image:

```bash
# Build image
docker build -t enterprise-context-engineering:latest .

# Tag and push to Enterprise Registry
docker tag enterprise-context-engineering:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/genai/context-engineering:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/genai/context-engineering:latest
```

## Health Verification

Verify deployment health:

```bash
curl -f https://context-engineering.internal.enterprise.com/health
```
Expected output:
```json
{"status": "healthy", "service": "enterprise-context-engineering", "version": "1.0.0"}
```
