# Atelier AI Telegram FAQ Bot

A Telegram bot that answers frequently asked questions about the [Atelier AI](https://atelierai.xyz) marketplace — the Fiverr for AI Agents on Solana.

## Features

- Answers 12+ common questions about Atelier (what it is, payments, fees, agent registration, API, tokens, security, etc.)
- Keyword-based matching with fuzzy scoring
- `/start` welcome message and `/help` topic listing
- Lightweight, no external DB required

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the bot token

### 2. Run Locally

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="your-token-here"
python bot.py
```

### 3. Run with Docker

```bash
docker build -t atelier-faq-bot .
docker run -e TELEGRAM_BOT_TOKEN="your-token-here" atelier-faq-bot
```

## FAQ Topics Covered

- What is Atelier?
- How does Atelier work?
- Agent categories
- Payments (SOL/USDC)
- Platform fees (10%)
- Agent registration
- Agent API endpoints
- Token launches (PumpFun)
- Security & wallets
- Subscriptions
- Rate limits
- Bounties

## Tech Stack

- Python 3.12+
- [python-telegram-bot](https://python-telegram-bot.org/) v21

## License

MIT
