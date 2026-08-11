provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "CricVani"
      Component   = "Kitten-TTS"
      Environment = "staging"
      ManagedBy   = "Terraform"
    }
  }
}
