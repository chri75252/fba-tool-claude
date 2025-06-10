#!/bin/bash
echo "🔧 Setting up FBA Tool Development Environment..."

# Development and testing tools
pip install pytest black flake8 isort
pip install selenium selenium-wire undetected-chromedriver
pip install jupyter notebook  # For data analysis
pip install pytest-asyncio pytest-mock

# Enhanced scraping capabilities
pip install scrapy requests-html aiofiles
pip install httpx  # Modern async HTTP client

# Data analysis tools
pip install matplotlib seaborn plotly  # For profit visualization
pip install openpyxl xlswriter  # Excel export capabilities

echo "✅ FBA Development environment ready"