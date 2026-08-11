variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
  default     = "us-east-1"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type (must be x86_64, default: t3.small)"
  default     = "t3.small"
}

variable "root_volume_size" {
  type        = number
  description = "Root EBS volume size in GB"
  default     = 20
}

variable "key_pair_name" {
  type        = string
  description = "Name of the existing AWS key pair for SSH access"
}

variable "ssh_allowed_cidr" {
  type        = string
  description = "CIDR block allowed for SSH access"
}

variable "app_allowed_cidr" {
  type        = string
  description = "CIDR block allowed for Application (port 8001) access"
}

variable "environment" {
  type        = string
  description = "Environment name"
  default     = "staging"
}

variable "project_name" {
  type        = string
  description = "Project name"
  default     = "CricVani"
}

variable "component_name" {
  type        = string
  description = "Component name"
  default     = "Kitten-TTS"
}

variable "use_elastic_ip" {
  type        = bool
  description = "Whether to create and attach an Elastic IP"
  default     = true
}
