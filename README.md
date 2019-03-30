# Carousell Telebot

Telegram notifier for snatching the best deals on Carousell.

## Why?

Yes.

## How does it work?

Carousell uses Fluxible for server-side rendering (SSR). This is very nice because we can parse the React props in the `<script>` tag as JSON to a Python dictionary.

The nested objects that this project need have the keys of `"productsMap"` and `"PRODUCTS_BROWSE"`. They happen to be valid JSON (no functions as values) so we can treat it as such and use the `json.loads()` function.

## How do I run this myself?

1. Download this repository

2. Run this in the terminal:
```
python3 -m venv /path/to/new/virtual/env
. env/bin/activate
pip install -r requirements.txt
python setup.py
```

## `credentials.json` format:

```
{
  "bot_token": "INSERT_BOT_TOKEN",
  "chat_id": 12345215
}
```

## Where can I get my chat_id?

Try changing the handler code to `print(message.chat.id)`.

## Can I follow multiple keywords?

Not now.

## I would like to hire you.

Send me an email at dexter@dexterleng.com
