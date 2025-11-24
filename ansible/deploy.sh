#!/bin/bash

# CountryPuff Deployment Script
# Usage: ./deploy.sh [dev|prod]

set -e

ENVIRONMENT=${1:-dev}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INVENTORY_FILE="$SCRIPT_DIR/inventories/hosts.yml"
PLAYBOOK_FILE="$SCRIPT_DIR/playbooks/deploy.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 CountryPuff Deployment Script${NC}"
echo -e "${BLUE}=================================${NC}"

# Validate environment
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
    echo -e "${RED}❌ Error: Environment must be 'dev' or 'prod'${NC}"
    echo "Usage: $0 [dev|prod]"
    exit 1
fi

# Set target group based on environment
if [[ "$ENVIRONMENT" == "dev" ]]; then
    TARGET_GROUP="development"
    HOST_INFO="host78.nird.club:63081"
else
    TARGET_GROUP="production"
    HOST_INFO="host74.nird.club:63080"
fi

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo -e "   Environment: ${GREEN}$ENVIRONMENT${NC}"
echo -e "   Target Group: ${GREEN}$TARGET_GROUP${NC}"
echo -e "   Host: ${GREEN}$HOST_INFO${NC}"
echo -e "   Inventory: ${GREEN}$INVENTORY_FILE${NC}"
echo -e "   Playbook: ${GREEN}$PLAYBOOK_FILE${NC}"
echo ""

# Check if required files exist
if [[ ! -f "$INVENTORY_FILE" ]]; then
    echo -e "${RED}❌ Error: Inventory file not found: $INVENTORY_FILE${NC}"
    exit 1
fi

if [[ ! -f "$PLAYBOOK_FILE" ]]; then
    echo -e "${RED}❌ Error: Playbook file not found: $PLAYBOOK_FILE${NC}"
    exit 1
fi

# Check if ansible is installed
if ! command -v ansible-playbook &> /dev/null; then
    echo -e "${RED}❌ Error: ansible-playbook command not found${NC}"
    echo "Please install Ansible first:"
    echo "  pip install ansible"
    exit 1
fi

# Check SSH key
SSH_KEY="$HOME/.ssh/keys/nirdclub__id_ed25519"
if [[ ! -f "$SSH_KEY" ]]; then
    echo -e "${YELLOW}⚠️  Warning: SSH key not found at $SSH_KEY${NC}"
    echo "Make sure the SSH key is available for deployment"
fi

echo -e "${BLUE}🔍 Testing connection to target hosts...${NC}"
if ansible -i "$INVENTORY_FILE" "$TARGET_GROUP" -m ping; then
    echo -e "${GREEN}✅ Connection test successful${NC}"
else
    echo -e "${RED}❌ Connection test failed${NC}"
    echo "Please check:"
    echo "  - SSH key is available and correct"
    echo "  - Target host is accessible"
    echo "  - Inventory configuration is correct"
    exit 1
fi

echo ""
echo -e "${BLUE}🚀 Starting deployment...${NC}"
echo ""

# Run the deployment
ansible-playbook \
    -i "$INVENTORY_FILE" \
    -l "$TARGET_GROUP" \
    "$PLAYBOOK_FILE" \
    --diff \
    -v

if [[ $? -eq 0 ]]; then
    echo ""
    echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
    echo -e "${GREEN}🌍 Application should be available at: http://$HOST_INFO${NC}"
    echo ""
    echo -e "${BLUE}📋 Next steps:${NC}"
    echo "  - Test the application: curl http://$HOST_INFO/api"
    echo "  - Check service status: systemctl status countrypuff-$ENVIRONMENT"
    echo "  - View logs: journalctl -u countrypuff-$ENVIRONMENT -f"
else
    echo ""
    echo -e "${RED}❌ Deployment failed!${NC}"
    echo "Check the output above for error details."
    exit 1
fi