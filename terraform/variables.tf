variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t3.small"
}

variable "root_volume_size" {
  type        = number
  description = "Root EBS volume size in GB"
  default     = 20
}

variable "key_pair_name" {
  type        = string
  description = "AWS EC2 Key Pair Name"
}

variable "allowed_cidr" {
  type        = string
  description = "CIDR block allowed for SSH and port 8001"
}
