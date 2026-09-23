#!/usr/bin/env bash
# Universal 1-Line Installer for jev-pilot
# Works across Linux, macOS, WSL for humans and AI agents.
set -e

echo "🚀 Installing jev-pilot..."
python3 -m pip install --quiet --upgrade git+https://github.com/h0j5bz0adh0-stack/jev-pilot.git

if [ -n "$1" ]; then
    echo "🔑 Configuring API key..."
    python3 -m jev_pilot.setup "$1"
else
    echo "✨ jev-pilot installed successfully!"
    echo "To configure your key later, run: python3 -m jev_pilot.setup <your_api_key>"
fi
