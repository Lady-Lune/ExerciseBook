#!/bin/bash
set -e  # Exit on error
# Today's date
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo ""
echo "============================================================"
echo "Price Tracker"
echo "============================================================"
echo ""
echo "Scraping Etsy listings..."
# Create data directory if needed
mkdir -p data/daily
# Run scraper
scrapy crawl etsy-bitsy -O "data/daily/listing-$TODAY.json" --nolog
echo "   ✅ Scrape complete"
echo ""
echo "Combining price history..."
python3 combiner.py
echo ""
echo "Checking for price drops..."
python3 price_checker.py
