# Ethereum Lottery Monitor

A monitoring service that watches Ethereum smart contract events and posts notifications to Discord channels. Currently monitoring contract `0x043c9ae2764B5a7c2d685bc0262F8cF2f6D86008` for lottery events.

## Project Structure

```
eth-lottery-monitor/
├── monitor.py          # Main monitoring script
├── contract_abi.py     # Contract ABI definition
└── requirements.txt    # Python dependencies
```

## Local Development Setup

1. Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create Discord webhooks:

- Go to Discord server
- Edit Channel -> Integrations -> Create Webhook
- Create two webhooks:
  - One for ticket purchases
  - One for other game events
- Save the webhook URLs

3. Run locally:

```bash
export ETH_NODE_URL='your_ethereum_node_url'
export TICKETS_WEBHOOK_URL='your_tickets_webhook'
export EVENTS_WEBHOOK_URL='your_events_webhook'
python monitor.py
```

## Google Cloud Deployment

### Initial Setup

1. Install Google Cloud SDK:

- Download from https://cloud.google.com/sdk/docs/install
- Initialize: `gcloud init`

2. Create GCP project:

```bash
gcloud projects create PROJECT_ID
gcloud config set project PROJECT_ID
gcloud services enable compute.googleapis.com
```

3. Create VM:

```bash
gcloud compute instances create eth-monitor \
    --project=PROJECT_ID \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --boot-disk-size=10GB
```

### Deployment Steps

1. Copy files to VM:

```bash
gcloud compute scp monitor.py eth-monitor:/opt/eth-monitor/ --zone=us-central1-a
gcloud compute scp contract_abi.py eth-monitor:/opt/eth-monitor/ --zone=us-central1-a
```

2. SSH into VM:

```bash
gcloud compute ssh eth-monitor --zone=us-central1-a
```

3. Install dependencies:

```bash
sudo apt-get update
sudo apt-get install -y python3-pip
sudo pip3 install web3 python-dotenv requests
```

4. Create service file:

```bash
sudo tee /etc/systemd/system/eth-monitor.service << EOF
[Unit]
Description=Ethereum Monitor Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/eth-monitor/monitor.py
WorkingDirectory=/opt/eth-monitor
Environment=ETH_NODE_URL=your_ethereum_node_url
Environment=TICKETS_WEBHOOK_URL=your_tickets_webhook
Environment=EVENTS_WEBHOOK_URL=your_events_webhook
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
```

5. Start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable eth-monitor
sudo systemctl start eth-monitor
```

### Maintenance Commands

Monitor logs:

```bash
sudo journalctl -u eth-monitor -f
```

Service control:

```bash
# Stop monitor
sudo systemctl stop eth-monitor

# Start monitor
sudo systemctl start eth-monitor

# Restart monitor
sudo systemctl restart eth-monitor

# Check status
sudo systemctl status eth-monitor
```

### Updating Code

1. Update local files
2. Upload to VM:

```bash
gcloud compute scp monitor.py eth-monitor:/opt/eth-monitor/ --zone=us-central1-a
```

3. Restart service:

```bash
gcloud compute ssh eth-monitor --zone=us-central1-a
sudo systemctl restart eth-monitor
```

### Cleaning Up

To stop and delete everything:

```bash
# Stop VM
gcloud compute instances stop eth-monitor --zone=us-central1-a

# Delete VM
gcloud compute instances delete eth-monitor --zone=us-central1-a

# Delete project (optional, will delete everything in the project)
gcloud projects delete PROJECT_ID
```

## Environment Variables

- `ETH_NODE_URL`: Your Ethereum node URL (Infura, Alchemy, etc.)
- `TICKETS_WEBHOOK_URL`: Discord webhook for ticket purchases
- `EVENTS_WEBHOOK_URL`: Discord webhook for other game events

## Events Monitored

- `TicketPurchased`: New lottery ticket purchases
- `DrawInitiated`: Start of new lottery draws
- `RandomSet`: When RANDAO value is set
- `VDFProofSubmitted`: VDF proof submissions
- `GamePrizePayoutInfo`: Prize pool information

## Troubleshooting

1. Check logs for errors:

```bash
sudo journalctl -u eth-monitor -f
```

2. Verify environment variables:

```bash
sudo systemctl status eth-monitor
```

3. Test Discord webhooks:

```python
import requests
requests.post(webhook_url, json={"content": "Test message"})
```

4. Check Ethereum node connection:

```python
from web3 import Web3
w3 = Web3(Web3.HTTPProvider(node_url))
print(w3.is_connected())
```

## Notes

- The monitor runs continuously with automatic restart on failure
- Logs are stored in systemd journal
- Uses about 256MB of memory
- Polls for new events every 12 seconds (average Ethereum block time)
