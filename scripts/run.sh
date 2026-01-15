
cd ~/vkBesedaBot
source .venv/bin/activate

sudo timedatectl set-timezone Asia/Yekaterinburg

sudo systemctl daemon-reload
sudo systemctl enable vk_bot
sudo systemctl stop vk_bot
sudo systemctl start vk_bot

