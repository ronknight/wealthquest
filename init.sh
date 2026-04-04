#!/bin/bash
# init.sh - Initialize WealthQuest Environment and Dependencies

echo "⚔️ Initializing WealthQuest Financial Ecosystem..."

# 1. Update system packages (Termux specific)
echo "📦 Updating system packages..."
pkg update -y
pkg upgrade -y

# 2. Install system dependencies
echo "🛠️ Installing system dependencies (Python, SQLite, Termux-API)..."
pkg install -y python sqlite termux-api pkg-config libffi openssl rust

# 3. Install Python packages
echo "🐍 Installing Python dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Ensure scripts are executable
echo "📜 Setting permissions for start/stop scripts..."
chmod +x start.sh stop.sh

# 5. Initialize Database
echo "💾 Initializing database tables..."
python3 -c "from src.models.database import create_tables; create_tables(); print('✅ Database tables initialized.')"

echo ""
echo "✨ Initialization Complete!"
echo "🚀 You can now start the quest with: ./start.sh"
echo "📱 Use the 'Connect' section in the Admin tab to view on other devices."
