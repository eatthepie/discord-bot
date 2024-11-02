# Repository Structure

```
discord-bot/
├── .env.example
├── requirements.txt
├── monitor/
│   ├── monitor.py
│   ├── historical_monitor.py
│   ├── contract_abi.py
│   └── setup-monitor.sh
├── bot/
│   ├── status_bot.py
│   └── setup-bot.sh
└── systemd/
    ├── eth-monitor.service
    └── discord-bot.service
```

# Quick Deploy Steps

```bash
# Clone repository
git clone https://github.com/eatthepie/discord-bot.git
cd discord-bot

# Permissions
chmod +x monitor/setup-monitor.sh
chmod +x bot/setup-bot.sh

# Setup monitor
sudo ./monitor/setup-monitor.sh

# Setup bot
sudo ./bot/setup-bot.sh

# Configure environment variables
sudo nano /opt/eth-monitor/.env
sudo nano /opt/discord-bot/.env

# Start services
sudo systemctl start eth-monitor discord-bot
```

# To update after changes

### Pull latest changes

git pull

### Redeploy monitor

sudo ./monitor/setup-monitor.sh

### Redeploy bot

sudo ./bot/setup-bot.sh

### Restart services

sudo systemctl restart eth-monitor discord-bot
