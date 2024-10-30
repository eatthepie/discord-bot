#!/bin/bash
# Install dependencies
apt-get update
apt-get install -y python3-pip git

# Clone your repository or copy files
git clone YOUR_REPO_URL  # if using git
# or create directory and copy files
mkdir -p /opt/eth-monitor
cd /opt/eth-monitor

# Install Python requirements
pip3 install web3 python-dotenv requests

# Create service file
cat > /etc/systemd/system/eth-monitor.service << EOF
[Unit]
Description=Ethereum Monitor Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/eth-monitor/monitor.py
WorkingDirectory=/opt/eth-monitor
Environment="ETH_NODE_URL=https://mainnet.infura.io/v3/e0be1bb2fb644b8e9020c688b0783f1f"
Environment="TICKETS_WEBHOOK_URL=https://discord.com/api/webhooks/1301260129231962172/INZq6heGnv6oZpfz9jvfdMYLKL-euIbq_yHKBAQXVd8zlfxleqsYjAQTn3O_xpdFL_Es"
Environment="EVENTS_WEBHOOK_URL=https://discord.com/api/webhooks/1301260222064754869/qf42-dHPvubrGbMWminTP2X1oEStRWHHnQ1GRFndsMb-Ovwpz7BuJYM0rYvVsJFrqw-0"
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl enable eth-monitor
systemctl start eth-monitor