#!/usr/bin/env python3
"""
Test script to verify FBA/FBM seller counts extraction and new CSV columns
"""
import os
import json
import sys

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

from FBA_Financial_calculator import extract_enhanced_metrics, run_calculations

def test_seller_counts_extraction():
    """Test if FBA/FBM seller counts are being extracted from Amazon data"""
    print("🧪 Testing FBA/FBM Seller Counts Extraction...")
    
    # Load a sample Amazon cache file
    amazon_cache_dir = "OUTPUTS/FBA_ANALYSIS/amazon_cache"
    if not os.path.exists(amazon_cache_dir):
        print("❌ Amazon cache directory not found")
        return False
    
    cache_files = [f for f in os.listdir(amazon_cache_dir) if f.endswith('.json')]
    if not cache_files:
        print("❌ No Amazon cache files found")
        return False
    
    # Test with first available cache file
    test_file = os.path.join(amazon_cache_dir, cache_files[0])
    print(f"📁 Testing with: {cache_files[0]}")
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            amazon_data = json.load(f)
        
        # Extract enhanced metrics
        metrics = extract_enhanced_metrics(amazon_data)
        
        print("📊 Extracted Enhanced Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        
        # Check if we found any seller data
        seller_data_found = any([
            metrics['fba_seller_count'] is not None,
            metrics['fbm_seller_count'] is not None,
            metrics['total_offer_count'] is not None
        ])
        
        if seller_data_found:
            print("✅ Seller count extraction working!")
            return True
        else:
            print("⚠️ No seller count data found in this file")
            return False
            
    except Exception as e:
        print(f"❌ Error testing seller counts: {e}")
        return False

def test_csv_columns():
    """Test if new columns appear in CSV output"""
    print("\n🧪 Testing CSV Column Generation...")
    
    try:
        # Run FBA calculator
        results = run_calculations()
        
        if results and 'dataframe' in results:
            df = results['dataframe']
            expected_columns = ['bought_in_past_month', 'fba_seller_count', 'fbm_seller_count', 'total_offer_count']
            
            print("📋 CSV Columns Found:")
            for col in df.columns:
                status = "✅" if col in expected_columns else "📄"
                print(f"  {status} {col}")
            
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                print(f"❌ Missing columns: {missing_columns}")
                return False
            else:
                print("✅ All new columns present in CSV!")
                return True
        else:
            print("❌ No dataframe generated")
            return False
            
    except Exception as e:
        print(f"❌ Error testing CSV columns: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Enhanced Metrics Verification Tests...\n")
    
    test1_passed = test_seller_counts_extraction()
    test2_passed = test_csv_columns()
    
    print(f"\n📊 Test Results:")
    print(f"  Seller Counts Extraction: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  CSV Columns Generation: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Enhanced metrics are working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
