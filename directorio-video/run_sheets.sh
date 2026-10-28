#!/bin/bash
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
python3 sheets_wsl.py "$@"
