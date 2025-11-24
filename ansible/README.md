# CountryPuff Deployment Guide

This directory contains Ansible playbooks and configuration for deploying CountryPuff to development and production environments.

## 🏗️ Infrastructure Overview

### Environments

- **Development**: `host78.nird.club:63081` (backend: 63181)
- **Production**: `host74.nird.club:63080` (backend: 63180)

### Git Branches

- **Development**: Deploys from `dev` branch
- **Production**: Deploys from `main` branch

## 📋 Prerequisites

1. **Ansible Installation**
   ```bash
   pip install ansible
   ```

2. **SSH Key Setup**
   - Ensure SSH key is available at: `~/.ssh/keys/nirdclub__id_ed25519`
   - Key should have access to both target hosts

3. **Git Repository Access**
   - Deployment pulls from: `https://github.com/pbertain/countrypuff.git`

## 🚀 Quick Deployment

### Deploy to Development
```bash
cd ansible
./deploy.sh dev
```

### Deploy to Production
```bash
cd ansible
./deploy.sh prod
```

## 📁 Directory Structure

```
ansible/
├── deploy.sh                    # Main deployment script
├── README.md                    # This file
├── inventories/
│   └── hosts.yml               # Host inventory configuration
├── group_vars/
│   ├── development.yml         # Development environment variables
│   └── production.yml          # Production environment variables
└── playbooks/
    ├── deploy.yml              # Main deployment playbook
    └── templates/
        └── countrypuff.service.j2  # Systemd service template
```

## 🔧 Manual Deployment

If you prefer to run Ansible commands manually:

### Development
```bash
ansible-playbook -i inventories/hosts.yml -l development playbooks/deploy.yml --diff -v
```

### Production
```bash
ansible-playbook -i inventories/hosts.yml -l production playbooks/deploy.yml --diff -v
```

## 📊 Post-Deployment Verification

### Check Service Status
```bash
# Development
ssh -i ~/.ssh/keys/nirdclub__id_ed25519 root@host78.nird.club "systemctl status countrypuff-dev"

# Production
ssh -i ~/.ssh/keys/nirdclub__id_ed25519 root@host74.nird.club "systemctl status countrypuff-prod"
```

### Test API Endpoints
```bash
# Development
curl http://host78.nird.club:63081/api
curl http://host78.nird.club:63081/api/countries/US

# Production
curl http://host74.nird.club:63080/api
curl http://host74.nird.club:63080/api/countries/US
```

### View Logs
```bash
# Development
ssh -i ~/.ssh/keys/nirdclub__id_ed25519 root@host78.nird.club "journalctl -u countrypuff-dev -f"

# Production
ssh -i ~/.ssh/keys/nirdclub__id_ed25519 root@host74.nird.club "journalctl -u countrypuff-prod -f"
```

## 🛠️ What the Deployment Does

1. **System Setup**
   - Updates package cache
   - Installs Python 3, pip, venv, git, curl, htop
   - Creates application user and group

2. **Application Deployment**
   - Creates application directory structure
   - Clones/updates git repository from appropriate branch
   - Sets up Python virtual environment
   - Installs Python dependencies from requirements.txt

3. **Service Configuration**
   - Creates systemd service file
   - Configures environment variables (PORT, FLASK_ENV, etc.)
   - Sets up logging to `/var/log/countrypuff-{env}/`

4. **Service Management**
   - Starts and enables the systemd service
   - Configures automatic restart on failure

## 🔍 Troubleshooting

### Connection Issues
```bash
# Test SSH connectivity
ssh -i ~/.ssh/keys/nirdclub__id_ed25519 root@host78.nird.club "echo 'Connection successful'"
ssh -i ~/.ssh/keys/nirdclub__id_ed25519 root@host74.nird.club "echo 'Connection successful'"

# Test Ansible connectivity
ansible -i inventories/hosts.yml development -m ping
ansible -i inventories/hosts.yml production -m ping
```

### Service Issues
```bash
# Check service status
systemctl status countrypuff-{env}

# View recent logs
journalctl -u countrypuff-{env} --since "10 minutes ago"

# Restart service
systemctl restart countrypuff-{env}
```

### Application Issues
```bash
# Check if port is listening
netstat -tlnp | grep {port}

# Test local connectivity on server
curl localhost:{port}/api
```

## 🔄 Deployment Workflow

1. **Development Cycle**
   - Make changes on local machine
   - Commit to `dev` branch
   - Deploy to development: `./deploy.sh dev`
   - Test on `host78.nird.club:63081`

2. **Production Release**
   - Merge `dev` branch to `main`
   - Deploy to production: `./deploy.sh prod`
   - Verify on `host74.nird.club:63080`

## 📝 Configuration Details

### Environment Variables
- `PORT`: Application port (63081 for dev, 63080 for prod)
- `FLASK_ENV`: Environment mode (development/production)
- `LOG_LEVEL`: Logging level (DEBUG for dev, INFO for prod)

### File Locations
- **Application**: `/opt/{env}/countrypuff/src/`
- **Virtual Environment**: `/opt/{env}/countrypuff/venv/`
- **Logs**: `/var/log/countrypuff-{env}/`
- **Service File**: `/etc/systemd/system/countrypuff-{env}.service`

### Security
- Application runs as dedicated user (`countrypuff-{env}`)
- Systemd security features enabled (PrivateTmp, ProtectSystem, etc.)
- No root privileges required for application execution