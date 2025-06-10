#!/bin/bash
echo "🏥 FBA Tool Health Check"
echo "======================="

# Check Python environment
echo "Checking Python environment..."
python -c "
import sys
import openai, aiohttp, bs4, pandas, playwright
print(f'✅ Python {sys.version_info.major}.{sys.version_info.minor}')
print('✅ All core imports successful')
" || echo "❌ Python environment issues"

# Check Chrome debug port
echo "Checking Chrome debug port..."
curl -s http://localhost:9222/json >nul 2>&1 && echo "✅ Chrome debug port active" || echo "❌ Chrome debug port not responding"

# Check directories (Windows paths)
echo "Checking directories..."
if [ -d "OUTPUTS/FBA_ANALYSIS" ]; then echo "✅ Output directories exist"; else echo "❌ Missing output directories"; fi

# Check config files
echo "Checking configuration..."
if [ -f "config/system_config.json" ]; then echo "✅ System config exists"; else echo "❌ Missing system config"; fi

echo "Health check complete!"
