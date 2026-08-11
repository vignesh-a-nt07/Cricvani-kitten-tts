provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.project_name
      Component   = var.component_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
