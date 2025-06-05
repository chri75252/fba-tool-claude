# System Configuration Toggles Reference

## Overview
This document provides a comprehensive reference for all configuration toggles in `config/system_config.json`, including their purpose, tested status, and usage guidelines.

## Configuration File Structure

### Main Configuration File: `config/system_config.json`

```json
{
  "system": {
    "clear_cache": false,
    "selective_cache_clear": false,
    "force_ai_scraping": true,
    "clear_failed_extractions": false,
    "max_products_per_category": 50,
    "max_analyzed_products": 100,
    "enable_supplier_parser": false,
    "test_mode": false,
    "bypass_ai_scraping": false,
    "enable_system_monitoring": true
  },
  "integrations": {
    "openai": {
      "enabled": true,
      "api_key": "sk-02XZ3ucKVViULVaTp4_Ad6byZCT6Fofr-BwRsD5mTcT3BlbkFJ7_HTmTRScAn0m-ITc_CX5a2beXTOcbK1-Qmm0s6nwA",
      "model": "gpt-4o-mini-search-preview-2025-03-11",
      "web_search_enabled": true
    }
  }
}
```

## System Configuration Toggles

### ✅ TESTED AND VERIFIED SETTINGS

#### `clear_cache` (boolean)
- **Purpose**: Controls whether to clear all cache files at system startup
- **Default**: `false`
- **Tested Values**: `true`, `false`
- **Usage**: 
  - `false`: Preserves existing cache data for efficiency (RECOMMENDED)
  - `true`: Clears all cache files for fresh start
- **Impact**: When `true`, removes supplier cache, Amazon cache, and linking map files

#### `force_ai_scraping` (boolean)
- **Purpose**: Forces AI category suggestions regardless of cache state
- **Default**: `true`
- **Tested Values**: `true`, `false`
- **Usage**: 
  - `true`: Always allows AI category suggestions (RECOMMENDED)
  - `false`: May skip AI suggestions if cache exists
- **Impact**: Essential for multi-cycle AI category progression

#### `clear_failed_extractions` (boolean)
- **Purpose**: Removes Amazon cache files with failed Keepa extractions
- **Default**: `false`
- **Tested Values**: `true`, `false`
- **Usage**:
  - `true`: Automatically clears failed Keepa extractions
  - `false`: Preserves all cache files regardless of extraction status
- **Impact**: Helps maintain clean cache by removing files with timeout/failed status

#### `max_products_per_category` (integer)
- **Purpose**: Controls how many products to process per AI-suggested category
- **Default**: `50`
- **Tested Values**: `3` (testing), `50` (production)
- **Usage**:
  - Testing: `3` for quick multi-cycle verification
  - Production: `50+` for efficient operation
- **Impact**: Affects frequency of category switching

#### `max_analyzed_products` (integer)
- **Purpose**: Controls when to trigger new AI category suggestions
- **Default**: `100`
- **Tested Values**: `5` (testing), `100` (production)
- **Usage**:
  - Testing: `5` for frequent AI calls
  - Production: `100+` for efficient operation
- **Impact**: Determines AI suggestion frequency

### ⚠️ UNTESTED CONFIGURATION OPTIONS - DO NOT MODIFY

#### `selective_cache_clear` (boolean)
- **Purpose**: Enables selective cache clearing instead of full clear
- **Default**: `false`
- **Status**: **UNTESTED - DO NOT CHANGE**
- **Warning**: Complex selective clearing logic not verified

#### `enable_supplier_parser` (boolean)
- **Purpose**: Enables advanced supplier data parsing
- **Default**: `false`
- **Status**: **UNTESTED - DO NOT CHANGE**
- **Warning**: Parser functionality not verified in current workflow

#### `test_mode` (boolean)
- **Purpose**: Enables test mode operation
- **Default**: `false`
- **Status**: **UNTESTED - DO NOT CHANGE**
- **Warning**: Test mode behavior not defined

#### `bypass_ai_scraping` (boolean)
- **Purpose**: Bypasses AI category suggestions
- **Default**: `false`
- **Status**: **UNTESTED - DO NOT CHANGE**
- **Warning**: May break multi-cycle AI progression

#### `enable_system_monitoring` (boolean)
- **Purpose**: Enables system resource monitoring
- **Default**: `true`
- **Status**: **UNTESTED - DO NOT CHANGE**
- **Warning**: Monitoring system integration not verified

## Integration Configuration

### OpenAI Integration

#### `enabled` (boolean)
- **Purpose**: Enables OpenAI API integration
- **Default**: `true`
- **Status**: ✅ **TESTED AND VERIFIED**
- **Usage**: Must be `true` for AI category suggestions

#### `api_key` (string)
- **Purpose**: OpenAI API authentication key
- **Status**: ✅ **TESTED AND VERIFIED**
- **Current Key**: `sk-02XZ3ucKVViULVaTp4_Ad6byZCT6Fofr-BwRsD5mTcT3BlbkFJ7_HTmTRScAn0m-ITc_CX5a2beXTOcbK1-Qmm0s6nwA`

#### `model` (string)
- **Purpose**: Specifies OpenAI model to use
- **Default**: `"gpt-4o-mini-search-preview-2025-03-11"`
- **Status**: ✅ **TESTED AND VERIFIED**
- **Features**: Includes web search capabilities for enhanced category discovery

#### `web_search_enabled` (boolean)
- **Purpose**: Enables web search capabilities in AI model
- **Default**: `true`
- **Status**: ✅ **TESTED AND VERIFIED**
- **Usage**: Enhances AI category suggestions with real-time market research

## Configuration Scenarios

### Multi-Cycle AI Testing Configuration
```json
{
  "system": {
    "clear_cache": false,
    "force_ai_scraping": true,
    "max_products_per_category": 3,
    "max_analyzed_products": 5
  }
}
```
**Purpose**: Triggers multiple AI cycles quickly for testing verification

### Production Configuration
```json
{
  "system": {
    "clear_cache": false,
    "force_ai_scraping": true,
    "max_products_per_category": 50,
    "max_analyzed_products": 100
  }
}
```
**Purpose**: Efficient operation for overnight infinite runs

### Cache Maintenance Configuration
```json
{
  "system": {
    "clear_cache": true,
    "clear_failed_extractions": true,
    "force_ai_scraping": true
  }
}
```
**Purpose**: Fresh start with automatic cleanup of failed extractions

## Critical Configuration Rules

### ✅ SAFE TO MODIFY
- `clear_cache`: Controls cache clearing behavior
- `force_ai_scraping`: Essential for AI progression
- `clear_failed_extractions`: Maintains cache cleanliness
- `max_products_per_category`: Controls processing pace
- `max_analyzed_products`: Controls AI suggestion frequency
- OpenAI integration settings

### ❌ DO NOT MODIFY
- `selective_cache_clear`: Complex logic not tested
- `enable_supplier_parser`: Parser not verified
- `test_mode`: Behavior undefined
- `bypass_ai_scraping`: May break AI progression
- `enable_system_monitoring`: Integration not verified

## Configuration Validation

### Required Settings for System Operation
1. **OpenAI Integration**: Must be enabled with valid API key
2. **AI Scraping**: `force_ai_scraping` should be `true`
3. **Cache Management**: `clear_cache` should typically be `false`

### Common Configuration Errors
1. **Missing API Key**: System will fail to initialize AI client
2. **Disabled AI Scraping**: Multi-cycle progression will not work
3. **Modifying Untested Settings**: May cause unpredictable behavior

## Troubleshooting Configuration Issues

### AI Client Initialization Failures
- Verify `openai.enabled` is `true`
- Check `openai.api_key` is valid
- Ensure internet connectivity for API access

### Cache-Related Issues
- Set `clear_cache: true` for fresh start
- Use `clear_failed_extractions: true` to clean problematic files
- Avoid modifying `selective_cache_clear`

### Performance Issues
- Adjust `max_products_per_category` for processing pace
- Modify `max_analyzed_products` for AI suggestion frequency
- Monitor system resources during infinite runs

## Configuration Best Practices

1. **Start with Tested Settings**: Use only verified configuration combinations
2. **Test Before Production**: Verify configuration changes with small test runs
3. **Document Changes**: Keep track of configuration modifications
4. **Backup Configurations**: Save working configurations before changes
5. **Monitor System Behavior**: Watch for unexpected behavior after configuration changes
