
cd ~/vkBesedaBot
source .venv/bin/activate

sudo systemctl daemon-reload
sudo systemctl enable vk_bot
sudo systemctl start vk_bot

