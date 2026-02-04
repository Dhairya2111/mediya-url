# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and Git
sudo apt install python3-pip git -y

# 3. Clone your repo
git clone https://github.com/Dhairya2111/mediya-url.git
cd mediya-url

# 4. Install dependencies
pip3 install -r requirements.txt

# 5. Run bot in background
nohup python3 main.py &