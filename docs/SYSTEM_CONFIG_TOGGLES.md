# System Configuration Toggles Reference

**Version:** 3.4  
**Date:** 2025-06-08  
**Purpose:** Complete reference for multi-tier AI fallback system configuration

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

## Multi-Tier AI-First Fallback System Configuration (v3.4)

### AI Category Selection Configuration

#### `ai_features.category_selection.disable_ai_category_selection`
- **Type:** Boolean
- **Default:** `false`
- **Description:** Master safety switch to bypass ALL AI tiers and use dynamic category discovery
- **Valid Values:** `true`, `false`
- **Test Environment:** `false` (test AI fallback ladder)
- **Production Environment:** `false` (enable AI-first system)
- **Usage:** Set to `true` only for testing manual fallback or debugging dynamic discovery

#### `ai_features.category_selection.mode`
- **Type:** Enum
- **Default:** `"v2"`
- **Description:** Primary AI prompt mode - system tries this first in fallback ladder
- **Valid Values:** `"v2"`, `"legacy"`, `"minimal"`
- **Test Environment:** `"v2"` (clearance-first optimization)
- **Production Environment:** `"v2"` (recommended starting point)
- **Usage:** 
  - `"v2"`: 25-line clearance-optimized prompt (Tier 1, Temperature: 0.1)
  - `"legacy"`: 86-line comprehensive prompt (Tier 2, Temperature: 0.3)  
  - `"minimal"`: 12-line terse prompt (Tier 3, Temperature: 0.5)

### Multi-Tier Fallback Configuration

#### `ai_features.category_selection.fallbacks.max_retries`
- **Type:** Integer
- **Default:** `2`
- **Description:** Number of fallback attempts through AI ladder before dynamic discovery
- **Valid Values:** `1-5`
- **Test Environment:** `2` (validate full ladder)
- **Production Environment:** `2` (balanced retries vs speed)
- **Usage:** Higher values = more AI attempts but slower fallback to dynamic discovery

#### `ai_features.category_selection.fallbacks.clear_cache_between_retries`
- **Type:** Boolean  
- **Default:** `true`
- **Description:** Cache invalidation between AI attempts for fresh results
- **Valid Values:** `true`, `false`
- **Test Environment:** `true` (clean testing)
- **Production Environment:** `true` (prevent cached bad results)
- **Usage:** Ensures each AI tier gets fresh category data

#### `ai_features.category_selection.fallbacks.alternate_prompts`
- **Type:** Array of strings
- **Default:** `["v2", "legacy", "minimal"]`
- **Description:** Order of prompt modes to try in fallback ladder
- **Valid Values:** Any combination of valid modes
- **Test Environment:** `["v2", "legacy", "minimal"]` (full ladder)
- **Production Environment:** `["v2", "legacy", "minimal"]` (recommended sequence)
- **Usage:** System tries each mode in sequence with escalating temperature

#### `ai_features.category_selection.fallbacks.temperature_escalation`
- **Type:** Array of floats
- **Default:** `[0.1, 0.3, 0.5]`  
- **Description:** Temperature values for each tier of fallback ladder
- **Valid Values:** `0.0-1.0` for each tier
- **Test Environment:** `[0.1, 0.3, 0.5]` (validate escalation)
- **Production Environment:** `[0.1, 0.3, 0.5]` (balanced creativity vs consistency)
- **Usage:** Lower temperatures = more focused, higher = more creative

#### `ai_features.category_selection.fallbacks.model_escalation`
- **Type:** Array of strings
- **Default:** `["gpt-4o-mini-2024-07-18"]`
- **Description:** Model progression for fallback tiers (future enhancement)
- **Valid Values:** Valid OpenAI model names
- **Test Environment:** `["gpt-4o-mini-2024-07-18"]` (single model)
- **Production Environment:** `["gpt-4o-mini-2024-07-18"]` (proven model)
- **Usage:** Future: escalate to more powerful models in higher tiers

### Dynamic Re-ordering Configuration

#### `ai_features.dynamic_reordering.enabled`
- **Type:** Boolean
- **Default:** `false`
- **Description:** Enable performance-based category re-ordering during processing
- **Valid Values:** `true`, `false`
- **Test Environment:** `false` (for predictable test results)
- **Production Environment:** `true` (optimize category processing order)
- **Usage:** Automatically prioritizes categories with better performance metrics

#### `ai_features.dynamic_reordering.trigger_interval`
- **Type:** Integer
- **Default:** `5`
- **Description:** Number of categories processed before triggering re-ordering evaluation
- **Valid Values:** `1-50`
- **Test Environment:** `1` (immediate re-ordering for testing)
- **Production Environment:** `5` (balanced performance vs overhead)
- **Usage:** Lower values = more responsive but higher computational overhead

## Processing Limits Configuration

### `processing_limits.category_timeout_minutes`
- **Type:** Integer
- **Default:** `30`
- **Description:** Maximum time to spend processing a single category before moving to next
- **Valid Values:** `5-120`
- **Test Environment:** `5` (quick timeout for testing)
- **Production Environment:** `30` (allow thorough processing)
- **Usage:** Prevents system from getting stuck on problematic categories

## Performance Configuration

### `performance.browser_instances`
- **Type:** Integer
- **Default:** `1`
- **Description:** Number of concurrent browser instances for parallel processing
- **Valid Values:** `1-5`
- **Test Environment:** `1` (single-threaded for debugging)
- **Production Environment:** `2-3` (optimal for hardware)
- **Usage:** Higher values increase speed but use more memory and CPU

### `performance.concurrent_products`
- **Type:** Integer
- **Default:** `1`
- **Description:** Number of products to process concurrently
- **Valid Values:** `1-10`
- **Test Environment:** `1` (sequential for predictable results)
- **Production Environment:** `3-5` (parallel processing)
- **Usage:** Must not exceed browser_instances limit

### `performance.memory_threshold_mb`
- **Type:** Integer
- **Default:** `2048`
- **Description:** Memory usage threshold in MB before triggering cleanup
- **Valid Values:** `512-8192`
- **Test Environment:** `1024` (trigger cleanup early for testing)
- **Production Environment:** `2048` (reasonable threshold for 32GB system)
- **Usage:** Prevents memory leaks during long runs

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
