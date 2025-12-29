#!/bin/bash
# Quick test script for Google Scholar BibTeX extraction

echo "🧪 Google Scholar BibTeX Extraction - Quick Test"
echo "================================================"
echo ""

# Check if credentials are set
if [ -z "$GOOGLE_EMAIL" ] || [ -z "$GOOGLE_PASSWORD" ]; then
    echo "❌ Error: Credentials not set"
    echo ""
    echo "Please set the following environment variables:"
    echo ""
    echo "  export GOOGLE_SCHOLAR_ID='AUpqepUAAAAJ'"
    echo "  export GOOGLE_EMAIL='your-email@gmail.com'"
    echo "  export GOOGLE_PASSWORD='your-password-here'"
    echo "  export HEADLESS='false'  # Set to 'true' for headless mode"
    echo ""
    echo "Then run this script again: bash scripts/quick_test.sh"
    exit 1
fi

# Set defaults
export GOOGLE_SCHOLAR_ID="${GOOGLE_SCHOLAR_ID:-AUpqepUAAAAJ}"
export BIB_OUTPUT_FILE="${BIB_OUTPUT_FILE:-pub_test.bib}"
export HEADLESS="${HEADLESS:-false}"

echo "📋 Configuration:"
echo "  Scholar ID: $GOOGLE_SCHOLAR_ID"
echo "  Email: $GOOGLE_EMAIL"
echo "  Output File: $BIB_OUTPUT_FILE"
echo "  Headless Mode: $HEADLESS"
echo ""

# Check Python dependencies
echo "🔍 Checking dependencies..."
python3 -c "import selenium, bibtexparser" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install selenium bibtexparser
fi

# Check ChromeDriver
which chromedriver > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ ChromeDriver not found!"
    echo "Please install ChromeDriver:"
    echo "  macOS: brew install chromedriver"
    echo "  Linux: sudo apt-get install chromium-chromedriver"
    exit 1
fi

echo "✅ All dependencies OK"
echo ""

# Run the script
echo "🚀 Starting extraction..."
echo "================================================"
echo ""

python3 scripts/fetch_google_scholar_bib_auth.py

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Test completed successfully!"
    echo ""
    echo "📄 Output file: $BIB_OUTPUT_FILE"
    if [ -f "$BIB_OUTPUT_FILE" ]; then
        ENTRY_COUNT=$(grep -c "^@" "$BIB_OUTPUT_FILE")
        echo "📊 Entries found: $ENTRY_COUNT"
        echo ""
        echo "First few lines:"
        head -20 "$BIB_OUTPUT_FILE"
    fi
else
    echo ""
    echo "================================================"
    echo "❌ Test failed!"
    echo ""
    echo "Please check the error messages above."
    echo "Common issues:"
    echo "  1. Wrong email/password"
    echo "  2. Need to use App Password (if 2FA enabled)"
    echo "  3. Google security check required"
    echo ""
    echo "Try running in non-headless mode to see what's happening:"
    echo "  export HEADLESS='false'"
    echo "  bash scripts/quick_test.sh"
fi

