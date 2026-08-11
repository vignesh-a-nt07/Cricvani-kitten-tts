# CricVani Kitten TTS Infrastructure

This directory contains the Infrastructure-as-Code (IaC) setup for deploying the CricVani Kitten TTS server to an AWS EC2 instance. 

It uses **Terraform** to provision the AWS infrastructure and **Ansible** to configure the server and deploy the application.

## 🏗️ Architecture

- **Cloud Provider**: AWS
- **Server**: 1x EC2 Instance (t3.small, Ubuntu 24.04 LTS x86_64)
- **Storage**: 20 GB gp3 Root EBS Volume
- **Network**: Security Group exposing SSH (22) and Application (8001) to specific CIDRs. Optional Elastic IP.
- **Application Stack**: Python 3, FastAPI, Uvicorn, ONNX Runtime, Kitten TTS. (No Docker)

---

## 🚀 Part 1: Provision Infrastructure (Terraform)

Terraform manages the AWS resources.

### 1. Configure Variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
- Ensure `key_pair_name` matches an existing SSH key pair in your AWS account.
- Update `ssh_allowed_cidr` and `app_allowed_cidr` to your public IP (e.g., `203.0.113.1/32`) to secure the staging environment.

### 2. Deploy

```bash
terraform init
terraform plan
terraform apply
```

After successful deployment, Terraform will output:
- `instance_id`
- `public_ip`
- `private_ip`
- `public_dns`
- `ssh_command`

Take note of the `public_ip`.

---

## 🛠️ Part 2: Configure Server (Ansible)

Ansible installs dependencies (Python, virtualenv, espeak-ng, etc.) and synchronizes the application code.

### 1. Configure Inventory

```bash
cd ../ansible
cp inventory/hosts.ini.example inventory/hosts.ini
```

Edit `inventory/hosts.ini` with the `public_ip` from Terraform and the path to your private key:

```ini
[kitten_tts]
<EC2_PUBLIC_IP> ansible_user=ubuntu ansible_ssh_private_key_file=~/path/to/your-key.pem
```

### 2. Run Ansible Playbook

```bash
ansible-playbook -i inventory/hosts.ini playbook.yml
```

> **Note**: Ansible sets up the server, creates the virtual environment, installs Python dependencies, and creates a systemd service file. However, **it does NOT start the application automatically** during the first run, allowing you to test it manually first.

---

## 🏃 Part 3: Manual Application Test

After Ansible finishes, SSH into the EC2 instance to test the application manually.

### 1. SSH into the Instance

```bash
ssh -i ~/path/to/your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### 2. Verify Server Setup

```bash
# Check Python version
python3 --version

# Verify application files exist
ls -la /opt/cricvani-kitten-tts

# Verify virtual environment exists
ls -la /opt/cricvani-kitten-tts/venv
```

### 3. Start the Application Manually

```bash
cd /opt/cricvani-kitten-tts
# Activate virtual environment
source venv/bin/activate
# Run application exactly as it runs locally
make run
```

*The application will download the Hugging Face model automatically on the first run if not found in `models/`.*

### 4. Test Health Endpoint

From a separate terminal on the EC2 instance or while the app is running:
```bash
curl http://localhost:8001/health
```

From your local laptop (requires your IP to be in `app_allowed_cidr` in Terraform):
```bash
curl http://<EC2_PUBLIC_IP>:8001/health
```

### 5. Configure Local CricVani

Update your local CricVani configuration to point to the new Kitten TTS staging server:

```text
Kitten TTS Server URL: http://<EC2_PUBLIC_IP>:8001
```

---

## ⚙️ Part 4: Managing with Systemd (Optional)

Once you have manually verified the application works via `make run`, you can use systemd to manage it in the background.

```bash
# Start the service
sudo systemctl start cricvani-kitten-tts

# Check status
sudo systemctl status cricvani-kitten-tts

# Stop the service
sudo systemctl stop cricvani-kitten-tts

# Restart the service
sudo systemctl restart cricvani-kitten-tts

# Enable to start on boot
sudo systemctl enable cricvani-kitten-tts
```

---

## 🧹 Part 5: Resource Destruction

To tear down all AWS resources created by Terraform and stop incurring costs:

```bash
cd terraform
terraform destroy
```

> This will destroy the EC2 instance, Security Group, and release the Elastic IP. It will not delete the local state or code.

---

## 🛡️ Important Notes

- **Application Code**: Terraform and Ansible do **not** modify any of the existing application code (`FastAPI routes`, `TTS logic`, `Makefile`, etc.). The application remains untouched.
- **Model Handling**: The deployment assumes the application handles model loading. As per the local setup, the `kittentts` library will download the model weights to cache upon first execution if not present in the `models/` directory.
- **Security**: The AWS key pair is only referenced by name. Private `.pem` keys, credentials, and `.tfstate` files are ignored via `.gitignore` and should never be committed.
