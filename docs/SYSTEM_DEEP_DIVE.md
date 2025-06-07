# System Deep Dive: Technical Backend Details (v3.3)

**Version:** 3.3 (AI Optimization + Manual Override Framework)
**Date:** 2025-01-07
**Purpose:** Technical reference for developers and troubleshooting

This document provides detailed technical implementation details, architectural insights, and optimization requirements for the Amazon FBA Agent System v3.3.

## Architecture Overview

### Core Components

#### 1. Main Workflow Engine (`tools/passive_extraction_workflow_latest.py`)
**Purpose:** Primary entry point containing complete workflow logic
**Key Responsibilities:**
- AI category suggestion management with configurable modes
- Product scraping coordination via ConfigurableSupplierScraper
- Amazon data extraction via FixedAmazonExtractor
- Financial analysis and report generation
- State persistence and resume capability

**Class Architecture:**
```python
class PassiveExtractionWorkflow:
    def __init__(self, supplier_name, ai_client=None):
        self.supplier_name = supplier_name
        self.ai_client = ai_client
        self.linking_map = {}
        self.last_processed_index = 0
        self.force_ai_category_progression = False
```

#### 2. AI Category Selection Module
**Purpose:** Configurable AI-driven category discovery with manual override
**Key Features:**
- Legacy vs v2 prompt modes
- Manual category list fallback
- Dynamic re-ordering based on performance metrics
- Comprehensive error handling and recovery

**Configuration Integration:**
```python
ai_config = _load_ai_features_config()
category_config = ai_config.get("category_selection", {})
ai_disabled = category_config.get("disable_ai_category_selection", False)
ai_mode = category_config.get("mode", "legacy").lower()
```

#### 3. Amazon Playwright Extractor (`amazon_playwright_extractor.py`)
**Purpose:** Amazon product data extraction using browser automation
**Key Responsibilities:**
- EAN/UPC-based product matching with title fallback
- Keepa integration for FBA fee calculations
- Comprehensive product data extraction
- Rate limiting and error recovery

#### 4. Configurable Supplier Scraper (`configurable_supplier_scraper.py`)
**Purpose:** Dynamic supplier website scraping with AI fallback
**Key Features:**
- Configuration-driven selector management
- Aiohttp session management for efficiency
- Product validation and filtering
- AI-enhanced extraction fallback

## Data Flow & Caching Strategy

### Cache Management System
**Location:** `tools/cache_manager.py`
**Strategy:** SmartSelectiveStrategy with file-based persistence

**Cache Types:**
1. **Supplier Cache:** `OUTPUTS/cached_products/{supplier}_products_cache.json`
   - Raw product data from supplier websites
   - EAN codes, titles, prices, URLs
   - Age-based validation and refresh logic

2. **Amazon Cache:** `OUTPUTS/FBA_ANALYSIS/amazon_cache/amazon_{ASIN}_{context}.json`
   - Complete Amazon product data including Keepa metrics
   - FBA/FBM seller counts and pricing data
   - Context-based naming for traceability

3. **AI Category Cache:** `OUTPUTS/FBA_ANALYSIS/ai_category_cache/{supplier}_ai_category_cache.json`
   - AI suggestion history with timestamps
   - Performance metrics and validation results
   - Progression strategy documentation

4. **Linking Map:** `OUTPUTS/FBA_ANALYSIS/Linking map/linking_map.json`
   - Confirmed supplier-to-Amazon product mappings
   - Prevents duplicate processing
   - Duplicate entry fallback protection

### Processing State Management
**File:** `OUTPUTS/FBA_ANALYSIS/{supplier}_processing_state.json`
**Purpose:** Resume capability for interrupted workflows
**Schema:**
```json
{
  "last_processed_index": 0,
  "categories_scraped": [],
  "failed_categories": [],
  "category_performance": {},
  "ai_decision_history": []
}
```

## AI Category Selection: v1 vs v2 Detailed Comparison

### Legacy Mode (v1)
**Characteristics:**
- 86-line comprehensive prompt with detailed instructions
- Complex JSON schema with multiple validation layers
- Extensive business context and FBA strategy guidance
- Redundant instruction repetition for emphasis

**Strengths:**
- Comprehensive coverage of business requirements
- Detailed reasoning capture
- Extensive context for complex decisions

**Weaknesses:**
- Token inefficiency (3.4x overhead)
- Cognitive overload leading to inconsistent responses
- Over-specification causing AI confusion
- Contradictory priorities (clearance misclassification)

### v2 Mode (Clearance-First Optimization)
**Characteristics:**
- 25-line focused prompt optimized for arbitrage
- Clear priority hierarchy with clearance emphasis
- Simplified JSON schema
- Performance-based category re-ordering

**Optimizations:**
```python
prompt = f"""AMAZON FBA UK ARBITRAGE CATEGORY ANALYSIS
ROLE: Expert clearance-arbitrage assistant.

{category_performance_summary}

DISCOVERED CATEGORIES:
{formatted}

INSTRUCTIONS
1. Use ONLY URLs above.
2. 🚨 CLEARANCE / DISCOUNT = HIGHEST priority.
3. Return JSON: top_3_urls, secondary_urls, skip_urls, detailed_reasoning

CATEGORY PRIORITY:
▸ HIGHEST : clearance, pound-lines, 50p-under, liquidation
▸ HIGH    : home-kitchen, pet, beauty, baby, toys
▸ MEDIUM  : seasonal, crafts, automotive
▸ AVOID  : electronics, fashion, restricted, adult books

Focus on maximum profit-per-pound. Return ONLY valid JSON."""
```

**Improvements:**
- 70% token reduction (86 → 25 lines)
- Clear clearance prioritization
- Performance-based dynamic re-ordering
- Simplified decision tree

### Dynamic Re-ordering Implementation
**Trigger Conditions:**
- Every 5 categories processed OR
- Every 100 products analyzed

**Re-ordering Logic:**
1. Load category performance metrics from processing state
2. Sort discovered categories by historical success rate
3. Regenerate AI suggestions with performance context
4. Update category processing queue

**Performance Metrics:**
- Products found per category
- Profitable products per category
- Average ROI percentage
- Processing time efficiency

## Configuration System Architecture

### Hierarchical Configuration Loading
**Primary Config:** `config/system_config.json`
**Helper Functions:**
```python
def _load_ai_features_config():
    # Load AI features configuration section
    
def _load_processing_limits_config():
    # Load processing limits and thresholds
```

### Environment Variable Integration
**Rule:** OpenAI credentials ALWAYS hardcoded in scripts
**Rationale:** Reliability and runtime error prevention
**Exception Handling:** Test environment overrides via DISABLE_AI_CATEGORY_SELECTION

### Backwards Compatibility
All existing configuration keys preserved to maintain system stability
New configuration sections additive, not replacement-based

## Performance & Scaling Considerations

### Current Performance Metrics
- **Processing Speed:** 2-3 products per minute
- **Memory Usage:** Stable during infinite runs (~2GB typical)
- **API Efficiency:** 70% token reduction in v2 mode
- **Error Recovery:** Comprehensive fallback mechanisms

### Scaling Opportunities
1. **Parallel Processing:** Architecture ready for 5-8x speed improvement
2. **Advanced Caching:** Intelligent cache warming and preloading
3. **Database Backend:** Replace file-based storage for improved performance
4. **Multi-Supplier Framework:** Generic supplier interface implementation

### Memory Management
**Current Strategy:** File-based persistence with periodic cleanup
**Optimization Targets:**
- Cache size management with automatic rotation
- Memory leak prevention during long runs
- Efficient data structures for large datasets

### Rate Limiting Strategy
**Current Implementation:**
- Intelligent delays between API calls
- Chrome debug port connection management
- Aiohttp session pooling for efficiency

**Future Enhancements:**
- Adaptive rate limiting based on response times
- Circuit breaker patterns for API failures
- Load balancing across multiple API keys

## Critical System Optimizations Identified

### 1. AI Prompt Engineering Crisis (Resolved)
**Problem:** 86-line over-engineered prompt causing 80% profit loss
**Solution:** Implemented v2 mode with 25-line clearance-first optimization
**Impact:** Recovered access to 360+ clearance products (80% profit potential)

### 2. URL Extension Implementation Gap
**Problem:** Only 24 products per category (first page only)
**Required Enhancement:** 
```python
# Add pagination support
url = f"{base_category_url}?product_list_limit=64"
# Implement multi-page crawling: ?p=2&product_list_limit=64, etc.
```
**Expected Impact:** 5x increase in product coverage per category

### 3. Configuration Hygiene Requirements
**Current State:** Mix of hardcoded values and config-driven parameters
**Target State:** All dynamic toggles managed via system_config.json
**Implementation:** Systematic sweep to externalize all runtime flags

## Error Handling & Recovery Architecture

### AI API Protection
```python
try:
    raw = await asyncio.to_thread(
        self.ai_client.chat.completions.create,
        model=model_to_use,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=1200
    )
except Exception as e:
    log.error(f"AI API call failed: {e}")
    return manual_fallback_categories()
```

### Browser Automation Resilience
- Automatic Chrome debug port verification
- Playwright session recovery and restart
- Keepa extension status monitoring
- Rate limiting and backoff strategies

### Cache Corruption Recovery
- Individual file validation and recovery
- Automatic backup creation before modifications
- Selective cache rebuilding from source data
- Integrity checking with detailed logging

## Development Lessons Learned

### Configuration Management
**Lesson:** Only document and support tested configuration combinations
**Implementation:** Mark untested parameters with clear warnings
**Rationale:** Prevents system instability from experimental settings

### AI Integration Complexity
**Lesson:** Simpler prompts often outperform complex ones
**Evidence:** v2 mode (25 lines) > v1 mode (86 lines) in consistency
**Application:** Focus on clear priorities over comprehensive coverage

### Cache Strategy Evolution
**Lesson:** File-based persistence sufficient for current scale
**Rationale:** JSON files provide transparency and debugging ease
**Future:** Database migration planned for multi-supplier scaling

### Error Recovery Philosophy
**Principle:** Graceful degradation over complete failure
**Implementation:** Manual fallbacks for all AI-dependent operations
**Result:** System continues operation even during API outages

## Future Development Roadmap

### Phase 1: Core Optimizations (Current)
- AI v2 mode implementation and testing
- Configuration hygiene and externalization
- URL extension and pagination support
- Dynamic re-ordering validation

### Phase 2: Performance Scaling
- Parallel processing implementation
- Advanced caching strategies
- Memory optimization and cleanup
- Database backend preparation

### Phase 3: Multi-Supplier Framework
- Generic supplier interface development
- Configuration template system
- Normalized data processing pipeline
- Cross-supplier analytics

### Phase 4: Advanced Analytics
- Predictive modeling integration
- Market trend analysis
- Seasonal demand forecasting
- GPU-accelerated processing evaluation

## Debugging and Diagnostics

### Log Analysis Patterns
```bash
# AI decision tracking
grep "AI CATEGORY SELECTION" *.log

# Performance monitoring
grep "Processing speed\|products per minute" *.log

# Error pattern analysis
grep "ERROR\|FAILED\|Exception" *.log | sort | uniq -c
```

### Cache Validation Commands
```bash
# Verify AI cache integrity
python -c "import json; print(json.load(open('OUTPUTS/FBA_ANALYSIS/ai_category_cache/clearance-king_co_uk_ai_category_cache.json')))"

# Check processing state consistency
type "OUTPUTS\FBA_ANALYSIS\clearance-king_co_uk_processing_state.json"

# Validate linking map structure
python -c "import json; data=json.load(open('OUTPUTS/FBA_ANALYSIS/Linking map/linking_map.json')); print(f'Entries: {len(data)}')"
```

### Performance Profiling
- Memory usage tracking during long runs
- API response time monitoring
- Category processing efficiency metrics
- Error rate and recovery success tracking

---

**See also:** `Claude.md` for live progress tracking and session continuity
**Configuration Reference:** `SYSTEM_CONFIG_TOGGLES.md` for complete parameter documentation
**User Guide:** `README.md` for operational procedures and quick start