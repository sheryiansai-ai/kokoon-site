#!/bin/bash
# Publish the site: commit everything, push main, merge into gh-pages, push.
# Usage: bash tools/deploy.sh "what changed"
set -e
cd "$(dirname "$0")/.."
MSG="${1:-Update site}"
git checkout -q main
git add -A
git commit -q -m "$MSG" || echo "nothing to commit"
git push -q origin main
git checkout -q gh-pages && git merge -q main && git push -q origin gh-pages && git checkout -q main
echo "DEPLOYED $(git rev-parse --short HEAD) → https://sheryiansai-ai.github.io/kokoon-site/"
