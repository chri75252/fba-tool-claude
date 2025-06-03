# System Deep Dive: Core Logic and Mechanisms

This document provides a more detailed explanation of several critical components and logic flows within the Amazon FBA Agent System. It's intended for developers working on the system or for advanced users wishing to understand its internal workings more thoroughly.

## Table of Contents
1.  [Selective Cache Clearing Mechanisms](#1-selective-cache-clearing-mechanisms)
    *   [Configuration Flags](#configuration-flags)
    *   [Orchestrator-Level Clearing (`main_orchestrator.py`)](#orchestrator-level-clearing-main_orchestratorpy)
    *   [Workflow-Level Clearing (`passive_extraction_workflow_latest.py` via `CacheManager`)](#workflow-level-clearing-passive_extraction_workflow_latestpy-via-cachemanager)
    *   [Logging Cleared Unanalyzed Products](#logging-cleared-unanalyzed-products)
2.  [AI-Integrated Supplier Scraping](#2-ai-integrated-supplier-scraping)
    *   [The AI Category Cache (`ai_category_cache`)](#the-ai-category-cache-ai_category_cache)
    *   [AI Prompt and Context](#ai-prompt-and-context)
    *   [Forcing AI Category Progression](#forcing-ai-category-progression)
3.  [The Linking Map (`linking_map.json`)](#3-the-linking-map-linking_mapjson)
    *   [Purpose and Structure](#purpose-and-structure)
    *   [Role in Preventing Re-processing](#role-in-preventing-re-processing)
    *   [Handling Duplicates/Updates](#handling-duplicatesupdates)
4.  [Workflow Resume Logic](#4-workflow-resume-logic)
    *   [Role of `linking_map.json`](#role-of-linking_mapjson)
    *   [Role of `*_processing_state.json`](#role-of-_processing_statejson)
    *   [Interaction with Cache States](#interaction-with-cache-states)

---

## 1. Selective Cache Clearing Mechanisms

The system employs sophisticated cache clearing logic to manage data efficiently, avoid redundant processing, and allow for fresh data acquisition when needed. This is primarily controlled by flags in `config/system_config.json` and implemented across `main_orchestrator.py` and `passive_extraction_workflow_latest.py` (using `CacheManager`).

### Configuration Flags

From `config/system_config.json` (under the `system` key):
*   `"clear_cache"` (boolean):
    *   If `true`, the system will perform some form of cache clearing at startup.
*   `"selective_cache_clear"` (boolean):
    *   If `true` AND `clear_cache` is `true`: The orchestrator favors a selective clearing strategy.
    *   If `true` AND `clear_cache` is `false`: `passive_extraction_workflow_latest.py` will initiate its own selective clear via `CacheManager`. This is a key scenario for targeted refreshes.

### Orchestrator-Level Clearing (`main_orchestrator.py`)

When `FBASystemOrchestrator` in `tools/main_orchestrator.py` starts, its `run()` or `run_with_passive_workflow()` method checks the `clear_cache` flag:

```python
# In FBASystemOrchestrator.run() or run_with_passive_workflow()
if self.clear_cache:
    if self.selective_cache_clear:
        await self.selective_clear_cache_dirs()
    else:
        await self.clear_cache_dirs()
```

*   **`clear_cache_dirs()`**: Performs a full, non-selective wipe of directories listed in `self.cache_config.get('directories', {})`, which are populated from `system_config.json`.
*   **`selective_clear_cache_dirs()`**: This method implements a more nuanced clearing:
    *   It respects a `preserve_dirs` list (e.g., `ai_category_cache`, `Linking map` by default if their preservation flags in `selective_clear_config` are true).
    *   Calls `_clear_unanalyzed_products()` if `selective_clear_config.clear_unanalyzed_only` is true.
    *   Calls `_clear_failed_extractions()` if `selective_clear_config.clear_failed_extractions` is true.
    *   May call `_selective_clear_directory()` for other cache directories.

    **`_clear_unanalyzed_products()` in `FBASystemOrchestrator`**:
    This is a critical part of the selective clear initiated by the orchestrator.
    ```python
    # Snippet from FBASystemOrchestrator._clear_unanalyzed_products()
    # ...
    # processed_identifiers = set() loaded from linking_map.json
    # ...
    for supplier_file in supplier_cache_dir.glob("*.json"):
        # ... load products from supplier_file ...
        all_products_in_file_unanalyzed = True
        for product in products:
            identifier = product.get("ean") or product.get("url")
            if identifier and identifier in processed_identifiers:
                all_products_in_file_unanalyzed = False
                break 
        
        if all_products_in_file_unanalyzed:
            log.info(f"All products in {supplier_file.name} are unanalyzed. Preparing to clear.")
            if products: # Log contents before deleting
                # ... (logic to write products to manual_review_log_path) ...
            supplier_file.unlink() # Delete the file
    # ...
    ```
    This function iterates through supplier cache files (e.g., `OUTPUTS/cached_products/*.json`). If an entire file contains *only* products whose identifiers are *not* in `linking_map.json`, that file is deleted. Its contents are logged to `OUTPUTS/FBA_ANALYSIS/cleared_for_manual_review.jsonl` before deletion.

### Workflow-Level Clearing (`passive_extraction_workflow_latest.py` via `CacheManager`)

Independent of the orchestrator's initial clear, `PassiveExtractionWorkflow` in `tools/passive_extraction_workflow_latest.py` also has its own cache management logic, primarily for the Test 2 scenario (`clear_cache: false`, `selective_cache_clear: true`).

In its `run_workflow_main()` (or initialization leading up to its `run()` method), it checks the `selective_cache_clear` flag from `system_config.json`:

```python
# Simplified logic in passive_extraction_workflow_latest.py's startup/run
# (actual implementation is in run_workflow_main before PassiveExtractionWorkflow.run)

if not clear_cache_setting and selective_cache_setting: # Test 2 scenario
    log.info("System config: clear_cache=False + selective_cache_clear=True, performing selective cache clear only")
    clearing_results = await cache_manager.clear_cache(strategy="smart_selective")
    # This specific case forces supplier_cache_cleared = True to trigger AI progression
    supplier_cache_cleared = True 
elif clear_cache_setting and selective_cache_setting:
    # ... (other selective clear via cache_manager) ...
# ...

if supplier_cache_cleared and ai_client:
    log.info("Supplier cache was cleared - forcing AI category progression...")
    workflow_instance.force_ai_category_progression = True
```

The `cache_manager.clear_cache(strategy="smart_selective")` call invokes the `SmartSelectiveStrategy` within `tools/cache_manager.py`.

**`SmartSelectiveStrategy` in `CacheManager`**:
This strategy has a different behavior for `_clear_cache_file` compared to the orchestrator's method:

```python
# Snippet from CacheManager.SmartSelectiveStrategy._clear_cache_file()
# ...
# self.processed_identifiers = set() loaded from linking_map.json
# ...
# For a given supplier cache file_path:
with open(file_path, 'r', encoding='utf-8') as f:
    cached_data = json.load(f) # This is a list of products

if isinstance(cached_data, list):
    original_count = len(cached_data)
    filtered_data = [] # Will store products to KEEP
    
    for item in cached_data:
        identifier = self._get_product_identifier(item)
        if identifier not in self.processed_identifiers: # Keep if NOT in linking_map (i.e., unanalyzed)
            filtered_data.append(item)
    
    removed_count = original_count - len(filtered_data) # This is the count of ANALYZED products removed
    
    if removed_count > 0:
        # ... (backup and save filtered_data back to file_path) ...
        log.info(f"Removed {removed_count} processed (analyzed) items from {file_path.name}")
# ...
```
This strategy modifies supplier cache files by removing products that *are* in the `linking_map.json` (i.e., "analyzed" or "processed" products). It leaves the "unanalyzed" products in the file. This is designed to keep the supplier cache lean and focused on items that still need to go through the Amazon matching pipeline. It does **not** log to `cleared_for_manual_review.jsonl` because the items it removes are already considered processed.

### Logging Cleared Unanalyzed Products

As detailed above, the file `OUTPUTS/FBA_ANALYSIS/cleared_for_manual_review.jsonl` is populated **only** by `FBASystemOrchestrator._clear_unanalyzed_products` when it deletes an entire supplier cache file because all products within it were unanalyzed. Each product from the deleted file is written as a separate JSON line. This file serves as a log of items that were pending analysis but were removed from the primary workflow due to this specific cache clearing action.

---

## 2. AI-Integrated Supplier Scraping

When the system needs to discover new product categories or pages from a supplier website (especially if `force_ai_category_progression` is true), it uses an AI-assisted approach. This is primarily managed by `PassiveExtractionWorkflow` in `tools/passive_extraction_workflow_latest.py`.

### The AI Category Cache (`ai_category_cache`)

For each supplier, the system maintains a history of its AI-driven scraping activities in a JSON file located at: `OUTPUTS/FBA_ANALYSIS/ai_category_cache/{supplier_name}_ai_categories.json`.

This file is crucial for the AI's "memory." Its structure typically includes:
*   `"categories_scraped"`: (list of strings) URLs of supplier categories that have been selected by the AI and scraped in previous iterations.
*   `"pages_visited"`: (list of strings) General page URLs visited on the supplier site.
*   `"subpages_scraped"`: (list of strings) Specific sub-page URLs that have been scraped for products.
*   `"url_hash_cache"`: (dict) Maps MD5 hashes of URLs to the original URLs. This helps in identifying already visited URLs even if they have slight variations (e.g., different query parameters).
*   `"products_processed"`: (list of strings) Identifiers (EANs or URLs) of supplier products that have been processed (i.e., attempted to be matched on Amazon).
*   `"ai_decision_history"`: (list of dicts) A log of past decisions made by the AI. Each entry might contain:
    *   `"timestamp"`
    *   `"categories_suggested"` (e.g., `top_3_urls` from AI)
    *   `"skip_urls"`
    *   `"reasoning"`
    *   `"progression_strategy"`
*   `"category_performance"`: (dict) Maps category URLs to performance metrics:
    *   `"products_found"`
    *   `"last_scraped"`
    *   `"performance_score"` (e.g., normalized product count)

Key methods in `PassiveExtractionWorkflow` involved:
*   `_load_history()`: Loads this JSON file at the start of AI-driven category selection.
*   `_save_history()`: Saves the updated history object back to the JSON file.
*   `_hierarchical_category_selection()`: Orchestrates the AI category discovery.
*   `_get_ai_suggested_categories_enhanced()`: Formats the prompt for the AI and calls the LLM.
*   `_record_ai_decision()`, `_add_url_to_history()`: Update the history object with new information.

### AI Prompt and Context

The `_get_ai_suggested_categories_enhanced()` method constructs a detailed prompt for the LLM. Crucially, it includes context from the loaded history file:
```
PREVIOUSLY PROCESSED CATEGORIES: {list_from_hist["categories_scraped"]}
PREVIOUSLY PROCESSED PRODUCTS: {list_from_hist["products_processed"]}
# Potentially also a summary from hist["category_performance"]
```
This tells the AI which parts of the supplier's site it has already explored and which products it has already seen, guiding it to suggest new, potentially more fruitful categories and avoid redundant work.

### Forcing AI Category Progression

The `force_ai_category_progression` flag in `PassiveExtractionWorkflow` is important. It's set to `True` typically when `passive_extraction_workflow_latest.py` determines that the supplier cache was cleared or is stale (e.g., after a selective clear via `CacheManager` as in Test 2 scenario: `clear_cache: false, selective_cache_clear: true`).

When `True`, `_extract_supplier_products()` in `PassiveExtractionWorkflow` will prioritize calling `_hierarchical_category_selection()` to get a fresh list of category/page URLs to scrape, rather than relying on pre-configured `category_paths` in the supplier config or just loading an existing (but potentially stale or modified) supplier product cache file. This ensures that after certain cache operations, the system actively seeks new data from the supplier using AI.

---

## 3. The Linking Map (`linking_map.json`)

The `linking_map.json` file, located at `OUTPUTS/FBA_ANALYSIS/Linking map/linking_map.json`, is a cornerstone of the system's state management and efficiency.

### Purpose and Structure

*   **Purpose:** To store a persistent record of successfully established links between supplier products and their corresponding Amazon Standard Identification Numbers (ASINs). This map signifies that a supplier product has been found on Amazon, and its Amazon data has been extracted.
*   **Structure:** It's a JSON array of objects. Each object represents a single link and typically contains:
    *   `"supplier_product_identifier"`: A unique identifier for the supplier product (e.g., EAN, or the product's URL on the supplier site).
    *   `"chosen_amazon_asin"`: The ASIN of the Amazon product that was matched.
    *   Other relevant details like match method, timestamps, snippets of titles for quick reference, etc., might be included.

### Role in Preventing Re-processing

The primary use of `linking_map.json` is to avoid redundant work:
1.  **In `passive_extraction_workflow_latest.py`**: Before attempting to find an Amazon match for a supplier product (whether freshly scraped or loaded from `OUTPUTS/cached_products/`), the workflow checks if the `supplier_product_identifier` is already present in the `linking_map.json` with a `chosen_amazon_asin`. If a valid link exists, that supplier product is typically skipped, as its Amazon counterpart has already been processed.
2.  **In Cache Clearing (`main_orchestrator.py` and `cache_manager.py`)**:
    *   `FBASystemOrchestrator._clear_unanalyzed_products()` uses the linking map to determine if all products in a supplier cache file are "unanalyzed."
    *   `CacheManager.SmartSelectiveStrategy` uses it to identify "processed" items within a supplier cache file (to remove them and keep the cache lean with only unanalyzed items).

### Handling Duplicates/Updates

The `linking_map.json` aims to store the single best-known link for each unique `supplier_product_identifier`.
*   When `passive_extraction_workflow_latest.py` (specifically its `_cache_amazon_data` method or a helper it calls) adds a new link to its in-memory representation of the linking map (`self.linking_map`):
    *   It should first check if an entry for the given `supplier_product_identifier` already exists.
    *   If it exists: The existing entry is updated (e.g., if a new, better ASIN match is found, or just to refresh a timestamp). This prevents duplicate entries for the same supplier product.
    *   If it doesn't exist: The new link entry is appended.
*   The `_save_linking_map()` method then writes the entire (de-duplicated and updated) in-memory list back to the `linking_map.json` file, usually using an atomic write to prevent corruption.

This ensures that the `linking_map.json` remains a clean and authoritative record.

---

## 4. Workflow Resume Logic

The system has mechanisms to resume processing from where it left off, particularly useful for long runs or interruptions. This relies on `linking_map.json` and supplier-specific state files.

### Role of `linking_map.json`

As described above, the `linking_map.json` is the primary tool for ensuring that products already successfully matched and analyzed on Amazon are not re-processed from scratch in subsequent runs. This is a global resume mechanism across all suppliers for specific product links.

### Role of `*_processing_state.json`

For finer-grained resume capability *within a single supplier's list of products during a particular run*, `passive_extraction_workflow_latest.py` uses state files:
`OUTPUTS/FBA_ANALYSIS/{supplier_name}_processing_state.json`.

*   **Structure:** A simple JSON object, e.g., `{ "last_processed_index": 42 }`.
*   **Purpose:** This file stores the index of the last supplier product (in the current list being iterated over for that supplier) that was sent for Amazon matching.
*   **Usage:**
    *   At the start of processing a supplier, `PassiveExtractionWorkflow.run()` loads this state file (if `resume_from_last` is true).
    *   It then slices the current list of supplier products (after filtering out those already in `linking_map.json`) to start from `last_processed_index + 1`.
    *   The `last_processed_index` is updated as each product is processed.

### Interaction with Cache States

*   If a supplier's product cache (e.g., `OUTPUTS/cached_products/{supplier_name}_products_cache.json`) is cleared (either fully or selectively modified by `CacheManager`), and then fresh products are scraped for that supplier:
    *   The `last_processed_index` from an old `_processing_state.json` might become invalid (e.g., pointing beyond the bounds of the new, smaller list of products).
    *   `passive_extraction_workflow_latest.py` contains logic to detect this (e.g., if `self.last_processed_index >= len(current_product_list)`). If stale, it usually resets the index to 0 for the new list and may trigger a fresh data fetch for that supplier.
*   The system prioritizes the `linking_map.json` to avoid full re-processing of linked items. The `_processing_state.json` then helps resume iteration over the remaining (unlinked) items for the current batch.

This combination provides both broad (don't re-analyze linked products) and specific (continue from where you left off in the current list) resume capabilities. 