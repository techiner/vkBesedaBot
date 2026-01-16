# VK Beseda Bot

Telegram-like bot for VKontakte with phrase triggers, AI responses, and scheduled messages.

## Features

- **Phrase Triggers**: Bot responds to configured trigger phrases
- **AI Integration**: Uses AI service for answering questions
- **Scheduled Messages**: Daily jokes and quotes distribution
- **Subscription System**: Groups can subscribe to daily content
- **Command System**: Various commands for managing bot behavior

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vkBesedaBot
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Fill in your credentials in `.env`:
```
TOKEN=your_vk_bot_token
GROUP_ID=your_group_id
NEUROAPI_API_KEY=your_neuroapi_key
```

6. Initialize database (optional):
```bash
python scripts/init_db.py
```

## Usage

Run the bot:
```bash
python -m src.bot.main
```

Or use the run script:
```bash
bash scripts/run.sh
```

## Project Structure

```
vkBesedaBot/
├── src/bot/              # Main application code
│   ├── config/           # Configuration and settings
│   ├── vk/              # VK API client and utilities
│   ├── handlers/        # Event handlers and dispatcher
│   ├── commands/        # Command handlers
│   ├── services/        # Business logic services
│   ├── storage/         # Data storage modules
│   ├── scheduler/       # Scheduled tasks
│   └── utils/           # Utility functions
├── data/                # Data files (JSON, CSV, DB)
├── scripts/             # Utility scripts
└── requirements.txt     # Python dependencies
```

## Commands

- `help` - Show available commands
- `добавить "ключ" "ответ"` - Add trigger phrase
- `удалить "ключ"` - Remove trigger phrase
- `подписаться "шутки"` - Subscribe to daily jokes
- `окейалеша <вопрос>` - Ask AI a question

## License

MIT

