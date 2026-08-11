# CricVani Kitten TTS - Automated Deployment

This repository implements an automated software deployment pipeline using GitHub Actions, while keeping **AWS Infrastructure (Terraform) strictly local**.

## Architecture Overview

**1. Local Machine (Infrastructure):**
Terraform manages the AWS EC2 instance, Security Group, and Elastic IP on your local laptop. The `.tfstate` file is kept completely local. 

**2. GitHub Actions (Software Deployment):**
The `kittendeploy.yml` workflow connects to the already-running EC2 instance via SSH, configures the Ubuntu server, sets up the Python virtual environment, installs dependencies natively (without Ansible/Docker), and runs the application via Systemd.

---

## 1. Local Terraform (One-Time Setup)

Before triggering the deployment workflow in GitHub, you must manually create the AWS resources locally.

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Update terraform.tfvars with your actual Key Pair Name and Public IP CIDR

terraform init
terraform plan
terraform apply
```

After Terraform finishes, note the exact EC2 Public IP:
```bash
terraform output public_ip
```
You will need this IP for GitHub Actions.

---

## 2. GitHub Secrets & Variables

Before deploying, configure your GitHub Repository Settings (**Settings → Secrets and variables → Actions**).

### Required Secrets
| Secret Name | Description |
| :--- | :--- |
| `EC2_SSH_KEY` | The exact raw contents of your AWS SSH Private Key (`.pem` file). **Never print or commit this key.** |
| `HUGGINGFACE_TOKEN` | *(Optional)* If required by the model loader. |

### Optional Variables
You do NOT need to set these unless you are deviating from the defaults:
| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `EC2_USERNAME` | `ubuntu` | EC2 Login User |
| `APP_DIR` | `/opt/cricvani-kitten-tts` | Directory to deploy application |
| `APP_PORT` | `8001` | FastAPI port |
| `SYSTEMD_SERVICE`| `cricvani-kitten-tts` | Name of the systemd service |

---

## 3. GitHub Actions Deployment

Once the EC2 is up and running:

1. Navigate to **GitHub → Actions → Deploy Kitten TTS**
2. Click **Run workflow**
3. In the input box for **`ec2_host`**, paste the Public IP of your EC2 instance (e.g. `54.91.101.195`).
4. Execute.

**What GitHub Actions does automatically:**
- Connects securely via SSH (using `StrictHostKeyChecking=no` temporarily for the runner).
- Installs `python3-venv`, `build-essential`, `espeak-ng`, etc.
- Creates the `kittentts` user and directory.
- `rsync`s your current application code directly.
- Compiles a native Python `venv` using `pip install -r requirements.txt`.
- Idempotently creates and restarts a `systemd` service.
- Polls the `/health` endpoint until the system is responsive and the loaded model is verified.

---

## 4. Code Update Flow

Whenever you update the Kitten TTS code (routes, providers, config):
1. `git push` your changes to GitHub.
2. Go to **Actions → Deploy Kitten TTS**.
3. **Run workflow** and provide the EC2 IP.

The workflow is completely idempotent and will seamlessly update the code, upgrade Python dependencies, and restart the service in seconds.

---

## 5. Server Status Checking

If you are encountering issues, you can run the diagnostic workflow:
1. Navigate to **Actions → Server Status**
2. Click **Run workflow** and input the EC2 IP.
3. This safely retrieves `systemctl status`, system memory (`free -h`), disk space (`df -h`), networking (`ss -lntp`), and the actual `/health` JSON.

---

## 6. Local Terraform Destroy

To tear down the staging environment, use your local laptop where the Terraform state lives:

```bash
cd terraform
terraform destroy
```

**GitHub Actions will NEVER destroy your AWS resources or manage your Terraform state.**

---

## 7. Security Notes

- The AWS SSH key (`.pem`) is temporarily materialized in `/tmp` in the ephemeral Actions runner and immediately removed. 
- Using `StrictHostKeyChecking=no` allows the GitHub Action Runner to connect without prior trust caching. This is an acceptable tradeoff for an ephemeral staging runner, but the key is tightly restricted.
- Ensure your `terraform/terraform.tfvars`, AWS credentials, and `.pem` files are never tracked in `.git` (which are ignored correctly by `.gitignore`).
