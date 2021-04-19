# Aidabot
A Telegram bot that generates neural network content (images with StyleGAN and text with GPT-2) and posts to your channel using aiogram, Redis queue and Docker.

# Installation
1. Clone the code.
2. Download a trained StyleGAN model in the ./stylegan/src/ directory. An example model can be downloaded here: https://www.dropbox.com/s/mi9bbspwa724quc/network-snapshot-011170.pkl
3. In ./aida/src/aida.py change the MY_CHANNEL constant to the name of your Telegram channel where the bot is supposed to post (*not to the bot name!*). The bot should be added as an admin to this channel.
4. Put the bot access token to ./token.txt
5. Run:
```
docker-compose build
docker-compose up
```