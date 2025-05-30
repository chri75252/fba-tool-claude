#!/usr/bin/env python3
"""
Test script to demonstrate the supplier parser toggle feature
"""
import asyncio
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def test_supplier_parser_toggle():
    """Test the supplier parser toggle functionality"""
    print("=" * 60)
    print("Testing Supplier Parser Toggle Feature")
    print("=" * 60)
    
    # Import the orchestrator
    try:
        import sys
        sys.path.append('tools')
        from main_orchestrator import FBASystemOrchestrator
    except ImportError as e:
        print(f"Error importing orchestrator: {e}")
        print("Make sure you're running from the project root directory")
        return
    
    # Load system configuration
    config_path = Path('config/system_config.json')
    if not config_path.exists():
        print(f"Configuration file not found: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("\n1. Testing with Supplier Parser ENABLED")
    print("-" * 40)
    
    # Test with supplier parser enabled
    config['system']['enable_supplier_parser'] = True
    orchestrator_enabled = FBASystemOrchestrator(config)
    
    print(f"Supplier parser enabled: {orchestrator_enabled.enable_supplier_parser}")
    print("Expected behavior: Will use specialized supplier parsing logic")
    
    print("\n2. Testing with Supplier Parser DISABLED")
    print("-" * 40)
    
    # Test with supplier parser disabled
    config['system']['enable_supplier_parser'] = False
    orchestrator_disabled = FBASystemOrchestrator(config)
    
    print(f"Supplier parser enabled: {orchestrator_disabled.enable_supplier_parser}")
    print("Expected behavior: Will use raw element data without specialized parsing")
    
    print("\n3. Configuration Options")
    print("-" * 40)
    print("To control supplier parser behavior, set in config/system_config.json:")
    print('  "system": {')
    print('    "enable_supplier_parser": true   // Enable specialized parsing')
    print('    "enable_supplier_parser": false  // Use raw element data')
    print('  }')
    
    print("\n4. Implementation Details")
    print("-" * 40)
    print("When enabled:")
    print("  - Uses SupplierDataParser.parse_supplier_data()")
    print("  - Applies supplier-specific parsing rules")
    print("  - Extracts structured product data")
    
    print("\nWhen disabled:")
    print("  - Skips specialized parsing")
    print("  - Returns raw element data with metadata")
    print("  - Adds '_parser_disabled': True flag")
    
    print("\n5. Use Cases")
    print("-" * 40)
    print("Enable parser when:")
    print("  - You have well-defined supplier parsing rules")
    print("  - You need structured, validated product data")
    print("  - You want to filter out invalid products")
    
    print("\nDisable parser when:")
    print("  - Testing new suppliers without parsing rules")
    print("  - Debugging scraping issues")
    print("  - You want to see raw scraped data")
    print("  - Bypassing parsing for performance testing")
    
    print("\n" + "=" * 60)
    print("Supplier Parser Toggle Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_supplier_parser_toggle())
