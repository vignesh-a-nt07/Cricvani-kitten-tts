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
    Name = "CricVani-Kitten-TTS-staging-ec2"
  }
}

resource "aws_eip" "kitten_tts_eip" {
  instance = aws_instance.kitten_tts.id
  domain   = "vpc"

  tags = {
    Name = "CricVani-Kitten-TTS-staging-eip"
  }
}
