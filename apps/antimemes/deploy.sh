#!/bin/sh
# Assemble build/antimemes (site + gate) and deploy the private preview to Vercel.
set -e
cd "$(dirname "$0")/../.."
python3 apps/antimemes/build.py
rm -rf build/antimemes && mkdir -p build/antimemes
cp -R apps/antimemes/site/. build/antimemes/
cp apps/antimemes/deploy/middleware.js apps/antimemes/deploy/vercel.json build/antimemes/
cd build/antimemes && vercel deploy --prod --yes --scope omniharmonics-projects "$@"
