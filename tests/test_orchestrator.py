#!/usr/bin/env python3
"""
Test script for the enhanced FBA System Orchestrator
"""
import asyncio
import json
import logging
from pathlib import Path
import sys

# Add tools directory to path
sys.path.append('tools')

from main_orchestrator import FBASystemOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_orchestrator.log')
    ]
)

log = logging.getLogger(__name__)

async def test_orchestrator():
    """Test the orchestrator with 5 products."""
    try:
        # Load configuration
        config_path = Path('config/system_config.json')
        if not config_path.exists():
            log.error(f"Configuration file not found: {config_path}")
            return
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        log.info("Configuration loaded successfully")
        log.info(f"Test mode: {config['system']['test_mode']}")
        log.info(f"Clear cache: {config['system']['clear_cache']}")
        log.info(f"Selective cache clear: {config['system']['selective_cache_clear']}")
        log.info(f"Bypass AI scraping: {config['system']['bypass_ai_scraping']}")
        
        # Initialize orchestrator
        log.info("Initializing FBA System Orchestrator...")
        orchestrator = FBASystemOrchestrator(config)
        
        # Test configuration methods
        log.info(f"Active extraction mode: {orchestrator.active_extraction_mode}")
        log.info(f"Should bypass AI scraping: {orchestrator.should_bypass_ai_scraping()}")
        
        extraction_config = orchestrator.get_extraction_mode_config()
        log.info(f"Extraction mode config: {extraction_config}")
        
        fallback_behavior = orchestrator.get_fallback_behavior()
        log.info(f"Fallback behavior: {fallback_behavior}")
        
        # Test cache clearing
        log.info("Testing selective cache clearing...")
        await orchestrator.selective_clear_cache_dirs()
        
        # Run analysis with 5 products
        log.info("Starting analysis with 5 products...")
        suppliers = ['clearance-king']  # Use the configured supplier
        
        await orchestrator.run(suppliers, max_products=5)
        
        log.info("Analysis completed successfully!")
        
        # Display results
        if orchestrator.results:
            log.info(f"Found {len(orchestrator.results)} profitable products:")
            for i, result in enumerate(orchestrator.results, 1):
                supplier_product = result['supplier_product']
                analysis = result['analysis']
                log.info(f"  {i}. {supplier_product.get('title', 'Unknown')} - ROI: {analysis.roi_percent:.1f}% - Profit: £{analysis.net_profit:.2f}")
        else:
            log.info("No profitable products found in this test run")
        
    except Exception as e:
        log.error(f"Error during testing: {e}", exc_info=True)
        raise

def main():
    """Main entry point."""
    log.info("Starting FBA System Orchestrator Test")
    log.info("=" * 50)
    
    try:
        asyncio.run(test_orchestrator())
        log.info("=" * 50)
        log.info("Test completed successfully!")
    except KeyboardInterrupt:
        log.info("Test interrupted by user")
    except Exception as e:
        log.error(f"Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
