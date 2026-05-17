# Multi-Agent Platform: Usage Examples

## CRM Lead Qualifier Examples

### Example 1: Check a Software Company Lead

**Input Email**: `jane@acmecorp.com`

**Agent Process**:
1. Extract domain: `acmecorp.com`
2. Look up company info:
   - Industry: Software/SaaS
   - Size: 501-1000 employees
   - Revenue: $50M - $100M
3. Check CRM history:
   - Last contact: 2025-11-15
   - Status: Cold Lead
   - Notes: "Attended webinar, no follow-up yet."
4. Calculate score:
   - Revenue range ($50M) → Medium factor
   - Status (Cold Lead) → Medium factor
   - **Result: MEDIUM score**
5. Generate summary and recommendation

**Expected Output**:
```
Jane from AcmeCorp is a medium-priority lead. The company is a mid-sized SaaS 
organization in the $50M-$100M revenue range, which aligns with our target market. 
However, as a cold lead with only a webinar attendance on record, follow-up is needed 
to gauge interest. Recommendation: Send targeted nurture email with product relevance 
to their company size and industry.
```

---

### Example 2: Check an Active Opportunity

**Input Email**: `bob@widgetco.net`

**Agent Process**:
1. Extract domain: `widgetco.net`
2. Look up company info:
   - Industry: Manufacturing
   - Size: 100-250 employees
   - Revenue: $10M - $25M
3. Check CRM history:
   - Last contact: 2025-12-01 (recent)
   - Status: Active Opportunity
   - Notes: "Discussed Q1 budget and product integration."
4. Calculate score:
   - Revenue range ($10-25M) → Lower factor
   - Status (Active Opportunity) → High factor
   - **Result: HIGH score**
5. Generate summary and recommendation

**Expected Output**:
```
Bob from WidgetCo is a high-priority lead. Despite the company's smaller size, 
they represent an active opportunity with strong engagement. Recent discussion about 
Q1 budgeting and technical integration indicates serious buying intent. This is a 
warm lead with momentum. Recommendation: Schedule technical deep-dive meeting and 
prepare proposal tailored to their Q1 timeline.
```

---

### Example 3: New Unknown Lead

**Input Email**: `contact@startupcorp.io`

**Agent Process**:
1. Extract domain: `startupcorp.io`
2. Look up company info:
   - Result: Not in database → Unknown/N/A
3. Check CRM history:
   - Result: No CRM record found → New lead
4. Calculate score:
   - Revenue: Unknown → Low factor
   - Status: No Record → New/Cold → Low factor
   - **Result: LOW score**
5. Generate summary and recommendation

**Expected Output**:
```
contact@startupcorp.io is a new prospect from an unknown organization. There's no 
prior CRM history or company data available in our systems. This is a first-contact 
opportunity. Recommendation: Research the company independently (Crunchbase, LinkedIn), 
verify fit with our target market, then send an exploratory outreach email with 
personalized context.
```

---

## CSV FAQ Agent Examples

### Example 1: Hospital Policy Lookup

**Upload File**: `hospital_policy.csv`

**Sample Questions**:
1. "What is the visitor policy for ICU patients?"
   - Agent searches CSV and returns specific policy details
   
2. "What are the discharge instructions for post-operative care?"
   - Agent finds and summarizes relevant policies
   
3. "When can family members visit in the maternity ward?"
   - Agent extracts ward-specific visiting hours

---

### Example 2: E-Commerce FAQ

**Upload File**: `ecommerce_faqs.csv`

**Sample Questions**:
1. "What is your return policy?"
   - Agent searches FAQ and returns return window, conditions, refund timeline
   
2. "How long does shipping typically take?"
   - Agent provides shipping time estimates based on product type
   
3. "Do you offer international shipping?"
   - Agent finds shipping region information

---

### Example 3: SaaS Documentation

**Upload File**: `saas_docs.csv`

**Sample Questions**:
1. "What are the API rate limits?"
   - Agent returns rate limit documentation
   
2. "How do I authenticate with the API?"
   - Agent provides authentication methods and examples
   
3. "What payment methods do you accept?"
   - Agent lists accepted payment options

---

## Advanced Scenarios

### Scenario 1: Batch Lead Qualification (CSV)

**Process**:
1. Upload CSV with multiple leads in Tab 1
2. Use CSV FAQ in Tab 2 to extract leads
3. Manually run each lead through CRM Qualifier in Tab 3

**Example CSV**:
```csv
email,company,role
jane@acmecorp.com,AcmeCorp,VP Engineering
bob@widgetco.net,WidgetCo,Sales Director
sarah@globalfin.org,GlobalFin,CFO
```

---

### Scenario 2: Multi-Step Lead Investigation

**Step 1**: Enter lead email in CRM Qualifier → Get initial score

**Step 2**: If interested, ask CSV FAQ:
- "What are case studies in their industry?"
- "What are pricing tiers for their company size?"

**Step 3**: Generate personalized outreach email based on combined insights

---

### Scenario 3: Custom Lead Analysis

**In CRM Qualifier**:
- Email: `contact@techcorp.com`
- Custom Instructions: "Focus on technical fit. We're a B2B SaaS with enterprise features."

**Agent will**:
- Adjust scoring to emphasize company size and tech-readiness
- Provide recommendations tailored to your specific business model

---

## Integration Testing Checklist

### Tab 1 & 2: CSV FAQ Agent
- [ ] Upload single CSV file
- [ ] Upload multiple CSV files
- [ ] View data preview (rows, columns, size)
- [ ] Ask question about data
- [ ] See answer with data references
- [ ] Check question history

### Tab 3: CRM Lead Qualifier
- [ ] Enter known lead email (`jane@acmecorp.com`)
- [ ] See agent call tools in real-time
- [ ] Receive lead score and summary
- [ ] Check lead history
- [ ] Enter custom instructions
- [ ] Enter unknown lead email
- [ ] Verify graceful handling of new leads

### Configuration
- [ ] Enter API key in sidebar
- [ ] See success message
- [ ] Switch between tabs without issues
- [ ] Session state persists across tabs

---

## Performance Tips

### CSV FAQ Agent
- **Smaller CSVs (<5MB)**: Fast, 1-2 seconds response time
- **Larger CSVs (>10MB)**: May take 5-10 seconds
- **Multiple files**: Response time scales linearly
- **Pro tip**: Upload only relevant files to speed up agent processing

### CRM Lead Qualifier
- **First run**: 2-3 seconds (model initialization)
- **Subsequent runs**: 1-2 seconds per lead
- **API limit**: 3000 requests/minute (OpenAI free tier)
- **Pro tip**: Batch similar leads to optimize API usage

---

## Error Handling

### Common Errors & Solutions

**"Error: Import tabulate failed"**
- Solution: Run `pip install tabulate`

**"API key not working"**
- Check: Is key valid and not rate-limited?
- Check: Does key have access to gpt-4o and gpt-4o-mini?

**"Lead not found in CRM"**
- Expected: New leads will show "No Record"
- Solution: Research company independently before outreach

**"CSV not loading"**
- Check: File format is CSV (not XLSX)
- Check: File has headers in first row
- Check: No special characters in column names

---

## Data Privacy Notes

- ✅ API keys are session-only (not persisted)
- ✅ CSV data is processed in-memory only
- ✅ No data is stored after session ends
- ✅ CRM data in demo is mocked (for testing)
- ⚠️ When connecting to real CRM: ensure compliance with data protection laws

---

**Last Updated**: May 16, 2026  
**Platform Version**: 1.0 (Multi-Agent Edition)
