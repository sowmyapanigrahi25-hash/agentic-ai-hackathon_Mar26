# CLARA Synthetic Data Generation Summary

## ✓ Generation Complete

All synthetic data and scaffold files have been successfully generated for the CLARA project.

---

## Data Entities Generated

### Entity 1: Customers ✓
- **Location**: `synthetic_data/customers/`
- **Files**: `customers.json`, `customers.csv`
- **Records**: 150
- **Special Features**:
  - 10 high-risk customers (risk_score > 0.85 AND complaints > 3)
  - 5 new customers with no transaction history
  - 5% malformed phone numbers
  - Mixed ethnicities and regions

### Entity 2: Complaints ✓
- **Location**: `synthetic_data/complaints/`
- **Files**: `complaints.json`, `complaints.csv`
- **Records**: 300
- **Special Features**:
  - Realistic raw_text with typos and emotional language
  - 2% all caps complaints
  - 2% duplicate complaints
  - 2% spam/irrelevant
  - 2% mixed language (Spanish/Hindi)
  - Category distribution: 40% billing/fraud, 25% access, 20% refund, 15% other

**Sample Complaint Texts** (demonstrating realism):
1. "i think someone stole my card info. seeing charges from places ive never been"
2. "your website is broken. i cant login no matter what i do"
3. "can someone explain why theres a $344 charge from Amazon? i didnt buy anything"
4. "account locked after i entered wrong pin. how do i unlock it"
5. "my card got declined at the store even though i have money in my account"

### Entity 3: Transactions ✓
- **Location**: `synthetic_data/transactions/`
- **Files**: `transactions.json`, `transactions.csv`
- **Records**: 1000
- **Special Features**:
  - 30% of complaints have matching transactions
  - 10 complaints have NO matching transactions
  - 20 suspicious transactions (round amounts, foreign merchants, rapid duplicates)
  - 0 transactions for the 5 new customers (verified)

### Entity 4: Compliance Rules ✓
- **Location**: `synthetic_data/compliance/`
- **Files**: `compliance_rules.json` + 15 `.txt` files in `compliance_rules_txt/`
- **Records**: 15 rules (CR-001 through CR-015)
- **Categories**: refund_policy, fraud_protocol, communication_standard, escalation_trigger, data_privacy
- **Severities**: block, warn, info
- **Key Rules**:
  - CR-001: High value refund approval (>$500) - BLOCK
  - CR-002: SLA breach (>72 hours) - BLOCK
  - CR-003: No admission of liability - BLOCK
  - CR-004: High risk customer review (>0.85) - BLOCK
  - CR-005: Fraud routing protocol - BLOCK
  - CR-006: PII protection in logs - BLOCK

### Entity 5: Resolution Letters ✓
- **Location**: `synthetic_data/resolution_letters/`
- **Files**: `resolution_letters.json`
- **Records**: 100
- **Special Features**:
  - 20 letters with confidence_score < 0.5
  - 3 letters with final_status = rejected
  - Rejected letters contain compliance violations (liability admission, missing sign-off, uncommitted refund)
  - Professional bank letter format with proper structure

### Entity 6: Audit Log ✓
- **Location**: `synthetic_data/compliance/`
- **Files**: `audit_log.json`, `audit_log.csv`
- **Records**: 500
- **Special Features**:
  - 15% escalated records (75 total)
  - All 6 pipeline stages represented
  - Agent names consistent with stages
  - Realistic latency: 800-4500ms for draft/compliance, 50-300ms for classification/data_pull

---

## Scaffold Files Generated

### 1. pipeline_manifest.json ✓
Complete project manifest with:
- S3 bucket and prefix configuration
- Bedrock model ID and Knowledge Base configuration
- Agent definitions and responsibilities
- Thresholds (confidence, risk, SLA)
- Data entity metadata with row counts

### 2. config.py ✓
Configuration management with:
- Environment variable loading via python-dotenv
- Required variables: S3_BUCKET_NAME, COMPLIANCE_KB_ID
- Optional variables: AWS_REGION (default: us-east-1), BEDROCK_MODEL_ID
- Hardcoded thresholds: CONFIDENCE_THRESHOLD, RISK_SCORE_THRESHOLD, SLA_BREACH_HOURS
- validate_config() function with helpful error messages

### 3. requirements.txt ✓
Minimal dependencies:
- strands-agents
- strands-agents-tools
- boto3
- bedrock-agentcore
- python-dotenv

### 4. README.md ✓
Complete documentation with:
- Project overview
- 3-agent pipeline description
- Setup instructions
- How to run
- Folder structure
- Data summary table
- Tech stack
- Escalation conditions

### 5. kiro_spec.md ✓
Detailed agent specifications with:
- Agent 1: Triage Agent contract
- Agent 2: Resolution Agent contract
- Agent 3: Decision Agent contract
- Pipeline entry point specification
- Data contracts between agents
- Error handling requirements
- Logging and audit trail format

---

## Data Integrity Verification

All integrity checks passed:

✓ Every customer_id in complaints exists in customers (300/300)
✓ Every customer_id in transactions exists in customers, excluding 5 new customers (1000/1000)
✓ Every complaint_id in audit_log exists in complaints (500/500)
✓ Every rule_id in audit_log exists in compliance_rules (when not null)
✓ Every complaint_id in resolution_letters exists in complaints (100/100)
✓ All 15 compliance rule .txt files exist in compliance_rules_txt/
✓ Complaint raw_text fields sound realistic (not AI-generated)

---

## Final Summary Table

| Entity              | Expected | Generated | Integrity Check |
|---------------------|----------|-----------|-----------------|
| customers           | 150      | 150       | ✓               |
| complaints          | 300      | 300       | ✓               |
| transactions        | 1000     | 1000      | ✓               |
| compliance_rules    | 15       | 15        | ✓               |
| audit_log           | 500      | 500       | ✓               |
| resolution_letters  | 100      | 100       | ✓               |
| scaffold_files      | 5        | 5         | ✓               |

---

## Next Steps

1. **Upload to S3**:
   ```bash
   aws s3 sync synthetic_data/ s3://your-bucket-name/synthetic_data/
   ```

2. **Create Bedrock Knowledge Base**:
   - Point data source to: `s3://your-bucket-name/synthetic_data/compliance/compliance_rules_txt/`
   - Note the Knowledge Base ID

3. **Configure Environment**:
   - Create `.env` file with S3_BUCKET_NAME, COMPLIANCE_KB_ID, AWS_REGION

4. **Install Dependencies**:
   ```bash
   cd clara
   pip install -r requirements.txt
   ```

5. **Build the 3 Agents**:
   - Implement `agents/triage_agent.py`
   - Implement `agents/resolution_agent.py`
   - Implement `agents/decision_agent.py`
   - Implement tools in `agents/tools/`

6. **Build Pipeline**:
   - Implement `pipeline.py` to orchestrate the 3 agents

---

## CLARA synthetic data and scaffold generation complete. Ready to push to Git.
