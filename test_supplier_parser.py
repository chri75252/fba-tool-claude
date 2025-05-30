#!/usr/bin/env python3
"""
Test script for the enhanced supplier parser with debug logging
"""
import logging
import sys
import os

# Add tools directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

from tools.supplier_parser import SupplierDataParser

def test_supplier_parser():
    """Test the enhanced supplier parser functionality."""
    # Set up debug logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=== Testing Enhanced Supplier Parser ===\n")
    
    # Initialize parser
    parser = SupplierDataParser()
    print(f"Available supplier configs: {list(parser.parser_configs.keys())}\n")
    
    # Test HTML content
    test_html = '''
    <div class="product-list">
        <li class="item product product-item">
            <a href="/product/123" class="product-item-link">Test Product Title</a>
            <span class="price">£19.99</span>
            <img src="/image.jpg" class="product-image-photo" alt="product">
            <div class="product-item-details">
                EAN: 1234567890123
                Barcode: 9876543210987
            </div>
        </li>
        <li class="item product product-item">
            <a href="/product/456" class="product-item-link">Another Product</a>
            <span class="price">£29.99</span>
            <img src="/image2.jpg" class="product-image-photo" alt="product">
        </li>
    </div>
    '''
    
    print("=== Testing clearance-king configuration ===")
    result = parser.parse_supplier_data('clearance-king', test_html, 'http://test.com')
    
    print("\nParsing result:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_supplier_parser()
