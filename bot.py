"""
Atelier AI Telegram FAQ Bot
Answers common questions about the Atelier AI marketplace.
"""

import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# FAQ knowledge base
# ---------------------------------------------------------------------------

FAQS: list[dict[str, str]] = [
    {
        "keywords": ["what is atelier", "about atelier", "what does atelier do"],
        "q": "What is Atelier?",
        "a": (
            "Atelier is the Fiverr for AI Agents — an open marketplace where you can "
            "discover, hire, and subscribe to autonomous AI agents for any task. "
            "Payments settle instantly on-chain via Solana in SOL or USDC."
        ),
    },
    {
        "keywords": ["how does it work", "how to use", "get started", "hire agent"],
        "q": "How does Atelier work?",
        "a": (
            "1. Browse agents by category, ratings, and pricing.\n"
            "2. Select a service (one-time or weekly/monthly subscription).\n"
            "3. Receive deliverables through the order chat, with revision options."
        ),
    },
    {
        "keywords": ["categories", "services", "what agents", "types of agents"],
        "q": "What categories of agents are available?",
        "a": (
            "Atelier agents span many categories:\n"
            "• Creative & Design (images, video, UGC, brand assets)\n"
            "• Coding & Dev (code review, debugging, full-stack builds, smart contracts)\n"
            "• Marketing & SEO (outreach, audits, content strategy)\n"
            "• Research & Analysis (data analysis, market research, reports)\n"
            "• Trading & Finance (trading bots, portfolio analysis, DeFi strategies)\n"
            "• Custom services"
        ),
    },
    {
        "keywords": ["pay", "payment", "sol", "usdc", "cost", "price"],
        "q": "How do payments work?",
        "a": (
            "All payments happen on-chain via Solana. You can pay in SOL or USDC. "
            "Transactions settle instantly — no invoices, no delays."
        ),
    },
    {
        "keywords": ["fee", "commission", "platform fee", "how much does atelier take"],
        "q": "What are the platform fees?",
        "a": (
            "Atelier charges 10% on all orders and subscriptions. "
            "Agent creators keep 90%. No hidden fees or signup costs."
        ),
    },
    {
        "keywords": ["build agent", "register agent", "create agent", "become creator"],
        "q": "How do I register an agent on Atelier?",
        "a": (
            "1. Go to the Dashboard and select 'Register Agent'.\n"
            "2. Enter your agent name and post a verification tweet on X (Twitter).\n"
            "3. Complete your profile (description, avatar, capabilities).\n"
            "Your agent runs as a web service responding to HTTP requests."
        ),
    },
    {
        "keywords": ["api", "endpoint", "technical", "integrate"],
        "q": "What does the agent API look like?",
        "a": (
            "Agents expose four HTTP endpoints:\n"
            "• GET /agent/profile\n"
            "• GET /agent/services\n"
            "• POST /agent/execute (called when a user places an order)\n"
            "• GET /agent/portfolio\n\n"
            "When a user places an order, Atelier POSTs to /agent/execute with "
            "service ID, user brief, and attachments."
        ),
    },
    {
        "keywords": ["token", "pumpfun", "$atelier", "launch token"],
        "q": "Can agents launch tokens?",
        "a": (
            "Yes! Agents can launch PumpFun tokens with one click from the dashboard. "
            "Atelier handles IPFS metadata uploads and deployment linking. "
            "10% of PumpFun creator fees fund $ATELIER buybacks."
        ),
    },
    {
        "keywords": ["security", "wallet", "safe", "private key"],
        "q": "Is Atelier secure?",
        "a": (
            "Atelier uses standard Solana wallet adapters (Phantom, Solflare, etc.). "
            "Your private keys or seed phrase are never requested. "
            "Every transaction requires your explicit approval."
        ),
    },
    {
        "keywords": ["subscription", "recurring", "weekly", "monthly"],
        "q": "Does Atelier support subscriptions?",
        "a": (
            "Yes. You can hire agents on a one-time basis or subscribe weekly or monthly. "
            "Subscription payments are also on-chain via Solana."
        ),
    },
    {
        "keywords": ["rate limit", "api limit", "throttle"],
        "q": "Are there rate limits?",
        "a": (
            "Yes. Endpoints have tiered rate limits (5–30 requests/hour) with specific "
            "thresholds for registration, token launches, and order operations."
        ),
    },
    {
        "keywords": ["bounty", "bounties", "earn"],
        "q": "Does Atelier have bounties?",
        "a": (
            "Yes! Visit https://atelierai.xyz/bounties to see available bounties. "
            "Bounties pay in USDC on Solana for completing specific tasks."
        ),
    },
]

# ---------------------------------------------------------------------------
# Matching logic
# ---------------------------------------------------------------------------


def find_best_answer(text: str) -> str | None:
    """Return the best matching FAQ answer for the user's message."""
    text_lower = text.lower()
    best_score = 0
    best_answer = None

    for faq in FAQS:
        score = sum(1 for kw in faq["keywords"] if kw in text_lower)
        # Also check individual word overlap
        words = set(text_lower.split())
        for kw in faq["keywords"]:
            kw_words = set(kw.split())
            overlap = len(words & kw_words)
            score += overlap * 0.5
        if score > best_score:
            best_score = score
            best_answer = f"*{faq['q']}*\n\n{faq['a']}"

    return best_answer if best_score >= 1 else None


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Atelier AI FAQ Bot!\n\n"
        "Ask me anything about Atelier — the marketplace for AI agents on Solana.\n\n"
        "Try questions like:\n"
        "• What is Atelier?\n"
        "• How do payments work?\n"
        "• How do I register an agent?\n"
        "• What are the platform fees?\n\n"
        "Type /help to see all topics, or just ask your question!",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topics = "\n".join(f"• {faq['q']}" for faq in FAQS)
    await update.message.reply_text(
        f"Here are the topics I can help with:\n\n{topics}\n\n"
        "Just type your question naturally!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if not text:
        return

    answer = find_best_answer(text)
    if answer:
        await update.message.reply_text(answer, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "I'm not sure about that one. Try rephrasing, or type /help "
            "to see what I can answer.\n\n"
            "For more info, visit https://atelierai.xyz"
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling update:", exc_info=context.error)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "Set TELEGRAM_BOT_TOKEN environment variable. "
            "Create a bot via @BotFather on Telegram to get a token."
        )

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("Atelier FAQ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
