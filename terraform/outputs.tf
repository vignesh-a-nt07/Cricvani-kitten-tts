output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.kitten_tts.id
}

output "public_ip" {
  description = "Public IP address of the EC2 instance (EIP if created, otherwise auto-assigned)"
  value       = var.use_elastic_ip ? aws_eip.kitten_tts_eip[0].public_ip : aws_instance.kitten_tts.public_ip
}

output "private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.kitten_tts.private_ip
}

output "public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = var.use_elastic_ip ? aws_eip.kitten_tts_eip[0].public_dns : aws_instance.kitten_tts.public_dns
}

output "ssh_command" {
  description = "SSH command to connect to the instance"
  value       = "ssh -i <your_key.pem> ubuntu@${var.use_elastic_ip ? aws_eip.kitten_tts_eip[0].public_ip : aws_instance.kitten_tts.public_ip}"
}
