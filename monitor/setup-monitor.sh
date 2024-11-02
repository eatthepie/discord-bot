#!/bin/bash
set -e

# Configuration
INSTALL_DIR="/opt/eth-monitor"
ENV_FILE="${INSTALL_DIR}/.env"

echo "Setting up Ethereum Monitor..."

# Install dependencies
apt-get update
apt-get install -y python3-pip python3-venv

# Create installation directory if it doesn't exist
mkdir -p ${INSTALL_DIR}

# Copy monitor files
cp monitor/*.py ${INSTALL_DIR}/
cp requirements.txt ${INSTALL_DIR}/
cp .env ${INSTALL_DIR}/

# Setup Python virtual environment
cd ${INSTALL_DIR}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment file if it doesn't exist
if [ ! -f ${ENV_FILE} ]; then
    echo "Creating example .env file..."
    echo "ETH_NODE_URL='your_ethereum_node_url'" > ${ENV_FILE}
    echo "TICKETS_WEBHOOK_URL='your_tickets_webhook'" >> ${ENV_FILE}
    echo "EVENTS_WEBHOOK_URL='your_events_webhook'" >> ${ENV_FILE}
fi

# Install systemd service
cp systemd/eth-monitor.service /etc/systemd/system/
systemctl daemon-reload

# Set permissions
chown -R root:root ${INSTALL_DIR}
chmod -R 755 ${INSTALL_DIR}
chmod 600 ${ENV_FILE}

echo "Ethereum Monitor setup complete!"
echo "1. Edit your configuration: sudo nano ${ENV_FILE}"
echo "2. Start service: sudo systemctl start eth-monitor"
echo "3. View logs: sudo journalctl -u eth-monitor -f"