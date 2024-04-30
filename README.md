# FTB Server runner in Docker

### Prerequisites

* Docker installed
* Minecraft world folder
* Telegram bot token: https://t.me/BotFather

### Usage

1. Make a `.env` file at the root of this project, with these contents. Replace token with your bot token:

```
TELEGRAM_TOKEN=79845897275:DJKFLDFjDFjKLDFljkDFJLKjfkldDLJK
```

2. Place your `world` folder in `./server-files`
3. Run `docker compose up`
4. Add the server bot to group chat
5. Type `/server aan` in the bot chat to start the server, or `/server` for help