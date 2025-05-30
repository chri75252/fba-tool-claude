# Amazon FBA Agent System v3 - Updated Documentation

This document provides an updated overview of the Amazon FBA Agent System v3, detailing the workflow, configuration, script outputs, and integration notes for the enhanced system. It is designed to help users understand the system components, configuration options, and how to run the tool effectively, including the new test mode and cache clearing toggle.

---

## Overview

The Amazon FBA Agent System v3 is a modular, extensible pipeline designed to analyze supplier products for Amazon FBA profitability. It integrates user-edited core scripts with enhanced modules to provide a comprehensive workflow from supplier scraping to final profit analysis.

---

## Key Scripts and Their Outputs

### 1. `run_complete_fba_analysis.py`

- **Purpose:** Main entry point to run the complete FBA analysis workflow.
- **Functionality:** Orchestrates the entire pipeline, including cache clearing, passive extraction workflow, and result summarization.
- **Outputs:**
  - Analysis reports and summaries are saved under `OUTPUTS/FBA_ANALYSIS/`.----> ELBORATE A BIT MORE ON THE TYPE OF OUTPUT AND INFO IT WILL CONTAIN
  - Detailed execution logs are saved in `logs/complete_analysis.log`. .----> ELBORATE A BIT MORE ON THE TYPE OF OUTPUT AND INFO IT WILL CONTAIN
  - Cache clearing is performed on the directory `OUTPUTS/FBA_ANALYSIS/supplier_cache` if enabled. ---> CLEARNING CACHE, WILL CLEAR ALL THE RECORDED SAVED FILES OR ONLY THE ONES SCRAPED AND NOT ANALYZED ? I WANT IT TO BE THE LATTER, SINCE FIRST I DONT WANT TO REMOVE ALL EXISTING RECORDS WHEN I WANT TO TEST, AND THE SCRIPT USUALLY PRIROTIZES SCRAPED AND NOT ANALYZE PRODUCTS FIRST ( CORRECT ME IF IM WORNG, BUT IN THIS CASE THE TOOL JUMPS STRAIGHT TO THE AMAZON PLAYWRIGHT SCRIPT)
- **Configuration:**
  - Reads configuration from `config/config.json` or inline defaults.
  - Supports a **cache clearing toggle** via the boolean flag `"clear_cache"` in the configuration. ----> SAME QUESTION AS ABOVE ( ALL OR PARTIAL CLEARNING OF EXITING PRODUCT INFO)
  - Supports a `"test_mode"` flag to reduce the number of products processed for faster testing. ----> WHAT DOES TEST_MODE DO EXACTLY ? LIKE WHAT ARE THE PARAMENTERS OF SUCH A RUN VS A REGULAR RUN
- **Usage Example:**
  ```bash
  python Amazon-FBA-Agent-System-v3/run_complete_fba_analysis.py
  ```
- **Test Mode Behavior:**
  - When `"test_mode": true` in the config, the system processes a limited subset of products (e.g., 10) to speed up testing and debugging.
  - Useful for verifying pipeline stages without running full-scale analysis. ----> CONFIRM IF EVEN AI INTEGRATED SCRAPING METHOD WILL BE GURAENTEED TO RUN IN TEST_MODE

---

### 2. `main_orchestrator.py`

- **Purpose:** Coordinates the execution of all workflow modules.
- **Functionality:** Calls core modules such as passive extraction, supplier parsing, price analysis, and FBA fee calculation in sequence.
- **Outputs:**
  - Intermediate and final results are saved to disk in the `OUTPUTS` directory. ----> MENTION HERE OR SEPERATE SECTION ON WHAT EXACTLY ARE THE TYPES OF OUTPUTS WE GET ( WITH EXAMPLES AND FILES CONTENT)
  - Logs detailed progress and errors to the configured logging system.
- **Notes:**
  - The **supplier_api.py** and **currency_converter.py** modules are currently **commented out** and not part of the active workflow.
  - The **price_analyzer.py** is integrated for profitability filtering but can be extended further. ---- > PRICE ANALYZER WILL COME DURING WHICH STEP OF THE PROCESS/TOOL IS IT RIGHT BEFRE FBA FIANCIAL CALC SCRIPT ? IF SO THEN I DONT SEE A PURPORSE FOR IT EVEN IF IT IS PRIOR TO SCRAPING ( COMMENT IT OUT FOR NOW, SINCE IF IM NOT MISTAKEN,IT WILL READ AND USE EXISTING PRICING DATA ( ON ANALYZE PRODUCTS TO "CALCUALTE A PRICE OR PRICE RANGE)
  - The orchestrator respects the `"clear_cache"` flag to clear caches before running.
  - Integrates a persistent linking map to avoid reprocessing products.---> CONFIRM LINKING MAP WILL ALWAYS BE OVERRIDDEN AFTER EVERY TOOL RUN, AND I SAW A BACKUP LINKING MAP FOLDER; EVERY HOW ANY PRODUCTS OR RUN IS A BACKUP CREATED 

---

### 3. `passive_extraction_workflow_latest.py`

- **Purpose:** Implements the passive extraction workflow for supplier product scraping and Amazon data extraction.
- **Functionality:**
  - Performs EAN and title-based Amazon searches.
  - Extracts detailed product data including price, images, sales rank, ratings, and reviews.
  - Calculates FBA fees using integrated `fba_calculator.py`.
  - Maintains a **linking map** (persistent memory) recording processed products, categories, and pages to avoid redundant analysis.
- **Outputs:**
  - Saves detailed product data and linking maps under `OUTPUTS/FBA_ANALYSIS/`. ---> SAME COMMENT AS ABOVE, CLEARLY MENTION THE DIFFERENT FILES AND FOLDERS IN "OUTPUT" AND WHAT THEY CONTAIN AND FROM WHICH SCRIPT
  - Logs progress and warnings to the logging system.
- **Enhancements:**
  - Records additional metadata in the linking map for AI/LLM reference during iterative analyses. ---> WHAT INFO WIL LEAD TO AI (DURING SCRPAING) NOT TO RESUGGEST SAME PAGES/CATEGORIES. AND LIKE HOW IS THIS INFO INTERPERTED BY AI FOR THAT NOT TO HAPPEN
  - Supports `"test_mode"` to limit product processing count.
- **Usage:**
  - Invoked internally by the orchestrator; not typically run standalone.

---

### 4. `config/config.json`

- **Purpose:** Central configuration file for the system.
- **Key Parameters:**
  - `"clear_cache"` (boolean): Enables/disables cache clearing at the start of analysis.
  - `"test_mode"` (boolean): Enables reduced product count for testing.
  - `"max_products_per_supplier"` (integer): Limits the number of products processed per supplier.
  - `"suppliers"` (object): Defines supplier configurations.
  - `"enable_profitable_filtering"` (boolean): Toggles advanced profitability filtering.
  - `"enable_system_monitoring"` (boolean): Enables system health monitoring (currently informational).
- **Example:**
  ```json
  {
    "clear_cache": true,
    "test_mode": false,
    "max_products_per_supplier": 100,
    "suppliers": {
      "default": {}
    },
    "enable_profitable_filtering": true,
    "enable_system_monitoring": true
  }
  ```

---

## Modules Not Currently Integrated (Commented Out)

- **supplier_api.py**
  - Intended for direct API data fetching from suppliers.
  - Currently commented out in the orchestrator.
  - When integrated, it will replace or supplement scraping for suppliers with API access.
- **currency_converter.py**
  - Intended for currency conversion during price analysis.
  - Currently commented out.
  - Will be integrated with price_analyzer for multi-currency support.

---

## Additional Modules and Their Roles

- **supplier_parser.py** ----- > WHAT IS THE DIFFERENCE BETWEEN IT AND BETWEEN THE PASSICE EXTRACT SCRIPT? 
  - Parses supplier-specific data formats.
  - Integrated within the orchestrator to normalize supplier data.
- **price_analyzer.py**  --- > SAME AS ABOVE, WHEN IS IT CALLED UPON AND HOW DIFFERENT IS THE FBA FINANCIAL CALC SCRIPT
  - Performs profitability calculations and filtering.
  - Used in triage stages to identify profitable products.
- **system_monitor.py**  --- > TYPE OF PARAMETERS AND VALUES OR METRICS RECORED AND WHERE TO FIND THEM 
  - Monitors system health and performance during execution.
  - Provides logging and alerts for resource usage.
  - Currently integrated for informational purposes; no active control flow changes.

---

## Data Persistence and Memory System

- **data_store.py** ---> HOW DOES THIS FILE WORK EXACTLY ( LIKE TO ACCOMPLISH THE BELOW ITEMS STATED); IS THIS ALSO PART OF THE "WAY" OF HAVING AI NOT RESUGGEST THE SAME SET OF PRODUCTS ?
  - Provides persistent storage for the linking map and other cached data.
  - Ensures that processed products, categories, and pages are recorded.
  - Supports iterative analysis by preventing reprocessing of the same items.
  - The linking map is saved as JSON files under `OUTPUTS/FBA_ANALYSIS/Linking map/`.
  - This memory system is critical for AI/LLM integration to track what has been analyzed.

---

## Running the Tool - Step by Step

1. **Configure `config/config.json`**
   - Set `"clear_cache"` to `true` to clear caches before each run.
   - Set `"test_mode"` to `true` for quick tests with limited products.
   - Adjust `"max_products_per_supplier"` as needed.
   - Configure suppliers under `"suppliers"`.

2. **Run the Analysis**
   ```bash
   python Amazon-FBA-Agent-System-v3/run_complete_fba_analysis.py
   ```

3. **Outputs**
   - Check `OUTPUTS/FBA_ANALYSIS/` for analysis reports.
   - Review logs in `logs/complete_analysis.log`.
   - Linking maps and cached data are stored under `OUTPUTS/FBA_ANALYSIS/Linking map/`.

4. **Test Mode**
   - When enabled, processes a small subset of products (e.g., 10) for faster iteration.
   - Useful for debugging and verifying pipeline stages without full runs.

---

## Extending to Other Supplier Websites

- The system is designed to be extensible.
- To add new suppliers:
  - Add supplier configurations in `config/config.json`.
  - Implement or extend parsing logic in `supplier_parser.py`.
  - Optionally, implement API integration in `supplier_api.py` (currently commented out).
- The linking map and memory system will track new suppliers and products automatically.

---

## Summary

This updated documentation reflects the current state of the Amazon FBA Agent System v3, including new configuration options, workflow enhancements, and module integration status. It provides clear guidance on running the tool, understanding outputs, and extending the system for new suppliers.

For any questions or further customization, please refer to the source code comments and module docstrings.

---
