# Aidabot
A telegram bot generating neural network content (images with StyleGAN and text with GPT-2) using aiogram, Redis queue and Docker.

# Installation
1. Clone the code.
2. Download a trained StyleGAN model in the ./stylegan/src/ directory. An example model can be downloaded here: https://www.dropbox.com/s/mi9bbspwa724quc/network-snapshot-011170.pkl
3. In ./aida/scr/aida.py change the channel name to your Telegram channel
4. Put the bot access token to ./token.txt
5. Run:
```
docker-compose build
docker-compose up
```