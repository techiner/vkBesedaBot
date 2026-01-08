#!/bin/bash

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и зависимостей
sudo apt install python3 python3-pip python3-venv git -y

# Создание папки бота
mkdir -p ~/vkBesedaBot
cd ~/vkBesedaBot

# Виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей (если есть requirements.txt)
pip install -r requirements.txt

# Создание systemd-сервиса
sudo tee /etc/systemd/system/vk_bot.service > /dev/null <<EOF
[Unit]
Description=VK Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/vkBesedaBot
ExecStart=/root/vkBesedaBot/venv/bin/python3 /root/vkBesedaBot/main.py
Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable vk_bot
sudo systemctl start vk_bot

echo "Бот установлен и запущен!"