# POST-RUN TODO LIST
**File Purpose**: Critical tasks to execute after infinite run completion
**Reference**: See top of Claude.md for link to this file
**Last Updated**: June 10, 2025 at 08:53

## 🔧 CRITICAL FIXES NEEDED AFTER RUN COMPLETION

### 1. LINKING MAP CONTINUOUS SAVE FIX - CONFIRMED ADDED
**Current Issue**: `_save_linking_map()` function (line 2361 in `tools/passive_extraction_workflow_latest.py`) is only called conditionally and appears to be bypassed during active processing. New matches are stored in memory (`self.linking_map`) but not written to disk.

**EXACT LOCATION**: 
- File: `/tools/passive_extraction_workflow_latest.py`
- Function: `_save_linking_map()` at line 2361
- Problem: Only called at completion, not during processing
- Memory storage: `self.linking_map.append(link_record)` at line 2768

**REQUIRED FIX**: Add periodic saves every 25-50 processed products:
```python
# Add after line 2768 in _process_single_product_from_cache
processed_count = getattr(self, '_processed_count', 0) + 1
self._processed_count = processed_count

# Combined periodic saves and CSV generation every 40 products
if processed_count % 40 == 0:
    # Save linking map
    self._save_linking_map()
    
    # Generate separate EAN and Title CSV files
    self._generate_ean_matches_csv()
    self._generate_title_matches_csv_with_scores()
```

### 2. FBA CALCULATOR AUTO-TRIGGER INVESTIGATION - CONFIRMED ADDED
**MYSTERY SOLVED**: The system IS automatically triggering CSV generation. Found **107 CSV reports** generated automatically.

**INVESTIGATION NEEDED**: Determine exact trigger mechanism (appears to be completion-based or milestone-based)

### 3. SEPARATE EAN AND TITLE MATCH CSV FILES - CONFIRMED ADDED
**Current Issue**: Single CSV contains mixed EAN and Title matches without confidence scores

**REQUIRED CHANGES**:
- Create separate CSV for EAN matches: `fba_ean_matches_YYYYMMDD_HHMMSS.csv`
- Create separate CSV for Title matches: `fba_title_matches_YYYYMMDD_HHMMSS.csv`
- Add title similarity score column to title matches CSV
- Implement automatic generation every 40-50 products

### 4. SUBCATEGORY SCRAPING OPTIMIZATION - CONFIRMED ADDED
**Current Issue**: System scrapes both products AND subcategories, causing potential double processing

**CONFIRMED DOUBLE SCRAPING**: URLs show duplicates like:
- `/health-beauty.html` AND `/health-beauty/cosmetics.html`
- `/gifts-toys.html` AND `/gifts-toys/toys-games.html`

**REQUIRED FIX**: Add logic to scrape subcategories ONLY if main category has no products:
```python
# In category scraping function
if product_count >= 2:
    skip_subcategory_scraping = True
    use_pagination_only = True
else:
    scrape_subcategories = True
```

### 5. PHASE STATUS DASHBOARD INDICATOR - CONFIRMED ADDED
**Current Issue**: No clear indication of Phase 1 vs Phase 2 status in dashboard

**REQUIRED ADDITION**: Add to dashboard and metrics:
- Current Phase indicator (Phase 1: £0.1-£10 vs Phase 2: £10-£20)
- URL progress tracking per phase
- Page completion status per category

### 6. DASHBOARD ENCODING FIXES - CONFIRMED ADDED
**Current Issue**: Character encoding errors in dashboard display
- Keepa metrics: `'charmap' codec can't decode byte 0x8f`
- Financial metrics: `'charmap' codec can't decode byte 0x9d`

**REQUIRED FIX**: Update dashboard character encoding to UTF-8

### 7. KEEPA AND FINANCIAL DASHBOARD OUTPUT INVESTIGATION - CONFIRMED ADDED
**Current Issue**: All Keepa metrics show 0, Financial metrics show 0 despite data existing

**INVESTIGATION NEEDED**: 
- Verify why Keepa data extraction shows 0 success but Amazon files contain Keepa data
- Fix financial dashboard reporting (Financial Calculator works but dashboard shows 0)

## 📊 IMPLEMENTATION PRIORITY ORDER
1. **Linking Map Periodic Save** (CRITICAL - prevents data loss)
2. **Subcategory Double Scraping Fix** (HIGH - efficiency)
3. **Phase Status Dashboard** (HIGH - visibility)
4. **Separate EAN/Title CSV files** (MEDIUM - analysis improvement)
5. **Dashboard Encoding** (MEDIUM - cosmetic but important)
6. **Keepa/Financial Dashboard Fix** (LOW - reporting accuracy)

## 🎯 SUCCESS CRITERIA
- [ ] Linking map updates every 40 products during processing
- [ ] No double scraping of products via main + subcategories
- [ ] Clear Phase 1/2 status in dashboard
- [ ] CSV files generate automatically every 40-50 products  
- [ ] Separate EAN and Title match files with scores
- [ ] Dashboard displays without encoding errors
- [ ] Accurate Keepa and Financial metrics in dashboard