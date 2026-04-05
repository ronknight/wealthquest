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

# 2.1 Set Android API Level (Required for Rust/Maturin packages like pydantic-core)
API_LEVEL=$(getprop ro.build.version.sdk)
if [ -n "$API_LEVEL" ]; then
    echo "📱 Detected Android API Level: $API_LEVEL"
    export ANDROID_API_LEVEL=$API_LEVEL
else
    echo "⚠️ Could not detect Android API level. Defaulting to 24 (Termux standard)."
    export ANDROID_API_LEVEL=24
fi

# 3. Install Python packages
echo "🐍 Installing Python dependencies from requirements.txt..."
pip install --upgrade pip
if ! pip install -r requirements.txt; then
    echo "❌ Standard install failed. Retrying with --no-build-isolation if possible..."
    pip install -r requirements.txt --no-build-isolation
fi

# 4. Ensure scripts are executable
echo "📜 Setting permissions for start/stop scripts..."
chmod +x start.sh stop.sh

# 5. Initialize Database
echo "💾 Initializing database tables..."
export PYTHONPATH=$PYTHONPATH:.
if python3 -c "from src.models.database import create_tables; create_tables(); print('✅ Database tables initialized.')"; then
    echo "✨ Initialization Complete!"
else
    echo "❌ Database initialization failed. Ensure dependencies are correctly installed."
fi
echo "🚀 You can now start the quest with: ./start.sh"
echo "📱 Use the 'Connect' section in the Admin tab to view on other devices."
