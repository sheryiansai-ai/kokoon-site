#!/bin/bash
# One-time: turn this folder into a clone of the GitHub repo without re-downloading the files.
# Run from the project folder:  bash tools/connect-github.sh
set -e
cd "$(dirname "$0")/.."
[ -d .git ] && { echo "Already a git repo."; exit 0; }
git init -q
git remote add origin https://github.com/sheryiansai-ai/kokoon-site.git
git fetch -q origin
git checkout -q -b main origin/main 2>/dev/null || git reset -q --hard origin/main
git branch -q --track gh-pages origin/gh-pages 2>/dev/null || true
git status --short | head
echo "Connected to origin/main. Deploy with: bash tools/deploy.sh \"message\""
