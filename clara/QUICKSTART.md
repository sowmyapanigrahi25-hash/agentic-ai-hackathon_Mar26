# CLARA Quick Start Guide

## What Was Generated

✓ 150 customers with realistic profiles
✓ 300 complaints with authentic frustrated customer language
✓ 1000 transactions across multiple merchants
✓ 15 compliance rules (JSON + individual .txt files for RAG)
✓ 500 audit log records
✓ 100 resolution letters
✓ 5 scaffold files (manifest, config, requirements, README, spec)

## Test the Data Locally

### 1. Verify Data Integrity

```bash
cd clara
python -c "import json; print('Customers:', len(json.load(open('synthetic_data/customers/customers.json')))); print('Complaints:', len(json.load(open('synthetic_data/complaints/complaints.json')))); print('Transactions:', len(json.load(open('synthetic_data/transactions/transactions.json'))))"
```

### 2. Sample a Complaint

```bash
python -c "import json; c = json.load(open('synthetic_data/complaints/complaints.json'))[0]; print(f'Complaint ID: {c[\"complaint_id\"]}'); print(f'Customer ID: {c[\"customer_id\"]}'); print(f'Category: {c[\"category\"]}'); print(f'Text: {c[\"raw_text\"]}')"
```

Example output:
```
Complaint ID: ff3fb573-9994-4e30-aada-a7069187634b
Customer ID: d9874677-f96b-4061-8cb4-c614248cbccd
Category: billing_dispute
Text: i was charged twice for the same thing last week. This is ridiculous, fix it NOW.
```

### 3. Check Compliance Rules

```bash
ls synthetic_data/compliance/compliance_rules_txt/
```

Should show: CR-001.txt through CR-015.txt

### 4. Validate Config

```bash
python config.py
```

Will show missing environment variables (expected before AWS setup).

## Deploy to AWS

### Step 1: Create S3 Bucket

```bash
aws s3 mb s3://clara-hackathon-data-[your-name]
```

### Step 2: Upload Synthetic Data

```bash
aws s3 sync synthetic_data/ s3://clara-hackathon-data-[your-name]/synthetic_data/
```

### Step 3: Create Bedrock Knowledge Base

1. Go to AWS Console → Bedrock → Knowledge Bases
2. Create new Knowledge Base
3. Data source: S3
4. S3 URI: `s3://clara-hackathon-data-[your-name]/synthetic_data/compliance/compliance_rules_txt/`
5. Embedding model: Titan Embeddings G1 - Text
6. Note the Knowledge Base ID

### Step 4: Configure Environment

Create `.env` file:

```bash
S3_BUCKET_NAME=clara-hackathon-data-[your-name]
AWS_REGION=us-east-1
COMPLIANCE_KB_ID=[your-kb-id-from-step-3]
BEDROCK_MODEL_ID=anthropic.claude-3-7-sonnet-20250219
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Test Configuration

```bash
python config.py
```

Should show: ✓ Configuration validated successfully

## Sample Complaint IDs for Testing

Use these complaint_ids when testing your pipeline:

```
ff3fb573-9994-4e30-aada-a7069187634b  (billing_dispute)
```

To get more:
```bash
python -c "import json; complaints = json.load(open('synthetic_data/complaints/complaints.json')); [print(f'{c[\"complaint_id\"]} ({c[\"category\"]})') for c in complaints[:10]]"
```

## Next: Build the Agents

Follow `kiro_spec.md` to implement:
1. `agents/triage_agent.py`
2. `agents/resolution_agent.py`
3. `agents/decision_agent.py`
4. `agents/tools/s3_tools.py`
5. `agents/tools/bedrock_kb_tools.py`
6. `agents/tools/audit_tools.py`
7. `pipeline.py`

## Data Characteristics

- **Realistic complaints**: Typos, emotional language, vague references
- **High-risk customers**: 10 customers with risk_score > 0.85
- **Suspicious transactions**: 20 transactions with fraud indicators
- **Compliance violations**: 3 rejected letters with violations
- **Edge cases**: Spam complaints, mixed languages, duplicates

## Folder Structure

```
clara/
├── synthetic_data/          # All generated data
│   ├── customers/
│   ├── complaints/
│   ├── transactions/
│   ├── compliance/
│   └── resolution_letters/
├── agents/                  # To be implemented
│   ├── triage_agent.py
│   ├── resolution_agent.py
│   ├── decision_agent.py
│   └── tools/
├── pipeline.py              # To be implemented
├── config.py                # ✓ Ready
├── requirements.txt         # ✓ Ready
├── README.md                # ✓ Ready
├── kiro_spec.md             # ✓ Ready
└── pipeline_manifest.json   # ✓ Ready
```

## Ready to Code!

All synthetic data is generated and validated. Start building the agents using Strands SDK!
