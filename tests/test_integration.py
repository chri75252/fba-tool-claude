#!/usr/bin/env python3
"""
Integration test to verify all enhanced features are working
"""
import os
import json
import sys

def test_linking_map_logic():
    """Test EAN linking map logic"""
    print("🧪 Testing EAN Linking Map Logic...")
    
    linking_map_path = "OUTPUTS/FBA_ANALYSIS/Linking map/linking_map.json"
    if not os.path.exists(linking_map_path):
        print("❌ Linking map not found")
        return False
    
    try:
        with open(linking_map_path, 'r') as f:
            linking_map = json.load(f)
        
        print(f"📋 Linking map contains {len(linking_map)} entries")
        
        # Check for EAN-based identifiers
        ean_entries = [entry for entry in linking_map if entry.get('supplier_product_identifier', '').startswith('EAN_')]
        url_entries = [entry for entry in linking_map if entry.get('supplier_product_identifier', '').startswith('URL_')]
        
        print(f"  EAN-based entries: {len(ean_entries)}")
        print(f"  URL-based entries: {len(url_entries)}")
        
        # Show sample entries
        if ean_entries:
            sample = ean_entries[0]
            print(f"  Sample EAN entry: {sample['supplier_product_identifier']} -> {sample['chosen_amazon_asin']}")
        
        if len(linking_map) > 0:
            print("✅ Linking map logic working!")
            return True
        else:
            print("❌ No entries in linking map")
            return False
            
    except Exception as e:
        print(f"❌ Error testing linking map: {e}")
        return False

def test_enhanced_csv_output():
    """Test the latest CSV output has enhanced columns"""
    print("\n🧪 Testing Enhanced CSV Output...")
    
    reports_dir = "OUTPUTS/FBA_ANALYSIS/financial_reports"
    if not os.path.exists(reports_dir):
        print("❌ Financial reports directory not found")
        return False
    
    # Find the most recent CSV file
    csv_files = [f for f in os.listdir(reports_dir) if f.endswith('.csv')]
    if not csv_files:
        print("❌ No CSV files found")
        return False
    
    latest_csv = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(reports_dir, f)))
    csv_path = os.path.join(reports_dir, latest_csv)
    
    print(f"📁 Testing latest CSV: {latest_csv}")
    
    try:
        with open(csv_path, 'r') as f:
            header = f.readline().strip()
        
        columns = header.split(',')
        expected_new_columns = ['bought_in_past_month', 'fba_seller_count', 'fbm_seller_count', 'total_offer_count']
        
        print("📋 CSV Columns:")
        for col in columns:
            status = "✅" if col in expected_new_columns else "📄"
            print(f"  {status} {col}")
        
        missing = [col for col in expected_new_columns if col not in columns]
        if missing:
            print(f"❌ Missing columns: {missing}")
            return False
        else:
            print("✅ All enhanced columns present!")
            return True
            
    except Exception as e:
        print(f"❌ Error testing CSV: {e}")
        return False

def test_amazon_cache_data():
    """Test Amazon cache contains enhanced data"""
    print("\n🧪 Testing Amazon Cache Enhanced Data...")
    
    cache_dir = "OUTPUTS/FBA_ANALYSIS/amazon_cache"
    if not os.path.exists(cache_dir):
        print("❌ Amazon cache directory not found")
        return False
    
    cache_files = [f for f in os.listdir(cache_dir) if f.endswith('.json')]
    if not cache_files:
        print("❌ No Amazon cache files found")
        return False
    
    enhanced_data_found = False
    
    for cache_file in cache_files[:3]:  # Test first 3 files
        try:
            with open(os.path.join(cache_dir, cache_file), 'r') as f:
                data = json.load(f)
            
            # Check for enhanced data
            has_monthly_sales = data.get('amazon_monthly_sales_badge') is not None
            has_keepa_data = data.get('keepa', {}).get('product_details_tab_data') is not None
            
            if has_monthly_sales or has_keepa_data:
                enhanced_data_found = True
                print(f"✅ Enhanced data found in {cache_file}")
                if has_monthly_sales:
                    print(f"  Monthly sales: {data.get('amazon_monthly_sales_badge')}")
                if has_keepa_data:
                    keepa_details = data['keepa']['product_details_tab_data']
                    seller_info = []
                    if 'Lowest FBA Seller' in keepa_details:
                        seller_info.append("FBA seller data")
                    if 'Lowest FBM Seller' in keepa_details:
                        seller_info.append("FBM seller data")
                    if 'Total Offer Count' in keepa_details:
                        seller_info.append(f"Total offers: {keepa_details['Total Offer Count']}")
                    if seller_info:
                        print(f"  Keepa data: {', '.join(seller_info)}")
                break
                
        except Exception as e:
            print(f"⚠️ Error reading {cache_file}: {e}")
            continue
    
    if enhanced_data_found:
        print("✅ Enhanced Amazon data extraction working!")
        return True
    else:
        print("❌ No enhanced data found in Amazon cache")
        return False

def main():
    print("🚀 Starting Integration Tests...\n")
    
    test1_passed = test_linking_map_logic()
    test2_passed = test_enhanced_csv_output()
    test3_passed = test_amazon_cache_data()
    
    print(f"\n📊 Integration Test Results:")
    print(f"  EAN Linking Map Logic: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  Enhanced CSV Output: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"  Amazon Cache Enhanced Data: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    
    all_passed = test1_passed and test2_passed and test3_passed
    
    if all_passed:
        print("\n🎉 All integration tests passed! System is working correctly.")
    else:
        print("\n⚠️ Some integration tests failed. Check the output above for details.")
    
    return all_passed

if __name__ == "__main__":
    main()
