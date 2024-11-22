#!/bin/bash
set -e

# Configuration
INSTALL_DIR="/opt/discord-bot"
ENV_FILE="${INSTALL_DIR}/.env"

echo "Setting up Multi-Chain Discord Bot..."

# Install dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3-pip python3-venv

# Create installation directory if it doesn't exist
echo "Creating installation directory..."
mkdir -p ${INSTALL_DIR}

# Copy bot files
echo "Copying bot files..."
cp bot/*.py ${INSTALL_DIR}/
cp requirements.txt ${INSTALL_DIR}/
cp .env ${INSTALL_DIR}/

# Setup Python virtual environment
echo "Setting up Python virtual environment..."
cd ${INSTALL_DIR}
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies with verbose output
echo "Installing Python dependencies..."
pip install -v pip --upgrade
pip install -v -r requirements.txt

# Setup environment file if it doesn't exist
if [ ! -f ${ENV_FILE} ]; then
    echo "Creating example .env file..."
    cat > ${ENV_FILE} << EOL
# Ethereum Network Configuration
ETH_NODE_URL='your_ethereum_node_url'
ETH_CONTRACT_ADDRESS='0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008'
ETH_GAME_BOT_TOKEN='your_ethereum_game_bot_token'
ETH_PRIZE_BOT_TOKEN='your_ethereum_prize_bot_token'

# World Chain Network Configuration
WORLD_NODE_URL='your_world_chain_node_url'
WORLD_CONTRACT_ADDRESS='your_world_chain_contract_address'
WORLD_GAME_BOT_TOKEN='your_world_chain_game_bot_token'
WORLD_PRIZE_BOT_TOKEN='your_world_chain_prize_bot_token'
EOL
fi

# Install systemd service
echo "Installing systemd service..."
cat > /etc/systemd/system/discord-bot.service << EOL
[Unit]
Description=Multi-Chain Discord Status Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=${INSTALL_DIR}
Environment=PATH=${INSTALL_DIR}/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=${INSTALL_DIR}/venv/bin/python3 ${INSTALL_DIR}/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

systemctl daemon-reload

# Set permissions
echo "Setting permissions..."
chown -R root:root ${INSTALL_DIR}
chmod -R 755 ${INSTALL_DIR}
chmod 600 ${ENV_FILE}

echo "Multi-Chain Discord Bot setup complete!"
echo "Please follow these steps:"
echo "1. Edit your configuration: sudo nano ${ENV_FILE}"
echo "2. Make sure to fill in all required environment variables for both networks"
echo "3. Start service: sudo systemctl start discord-bot"
echo "4. Enable service to start on boot: sudo systemctl enable discord-bot"
echo "5. View logs: sudo journalctl -u discord-bot -f"
echo ""
echo "Required environment variables:"
echo "- ETH_NODE_URL"
echo "- ETH_GAME_BOT_TOKEN"
echo "- ETH_PRIZE_BOT_TOKEN"
echo "- WORLD_NODE_URL"
echo "- WORLD_CONTRACT_ADDRESS"
echo "- WORLD_GAME_BOT_TOKEN"
echo "- WORLD_PRIZE_BOT_TOKEN"