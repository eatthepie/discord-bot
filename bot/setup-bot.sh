#!/bin/bash
set -e

# Configuration
INSTALL_DIR="/opt/discord-bot"
ENV_FILE="${INSTALL_DIR}/.env"

echo "Setting up Discord Bot..."

# Install dependencies
apt-get update
apt-get install -y python3-pip python3-venv

# Create installation directory if it doesn't exist
mkdir -p ${INSTALL_DIR}

# Copy bot files
cp bot/*.py ${INSTALL_DIR}/
cp requirements.txt ${INSTALL_DIR}/

# Setup Python virtual environment
cd ${INSTALL_DIR}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment file if it doesn't exist
if [ ! -f ${ENV_FILE} ]; then
    echo "Creating example .env file..."
    echo "ETH_NODE_URL='your_ethereum_node_url'" > ${ENV_FILE}
    echo "GAME_BOT_TOKEN='your_game_bot_token'" >> ${ENV_FILE}
    echo "PRIZE_BOT_TOKEN='your_prize_bot_token'" >> ${ENV_FILE}
fi

# Install systemd service
cp systemd/discord-bot.service /etc/systemd/system/
systemctl daemon-reload

# Set permissions
chown -R root:root ${INSTALL_DIR}
chmod -R 755 ${INSTALL_DIR}
chmod 600 ${ENV_FILE}

echo "Discord Bot setup complete!"
echo "1. Edit your configuration: sudo nano ${ENV_FILE}"
echo "2. Start service: sudo systemctl start discord-bot"
echo "3. View logs: sudo journalctl -u discord-bot -f"