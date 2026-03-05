# CLARA Agent Specification

This document describes the contracts and responsibilities for the 3 agents in the CLARA pipeline.

---

## Agent 1: Triage Agent

**File**: `agents/triage_agent.py`

**Responsibility**: Receives a complaint_id, loads the complaint from S3, classifies category and priority, pulls matching transactions for that customer from S3

**Input**: 
- `complaint_id` (string) - UUID of the complaint to process

**Output**: Dictionary containing:
```python
{
    "complaint_id": "uuid",
    "customer_id": "uuid",
    "category": "string",  # e.g., "billing_dispute", "fraud", "account_access"
    "priority": "string",  # e.g., "low", "medium", "high", "critical"
    "sentiment": "string",  # e.g., "negative", "very_negative", "neutral"
    "confidence_score": 0.0,  # float between 0.0 and 1.0
    "matched_transactions": []  # list of transaction dicts
}
```

**Tools Needed**:
- Read complaints from S3 (`synthetic_data/complaints/complaints.json`)
- Read customers from S3 (`synthetic_data/customers/customers.json`)
- Read transactions from S3 (`synthetic_data/transactions/transactions.json`)

**Escalate If**:
- Complaint cannot be classified with confidence above 0.5
- Customer data or complaint data not found in S3

---

## Agent 2: Resolution Agent

**File**: `agents/resolution_agent.py`

**Responsibility**: Takes triage output, drafts a resolution letter using Bedrock Claude 3.7 Sonnet, then queries Bedrock Knowledge Base to check the draft against compliance rules

**Input**: Triage output dict (from Agent 1)

**Output**: Dictionary containing:
```python
{
    "complaint_id": "uuid",
    "customer_id": "uuid",
    "risk_score": 0.0,  # from customer record
    "draft_letter": "string",  # full resolution letter text
    "confidence_score": 0.0,  # float between 0.0 and 1.0
    "compliance_results": [
        {
            "rule_id": "CR-001",
            "result": "pass"  # or "warn" or "block"
        }
    ]
}
```

**Tools Needed**:
- Invoke Bedrock for drafting resolution letter
- Query Bedrock Knowledge Base for compliance check
- Read customer risk_score from S3

**Escalate If**:
- Any compliance rule returns "block"
- confidence_score is below 0.5
- Unable to draft letter due to insufficient information

---

## Agent 3: Decision Agent

**File**: `agents/decision_agent.py`

**Responsibility**: Makes the final call — resolve or escalate based on confidence score, risk score, and compliance results

**Input**: Resolution agent output dict + customer risk_score

**Output**: Dictionary containing:
```python
{
    "complaint_id": "uuid",
    "final_status": "resolved",  # or "escalated"
    "resolution_letter": "string or null",  # full letter if resolved, null if escalated
    "escalation_reason": "string or null",  # human-readable reason if escalated
    "audit_trail": [
        {
            "stage": "string",
            "result": "string",
            "timestamp": "ISO8601"
        }
    ]
}
```

**Decision Logic**:
- **RESOLVE** if ALL of the following are true:
  - confidence_score >= 0.5
  - risk_score <= 0.85
  - No compliance rules returned "block"
  - Complaint category is NOT "fraud"
  - If refund mentioned, amount is <= $500

- **ESCALATE** if ANY of the following are true:
  - confidence_score < 0.5 → reason: "confidence score below threshold"
  - risk_score > 0.85 → reason: "customer risk score above 0.85"
  - Any compliance rule returned "block" → reason: "compliance rule violation detected"
  - Complaint category is "fraud" → reason: "fraud complaint requires specialized team"
  - Refund amount > $500 → reason: "high value refund requires approval"
  - Complaint age > 72 hours → reason: "SLA breach detected"

**Tools Needed**:
- Write final status to S3
- Write record to audit log
- Calculate complaint age from submission timestamp

---

## Pipeline Entry Point

**File**: `pipeline.py`

**Responsibility**: Orchestrates the 3 agents in sequence and handles command-line invocation

**Flow**:
1. Parse command-line argument for `complaint_id`
2. Call Triage Agent with `complaint_id`
3. Call Resolution Agent with triage output
4. Call Decision Agent with resolution output
5. Print final result to terminal as formatted JSON

**Command-Line Usage**:
```bash
python pipeline.py --complaint-id <uuid>
```

**Output Format**:
```json
{
  "complaint_id": "uuid",
  "final_status": "resolved",
  "resolution_letter": "Dear Customer...",
  "escalation_reason": null,
  "processing_time_ms": 3450,
  "audit_trail": [...]
}
```

---

## Data Contracts Between Agents

### Triage Agent → Resolution Agent

```python
{
    "complaint_id": "uuid",
    "customer_id": "uuid",
    "category": "string",
    "priority": "string",
    "sentiment": "string",
    "confidence_score": 0.0,
    "matched_transactions": []
}
```

### Resolution Agent → Decision Agent

```python
{
    "complaint_id": "uuid",
    "customer_id": "uuid",
    "risk_score": 0.0,
    "draft_letter": "string",
    "confidence_score": 0.0,
    "compliance_results": [
        {
            "rule_id": "CR-001",
            "result": "pass/warn/block"
        }
    ]
}
```

### Decision Agent → Pipeline (Final Output)

```python
{
    "complaint_id": "uuid",
    "final_status": "resolved or escalated",
    "resolution_letter": "string or null",
    "escalation_reason": "string or null",
    "audit_trail": []
}
```

---

## Error Handling

All agents must handle these error cases:

1. **S3 Read Failures**: Escalate with reason "data retrieval error"
2. **Bedrock API Failures**: Retry once, then escalate with reason "AI service unavailable"
3. **Knowledge Base Query Failures**: Escalate with reason "compliance check failed"
4. **Invalid Input Data**: Escalate with reason "invalid complaint data"
5. **Timeout**: If any agent takes > 30 seconds, escalate with reason "processing timeout"

---

## Logging and Audit Trail

Every agent invocation must log:
- Agent name and version
- Input parameters
- Output results
- Execution time (ms)
- Any errors or warnings

Audit records should be written to `synthetic_data/compliance/audit_log.json` with this structure:

```python
{
    "audit_id": "uuid",
    "complaint_id": "uuid",
    "rule_id": "string or null",
    "checked_at": "ISO8601",
    "result": "pass/warn/block",
    "escalated": true/false,
    "escalation_reason": "string or null",
    "pipeline_stage": "classification/data_pull/draft_generation/compliance_check/resolution/escalation",
    "agent_name": "triage-agent-v1/resolution-agent-v1/decision-agent-v1",
    "invocation_latency_ms": 0
}
```
