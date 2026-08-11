data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_security_group" "kitten_tts_sg" {
  name        = "${var.project_name}-${var.component_name}-${var.environment}-sg"
  description = "Security group for Kitten TTS Server"

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  ingress {
    description = "Application access (FastAPI)"
    from_port   = 8001
    to_port     = 8001
    protocol    = "tcp"
    cidr_blocks = [var.app_allowed_cidr]
  }

  egress {
    description = "Allow all outbound traffic for downloading packages and models"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "kitten_tts" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_pair_name

  vpc_security_group_ids = [aws_security_group.kitten_tts_sg.id]

  root_block_device {
    volume_size = var.root_volume_size
    volume_type = "gp3"
  }

  tags = {
    Name = "${var.project_name}-${var.component_name}-${var.environment}-ec2"
  }
}

resource "aws_eip" "kitten_tts_eip" {
  count    = var.use_elastic_ip ? 1 : 0
  instance = aws_instance.kitten_tts.id
  domain   = "vpc"

  tags = {
    Name = "${var.project_name}-${var.component_name}-${var.environment}-eip"
  }
}
