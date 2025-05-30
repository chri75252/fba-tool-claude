#!/usr/bin/env python
"""
Complete FBA Analysis - Integrated Workflow
This script runs the complete FBA analysis from supplier scraping to final profit analysis.
"""
import asyncio
import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(current_dir / 'logs' / 'complete_analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)

async def main():
    """Run the complete FBA analysis workflow."""
    
    print("="*80)
    print("Amazon FBA Agent System - Complete Analysis")
    print("Phase 3: Integrated Supplier Analysis")
    print("="*80)
    
    try:
        # Ensure required directories exist
        (current_dir / 'logs').mkdir(exist_ok=True)
        (current_dir / 'cache').mkdir(exist_ok=True)
        (current_dir / 'OUTPUTS' / 'FBA_ANALYSIS').mkdir(parents=True, exist_ok=True)
        
        print("\n🚀 Starting Complete FBA Analysis...")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load configuration from system_config.json
        import json
        config_path = current_dir / 'config' / 'system_config.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Import and initialize the orchestrator
        sys.path.append(str(current_dir / 'tools'))
        from main_orchestrator import FBASystemOrchestrator
        
        orchestrator = FBASystemOrchestrator(config)
        
        print("\n📊 Running Integrated Passive Extraction Workflow...")
        print("🧹 Clearing cache to ensure fresh analysis...")
        
        # Run the complete workflow with passive extraction
        results = await orchestrator.run_with_passive_workflow(max_products=100)
        
        print(f"\n✅ Analysis Complete!")
        print(f"📈 Processed: {len(results)} products")
        print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return results
        
        print("\n✅ Complete FBA Analysis Finished!")
        print(f"⏰ End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📁 Check the following directories for results:")
        print("   - OUTPUTS/FBA_ANALYSIS/ for analysis reports")
        print("   - logs/ for detailed execution logs")
        
    except Exception as e:
        log.error(f"Error in complete FBA analysis: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("Check logs/complete_analysis.log for detailed error information")
        return 1
    
    return 0

if __name__ == "__main__":
    # Clear any existing cache to ensure fresh start
    cache_dir = Path(__file__).parent / "OUTPUTS" / "FBA_ANALYSIS" / "supplier_cache"
    if cache_dir.exists():
        print("🧹 Clearing cache to ensure fresh start...")
        for cache_file in cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                print(f"   Cleared: {cache_file.name}")
            except Exception as e:
                print(f"   Warning: Could not clear {cache_file.name}: {e}")
    
    # Run the analysis
    exit_code = asyncio.run(main())
    sys.exit(exit_code)