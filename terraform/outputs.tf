output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.kitten_tts.id
}

output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.kitten_tts_eip.public_ip
}

output "private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.kitten_tts.private_ip
}

output "public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_eip.kitten_tts_eip.public_dns
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i <your_key.pem> ubuntu@${aws_eip.kitten_tts_eip.public_ip}"
}
