# CountryPuff Deployment Guide

This document provides comprehensive instructions for deploying CountryPuff to development and production environments using GitHub Actions and Ansible.

## 🏗️ Infrastructure Overview

### Environments

| Environment | Host | Frontend Port | Backend Port | Branch | Auto-Deploy |
|-------------|------|---------------|--------------|--------|-------------|
| Development | host78.nird.club | 63081 | 63181 | `dev` | ✅ |
| Production | host74.nird.club | 63080 | 63180 | `main` | ✅ |

### Deployment Architecture

```
GitHub Repository
├── dev branch → GitHub Actions → host78.nird.club:63081
└── main branch → GitHub Actions → host74.nird.club:63080
```

## 🚀 Quick Start

### Prerequisites

1. **GitHub Repository Setup**
   - Repository must be hosted on GitHub
   - SSH key must be added to repository secrets as `SSH_KEY`

2. **SSH Key Configuration**
   - Add your SSH private key to GitHub repository secrets
   - Key name: `SSH_KEY`
   - Key should have access to both target hosts

### Automatic Deployment

Deployments happen automatically when you push to the respective branches:

- **Development**: Push to `dev` branch → Auto-deploys to host78.nird.club:63081
- **Production**: Push to `main` branch → Auto-deploys to host74.nird.club:63080

### Manual Deployment

You can also trigger deployments manually:

1. Go to GitHub Actions tab in your repository
2. Select "Deploy to Development" or "Deploy to Production"
3. Click "Run workflow"
4. Optionally check "Force deployment" to deploy even without changes

## 📋 GitHub Actions Setup

### 1. Add SSH Key to Repository Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `SSH_KEY`
5. Value: Your SSH private key content (the entire key including headers)

### 2. Workflow Files

The repository includes two GitHub Actions workflows:

- `.github/workflows/deploy-dev.yml` - Development deployment
- `.github/workflows/deploy-prod.yml` - Production deployment

### 3. Environment Protection (Optional)

For production deployments, you can add environment protection:

1. Go to Settings → Environments
2. Create "production" environment
3. Add protection rules (required reviewers, deployment branches, etc.)

## 🔧 Local Development Workflow

### Development Cycle

1. **Make Changes**
   ```bash
   # Work on your local machine
   git checkout dev
   # Make your changes
   git add .
   git commit -m "feat: your changes"
   ```

2. **Deploy to Development**
   ```bash
   git push origin dev
   # GitHub Actions automatically deploys to host78.nird.club:63081
   ```

3. **Test Development Environment**
   ```bash
   curl http://host78.nird.club:63081/api
   curl http://host78.nird.club:63081/api/countries/US
   ```

4. **Promote to Production**
   ```bash
   git checkout main
   git merge dev
   git push origin main
   # GitHub Actions automatically deploys to host74.nird.club:63080
   ```

## 📊 Monitoring Deployments

### GitHub Actions Logs

1. Go to Actions tab in your GitHub repository
2. Click on the latest workflow run
3. Expand the deployment steps to see detailed logs

### Application Health Checks

The deployment workflows include automatic health checks:

- Tests SSH connectivity
- Verifies application startup
- Checks API endpoint response
- Reports deployment status

### Manual Verification

```bash
# Development
curl http://host78.nird.club:63081/api
curl http://host78.nird.club:63081/api/countries/US

# Production  
curl http://host74.nird.club:63080/api
curl http://host74.nird.club:63080/api/countries/US
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. SSH Connection Failed

**Symptoms**: GitHub Actions fails with SSH connection error

**Solutions**:
- Verify SSH key is correctly added to repository secrets
- Ensure SSH key has access to target hosts
- Check if hosts are accessible from GitHub Actions runners

#### 2. Deployment Verification Failed

**Symptoms**: Deployment completes but health check fails

**Solutions**:
- Check if application is running: `systemctl status countrypuff-{env}`
- Review application logs: `journalctl -u countrypuff-{env} -f`
- Verify port is listening: `netstat -tlnp | grep {port}`

#### 3. Service Start Failed

**Symptoms**: Systemd service fails to start

**Solutions**:
- Check service logs: `journalctl -u countrypuff-{env} --since "10 minutes ago"`
- Verify Python dependencies: Check if all packages in requirements.txt are installed
- Check file permissions: Ensure application user has proper access

### Manual Debugging

If GitHub Actions deployment fails, you can debug manually:

```bash
# SSH into the target host
ssh -i ~/.ssh/your-key root@host78.nird.club  # or host74.nird.club

# Check service status
systemctl status countrypuff-dev  # or countrypuff-prod

# View logs
journalctl -u countrypuff-dev -f  # or countrypuff-prod

# Check if port is listening
netstat -tlnp | grep 63081  # or 63080

# Test application locally on server
curl localhost:63081/api  # or 63080

# Restart service if needed
systemctl restart countrypuff-dev  # or countrypuff-prod
```

## 📁 File Structure

```
countrypuff/
├── .github/workflows/
│   ├── deploy-dev.yml          # Development deployment workflow
│   └── deploy-prod.yml         # Production deployment workflow
├── ansible/
│   ├── deploy.sh               # Local deployment script (alternative)
│   ├── README.md               # Ansible-specific documentation
│   ├── inventories/
│   │   └── hosts.yml           # Host inventory
│   ├── group_vars/
│   │   ├── development.yml     # Development variables
│   │   └── production.yml      # Production variables
│   └── playbooks/
│       ├── deploy.yml          # Main deployment playbook
│       └── templates/
│           └── countrypuff.service.j2  # Systemd service template
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
└── DEPLOYMENT.md              # This file
```

## 🔒 Security Considerations

### SSH Key Management

- Use dedicated SSH keys for deployment
- Rotate SSH keys regularly
- Limit SSH key access to deployment-specific operations

### Application Security

- Application runs as dedicated user (not root)
- Systemd security features enabled:
  - `PrivateTmp=true`
  - `ProtectSystem=strict`
  - `ProtectHome=true`
  - `NoNewPrivileges=true`

### Network Security

- Application binds to all interfaces (0.0.0.0) but relies on external firewall
- No sensitive data in environment variables
- Logs are written to dedicated directory with proper permissions

## 📈 Scaling and Maintenance

### Adding New Environments

1. Add new host to `ansible/inventories/hosts.yml`
2. Create new group variables file in `ansible/group_vars/`
3. Create new GitHub Actions workflow file
4. Update this documentation

### Updating Dependencies

1. Update `requirements.txt`
2. Commit and push to `dev` branch
3. Test in development environment
4. Merge to `main` for production deployment

### Database Migrations (Future)

When database is added:
1. Add migration steps to Ansible playbook
2. Include database backup in deployment process
3. Add rollback procedures

## 🆘 Emergency Procedures

### Rollback Deployment

If a deployment causes issues:

1. **Quick Rollback**: Revert the problematic commit and push
   ```bash
   git revert <commit-hash>
   git push origin main  # or dev
   ```

2. **Manual Rollback**: SSH into server and restart previous version
   ```bash
   ssh -i ~/.ssh/your-key root@host74.nird.club
   cd /opt/prod/countrypuff/src
   git checkout <previous-commit>
   systemctl restart countrypuff-prod
   ```

### Service Recovery

If service is completely down:

```bash
# SSH into affected server
ssh -i ~/.ssh/your-key root@{host}

# Check what's wrong
systemctl status countrypuff-{env}
journalctl -u countrypuff-{env} --since "1 hour ago"

# Try restart
systemctl restart countrypuff-{env}

# If restart fails, check application manually
cd /opt/{env}/countrypuff/src
source ../venv/bin/activate
python app.py  # Check for errors
```

## 📞 Support

For deployment issues:

1. Check GitHub Actions logs first
2. Review this documentation
3. Check application logs on target servers
4. Verify SSH connectivity and permissions

Remember: All deployments are logged and can be reviewed in the GitHub Actions tab of your repository.