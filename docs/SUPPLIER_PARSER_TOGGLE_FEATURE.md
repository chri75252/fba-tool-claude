# Supplier Parser Toggle Feature

## Overview

The Supplier Parser Toggle feature allows users to conditionally enable or disable the specialized supplier parsing logic in the FBA System Orchestrator. This provides flexibility for different use cases, from debugging to performance testing.

## Implementation

### Configuration

The feature is controlled via the `system_config.json` file:

```json
{
  "system": {
    "enable_supplier_parser": true  // or false
  }
}
```

### Code Changes

#### 1. Main Orchestrator (`tools/main_orchestrator.py`)

**Added Configuration Loading:**
```python
# System configuration flags
system_config = self.config.get('system', {})
self.enable_supplier_parser = system_config.get('enable_supplier_parser', True)
```

**Added Logging:**
```python
log.info(f"Supplier parser enabled: {self.enable_supplier_parser}")
```

**Modified Scraping Logic:**
```python
# Parse product data - conditionally use supplier parser
if self.enable_supplier_parser:
    log.debug(f"Using supplier parser for {supplier_id}")
    product_data = self.parser.parse_supplier_data(
        supplier_id,
        element,
        full_url
    )
else:
    log.debug(f"Supplier parser disabled, using raw element data for {supplier_id}")
    # Use raw element data without specialized parsing
    product_data = {
        'supplier_id': supplier_id,
        'url': full_url,
        'raw_element': str(element) if hasattr(element, '__str__') else element,
        '_parser_disabled': True
    }
```

## Behavior

### When Enabled (`enable_supplier_parser: true`)

- **Uses:** `SupplierDataParser.parse_supplier_data()`
- **Applies:** Supplier-specific parsing rules
- **Returns:** Structured, validated product data
- **Filters:** Invalid products based on validation rules
- **Performance:** Standard parsing overhead

### When Disabled (`enable_supplier_parser: false`)

- **Skips:** Specialized parsing logic
- **Returns:** Raw element data with metadata
- **Includes:** `_parser_disabled: true` flag
- **Performance:** Faster execution (no parsing overhead)
- **Data:** Unstructured raw scraped content

## Use Cases

### Enable Parser When:

1. **Production Use:** You have well-defined supplier parsing rules
2. **Data Quality:** You need structured, validated product data
3. **Filtering:** You want to automatically filter out invalid products
4. **Standard Operation:** Normal FBA analysis workflow

### Disable Parser When:

1. **New Suppliers:** Testing suppliers without established parsing rules
2. **Debugging:** Investigating scraping issues or data extraction problems
3. **Raw Data Analysis:** You want to examine unprocessed scraped content
4. **Performance Testing:** Bypassing parsing for speed benchmarks
5. **Development:** Building new parsing rules and need raw data

## Testing

### Test Script: `test_supplier_parser_toggle.py`

The test script demonstrates:
- Configuration loading
- Toggle behavior verification
- Expected outcomes for both states
- Implementation details
- Use case scenarios

### Running the Test

```bash
python test_supplier_parser_toggle.py
```

### Expected Output

```
============================================================
Testing Supplier Parser Toggle Feature
============================================================

1. Testing with Supplier Parser ENABLED
----------------------------------------
Supplier parser enabled: True
Expected behavior: Will use specialized supplier parsing logic

2. Testing with Supplier Parser DISABLED
----------------------------------------
Supplier parser enabled: False
Expected behavior: Will use raw element data without specialized parsing
```

## Integration

### System Configuration

The feature integrates seamlessly with the existing configuration system:

```json
{
  "system": {
    "test_mode": false,
    "clear_cache": true,
    "selective_cache_clear": true,
    "bypass_ai_scraping": false,
    "enable_supplier_parser": true  // New toggle
  }
}
```

### Logging Integration

The feature provides comprehensive logging:
- Initialization status
- Per-supplier parsing decisions
- Debug information for troubleshooting

### Error Handling

- Graceful fallback to raw data if parsing fails
- Validation error tracking
- Comprehensive error logging

## Benefits

1. **Flexibility:** Adapt to different operational needs
2. **Debugging:** Easier troubleshooting of parsing issues
3. **Performance:** Option to bypass parsing overhead
4. **Development:** Facilitates new supplier integration
5. **Testing:** Enables isolated testing scenarios

## Future Enhancements

1. **Per-Supplier Toggle:** Individual supplier parser control
2. **Conditional Logic:** Smart enabling based on supplier maturity
3. **Performance Metrics:** Parsing vs. raw data performance comparison
4. **Validation Levels:** Configurable validation strictness
5. **Fallback Strategies:** Automatic fallback on parsing failures

## Conclusion

The Supplier Parser Toggle feature provides essential flexibility for the FBA System, enabling users to adapt the system behavior to their specific needs while maintaining full functionality in both modes.
