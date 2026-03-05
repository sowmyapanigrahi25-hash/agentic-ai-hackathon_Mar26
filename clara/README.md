# CLARA — Complaint Learning & Agentic Resolution Assistant

CLARA is a fully agentic complaint resolution pipeline built for an AWS hackathon. It receives a customer complaint, processes it through 3 AI agents, and either resolves it automatically or escalates it to a human.

## The 3-Agent Pipeline

1. **Triage Agent** - Classifies the complaint, assigns priority, pulls matching transactions from S3
2. **Resolution Agent** - Drafts a resolution letter using Bedrock Claude 3.7 Sonnet, then checks it against compliance rules using Bedrock Knowledge Base (RAG)
3. **Decision Agent** - If confidence_score >= 0.5 AND risk_score <= 0.85, closes the ticket. Otherwise escalates to human.

## Setup Instructions

### 1. Install Dependencies

```bash
cd clara
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `clara/` directory with the following variables:

```
S3_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1
COMPLIANCE_KB_ID=your-knowledge-base-id
BEDROCK_MODEL_ID=anthropic.claude-3-7-sonnet-20250219
```

### 3. Upload Synthetic Data to S3

Upload the contents of `synthetic_data/` to your S3 bucket:

```bash
aws s3 sync synthetic_data/ s3://your-bucket-name/synthetic_data/
```

### 4. Create Bedrock Knowledge Base

Create a Bedrock Knowledge Base backed by the compliance rules:

```bash
# Point your KB data source to:
s3://your-bucket-name/synthetic_data/compliance/compliance_rules_txt/
```

## How to Run

```bash
python pipeline.py --complaint-id <uuid>
```

Example:
```bash
python pipeline.py --complaint-id a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

## Folder Structure

```
clara/
├── synthetic_data/
│   ├── customers/
│   │   ├── customers.json (150 records)
│   │   └── customers.csv
│   ├── complaints/
│   │   ├── complaints.json (300 records)
│   │   └── complaints.csv
│   ├── transactions/
│   │   ├── transactions.json (1000 records)
│   │   └── transactions.csv
│   ├── compliance/
│   │   ├── compliance_rules.json (15 rules)
│   │   ├── audit_log.json (500 records)
│   │   ├── audit_log.csv
│   │   └── compliance_rules_txt/ (15 .txt files)
│   └── resolution_letters/
│       └── resolution_letters.json (100 records)
├── agents/
│   ├── triage_agent.py
│   ├── resolution_agent.py
│   ├── decision_agent.py
│   └── tools/
│       ├── s3_tools.py
│       ├── bedrock_kb_tools.py
│       └── audit_tools.py
├── pipeline.py
├── pipeline_manifest.json
├── kiro_spec.md
├── config.py
├── requirements.txt
└── README.md
```

## Data Summary

| Entity              | Row Count | Primary Key      | Foreign Key   |
|---------------------|-----------|------------------|---------------|
| customers           | 150       | customer_id      | -             |
| complaints          | 300       | complaint_id     | customer_id   |
| transactions        | 1000      | transaction_id   | customer_id   |
| compliance_rules    | 15        | rule_id          | -             |
| audit_log           | 500       | audit_id         | complaint_id  |
| resolution_letters  | 100       | letter_id        | complaint_id  |

## Tech Stack

- **Framework**: Strands Agents SDK
- **AWS Services**: Amazon Bedrock (Claude 3.7 Sonnet), Bedrock Knowledge Bases, S3
- **Python**: 3.11+
- **Libraries**: strands-agents, strands-agents-tools, boto3, bedrock-agentcore

## Escalation Conditions

- confidence_score below 0.5 → escalate
- customer risk_score above 0.85 → escalate
- complaint unresolved for more than 72 hours → escalate
- fraud category complaint → always route to fraud team
- refund amount above $500 → requires human approval
