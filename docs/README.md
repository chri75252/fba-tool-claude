# Amazon FBA Agent System v3.4 - Complete Documentation

**Version:** 3.4 (Multi-Tier AI-First Fallback System)
**Date:** 2025-06-08
**Status:** Production-Ready with AI-First Fallback Ladder

## System Overview

The Amazon FBA Agent System is a sophisticated automation platform that identifies profitable products by scraping supplier websites, matching them with Amazon listings, and calculating profitability metrics.

### System Purpose and Workflow
The system automates the process of finding profitable products for Amazon FBA by:
1. **AI-Driven Category Discovery**: Uses OpenAI to intelligently suggest supplier categories to scrape
2. **Supplier Product Scraping**: Extracts product data from supplier websites (currently Clearance King UK)
3. **Amazon Product Matching**: Matches supplier products to Amazon listings using EAN/UPC codes and title fallback
4. **Profitability Analysis**: Calculates FBA fees, profit margins, and ROI using Keepa data
5. **Multi-Cycle Operation**: Automatically suggests new categories after processing batches, creating continuous discovery loops until ALL AI-suggested categories are exhausted
6. **Financial Reporting**: Generates comprehensive CSV reports with detailed financial analysis

### Key Features
- **Multi-Cycle AI Category Progression**: System automatically suggests new categories after processing batches
- **Infinite Workflow Operation**: Continuous operation until ALL AI-suggested categories are exhausted (not limited by product counts)
- **Smart Product Matching**: EAN/UPC-based matching with intelligent title fallback
- **Comprehensive Financial Analysis**: Automated FBA calculator execution every 40-50 products
- **State Persistence**: Resume capability with full workflow state management
- **Rate Limiting**: Intelligent timing gaps to prevent API throttling

### Multi-Tier AI-First Fallback System
The system implements a sophisticated three-tier fallback ladder that tries multiple AI approaches before falling back to manual category discovery:

**AI Fallback Ladder Architecture**:
1. **Tier 1 (v2 Mode)**: 25-line clearance-first prompt optimized for arbitrage (Temperature: 0.1)
2. **Tier 2 (Legacy Mode)**: 86-line detailed prompt with comprehensive instructions (Temperature: 0.3)
3. **Tier 3 (Minimal Mode)**: Terse 12-line fallback prompt for final AI attempt (Temperature: 0.5)
4. **Final Fallback**: Dynamic category discovery via homepage scraping (Manual)

**Three Micro-Patches for >99% AI Success Rate**:
- **Function-calling wrapper**: Guaranteed JSON structure via OpenAI tools API
- **Smart back-off on 429/502 errors**: Exponential backoff (1s, 2s, 4s)
- **URL head-check validator**: Prevents hallucinations by validating URLs exist

**Configuration Toggles**:
- `disable_ai_category_selection`: Boolean flag to bypass AI entirely and use dynamic discovery
- `mode`: Primary AI prompt mode selector ("v2", "legacy", "minimal")
- `fallbacks.max_retries`: Number of fallback attempts before manual mode (default: 2)
- `fallbacks.clear_cache_between_retries`: Cache invalidation between AI attempts

**AI Performance Validation**:
- **Phase A Testing**: v2 mode successfully prioritized clearance categories (sales.html, pound-lines.html)
- **URL Validation**: All AI-suggested URLs validated with HTTP 200 responses
- **Zero Overlap**: No overlap between top_3_urls and skip_urls
- **Profit Optimization**: AI correctly avoided low-margin categories (electrical, fashion, books)

## System Requirements

### Prerequisites
- Python 3.8+
- Chrome browser with debug port enabled
- Keepa browser extension installed and configured
- OpenAI API key (hardcoded in scripts)

### Required Chrome Setup
```bash
# Start Chrome with debug port (required for automation)
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile"
```

### Directory Structure
```
Amazon-FBA-Agent-System-v3/
├── config/
│   ├── system_config.json                    # Main configuration file
│   └── supplier_configs/                     # Supplier-specific configurations
├── tools/                                    # Core system components
│   ├── passive_extraction_workflow_latest.py # PRIMARY ENTRY POINT
│   ├── amazon_playwright_extractor.py        # Amazon data extraction
│   ├── configurable_supplier_scraper.py      # Supplier website scraping
│   ├── FBA_Financial_calculator.py           # Financial analysis and CSV generation
│   ├── cache_manager.py                      # Cache management
│   └── utils/                                # Utility modules
├── OUTPUTS/
│   ├── FBA_ANALYSIS/                         # Analysis results and reports
│   │   ├── ai_category_cache/               # AI category suggestions cache
│   │   ├── amazon_cache/                    # Amazon product data cache
│   │   ├── Linking map/                     # Product linking mappings
│   │   ├── fba_financial_report_*.csv       # Financial reports (generated here)
│   │   └── fba_summary_*.json               # FBA summary reports
│   ├── cached_products/                     # Supplier product cache
│   └── AMAZON_SCRAPE/                       # Amazon scraping artifacts
├── docs/                                    # Documentation
│   ├── README.md                            # This file
│   ├── SYSTEM_DEEP_DIVE.md                  # Technical deep dive
│   └── SYSTEM_CONFIG_TOGGLES.md             # Configuration reference
└── Claude.md                                # Session continuity
```

## Configuration Guide

### Main Configuration File: config/system_config.json

**AI FEATURES CONFIGURATION (MULTI-TIER FALLBACK):**
```json
{
  "ai_features": {
    "category_selection": {
      "enabled": true,
      "disable_ai_category_selection": false,
      "mode": "v2",
      "available_modes": {
        "legacy": "Original 86-line prompt with detailed instructions",
        "v2": "New 25-line clearance-first prompt optimized for arbitrage",
        "minimal": "Super terse 12-line prompt for fallback"
      },
      "fallbacks": {
        "max_retries": 2,
        "clear_cache_between_retries": true,
        "alternate_prompts": ["v2", "legacy", "minimal"],
        "temperature_escalation": [0.1, 0.3, 0.5],
        "model_escalation": ["gpt-4o-mini-2024-07-18"]
      },
      "dynamic_reordering": {
        "enabled": false,
        "trigger_interval_categories": 5,
        "trigger_interval_products": 100
      }
    }
  }
}
```

**CORE SYSTEM CONFIGURATION:**
```json
{
  "system": {
    "clear_cache": false,
    "selective_cache_clear": false,
    "force_ai_scraping": true,
    "max_products_per_category": 50,     // Production: 50+, Testing: 3
    "max_analyzed_products": 100         // Production: 100+, Testing: 5
  },
  "processing_limits": {
    "min_price_gbp": 0.1,
    "max_price_gbp": 20.0,
    "max_products_per_run": 0,
    "max_categories_per_cycle": 3
  }
}
```

**Configuration Parameters Explained**:
- `disable_ai_category_selection`: When true, bypasses ALL AI tiers and uses dynamic category discovery
- `mode`: Primary AI prompt mode ("v2", "legacy", "minimal") - system tries this first
- `fallbacks.max_retries`: Number of fallback attempts through the AI ladder (default: 2)
- `fallbacks.alternate_prompts`: Order of prompt modes to try in fallback ladder
- `fallbacks.temperature_escalation`: Temperature values for each tier [0.1, 0.3, 0.5]
- `fallbacks.clear_cache_between_retries`: Cache invalidation between AI attempts for fresh results
- `dynamic_reordering`: Performance-based category re-prioritization (future enhancement)

## Quick Start Guide

### Standard Operation
```bash
# Navigate to system directory
cd "C:\Users\chris\Cloud-Drive_christianhaddad8@gmail.com\Cloud-Drive\Full\claude code\Amazon-FBA-Agent-System-v3"

# Standard run (processes products until max_analyzed_products reached)
python tools\passive_extraction_workflow_latest.py

# Custom product limit
python tools\passive_extraction_workflow_latest.py --max-products 20
```

### Infinite Mode Operation
```bash
# Infinite processing with automatic AI category progression
# Runs until ALL AI-suggested categories are exhausted
python tools\passive_extraction_workflow_latest.py --max-products 0
```

### AI Fallback Ladder Testing
```bash
# Test v2 AI mode with fallback ladder (edit config first: set mode: "v2")
python tools\passive_extraction_workflow_latest.py --max-products 3

# Test manual override mode (edit config first: set disable_ai_category_selection: true)
python tools\passive_extraction_workflow_latest.py --max-products 3

# Validate AI path - clean cache and test v2 mode
rm -f OUTPUTS\FBA_ANALYSIS\ai_category_cache\*json
python tools\passive_extraction_workflow_latest.py --max-products 3
```

### Multi-Cycle AI Testing
```bash
# First, edit config/system_config.json:
# - Set max_products_per_category: 3
# - Set max_analyzed_products: 5
# Then run:
python tools\passive_extraction_workflow_latest.py --max-products 15

# Expected: 3 FBA summaries + 3 CSV files + 3 AI cache entries
```

## Output Files and Locations

### Key Output Directories
- **AI Cache**: `OUTPUTS\FBA_ANALYSIS\ai_category_cache\clearance-king_co_uk_ai_category_cache.json`
  - **Behavior**: Appends new entries (no overwriting existing entries)
  - **Content**: AI-suggested categories with timestamps and scraping history
- **Financial Reports**: `OUTPUTS\FBA_ANALYSIS\fba_financial_report_YYYYMMDD_HHMMSS.csv`
  - **Behavior**: Creates new file each time
  - **Location**: Generated directly in `OUTPUTS\FBA_ANALYSIS\` (not in financial_reports subdirectory)
- **FBA Summaries**: `OUTPUTS\FBA_ANALYSIS\fba_summary_clearance-king_co_uk_YYYYMMDD_HHMMSS.json`
  - **Behavior**: Creates new file each time
  - **Content**: Complete workflow summary with processed product counts
- **Amazon Cache**: `OUTPUTS\FBA_ANALYSIS\amazon_cache\{ASIN}_{EAN}.json`
  - **Behavior**: Creates new file for each product
  - **Naming**: Enhanced filename logic ALWAYS includes supplier context for traceability
- **State Files**: `OUTPUTS\FBA_ANALYSIS\clearance-king_co_uk_processing_state.json`
  - **Behavior**: Same file updated with current processing index
  - **Content**: Last processed product index for resuming operations
- **Linking Map**: `OUTPUTS\FBA_ANALYSIS\Linking map\linking_map.json`
  - **Behavior**: Appends new entries (no overwriting existing entries)
  - **Content**: Confirmed links between supplier products and Amazon ASINs

### File Generation Patterns
- **FBA Summary**: Generated once per workflow completion
- **Financial Report**: Generated every 40-50 products OR at workflow completion
- **AI Cache**: Appends new entries with each AI call (multiple entries in same file)
- **Amazon Cache**: Individual JSON files for each product analyzed, named with ASIN and supplier EAN

## Monitoring Commands

### Check System Status
```bash
# Check AI cache progression
type "OUTPUTS\FBA_ANALYSIS\ai_category_cache\clearance-king_co_uk_ai_category_cache.json"

# Check recent financial reports
dir "OUTPUTS\FBA_ANALYSIS\fba_financial_report_*.csv" /od

# Monitor running processes
tasklist | findstr python
```

### Health Indicators
- **Healthy Operation**: New AI calls every 40-50 products
- **File Generation**: New CSV reports every 40-50 products
- **Memory Usage**: Should remain stable during infinite runs
- **Processing Speed**: ~2-3 products per minute average

## Troubleshooting

### Common Issues

**AI Client Initialization Failures:**
```bash
# Check hardcoded API key in tools\passive_extraction_workflow_latest.py
# Verify internet connectivity
# Test API key manually:
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.openai.com/v1/models
```

**Chrome/Browser Issues:**
```bash
# Restart Chrome with debug port
taskkill /f /im chrome.exe
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebugProfile"
```

**Cache Issues:**
```bash
# Clear all caches and restart
rmdir /s "OUTPUTS\FBA_ANALYSIS\amazon_cache"
rmdir /s "OUTPUTS\FBA_ANALYSIS\ai_category_cache"
del "OUTPUTS\cached_products\*.json"
```

### Recovery Procedures

**Complete System Reset:**
```bash
# Stop all processes
taskkill /f /im python.exe

# Clear all caches
rmdir /s "OUTPUTS\FBA_ANALYSIS"
rmdir /s "OUTPUTS\cached_products"

# Recreate directory structure
mkdir OUTPUTS\FBA_ANALYSIS\ai_category_cache
mkdir OUTPUTS\FBA_ANALYSIS\amazon_cache
mkdir OUTPUTS\cached_products

# Restart with minimal test
python tools\passive_extraction_workflow_latest.py --max-products 5
```

## Important Notes

### Critical Instructions
- **Always use original production scripts** - NEVER generate separate test scripts
- **Always verify by checking actual files** - NEVER trust logs alone
- **Only modify tested configuration parameters** - Leave untested options unchanged
- **Clear AI cache before testing** - Delete ai_category_cache files for fresh starts
- **Use `tools\passive_extraction_workflow_latest.py` directly** - This is the primary entry point
- **AI credentials are hardcoded** - OpenAI API keys stored directly in scripts for reliability

### System Limitations
- Currently supports only Clearance King UK supplier
- Requires manual Chrome setup with debug port
- Keepa extension must be installed and active for fee calculations
- OpenAI API key hardcoded in scripts (no environment variables)

### Script Consolidation Notes
- **Primary Entry Point:** `passive_extraction_workflow_latest.py` contains ALL critical functionality
- **Legacy Entry Point:** `run_complete_fba_analysis.py` is available but not used in current workflow
- **No Missing Functionality:** All critical code snippets, workflow details, and functionality are preserved in the primary script
- **Verified Integration:** All components properly integrate through the primary workflow script

For technical implementation details, see `SYSTEM_DEEP_DIVE.md`
For configuration reference, see `SYSTEM_CONFIG_TOGGLES.md`
For session continuity, see `Claude.md`