# Network Bounty Hunter Agent - Implementation Plan

**Project Overview**: AI-powered network monitoring and outreach agent that turns 'I need X' into ranked contacts, tailored outreach drafts, follow-up schedules, and a pipeline board.

**Built with**: Google Cloud Platform Agent Starter Pack (adk_base)
**Date**: December 19, 2025

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Data Models & Schemas](#data-models--schemas)
4. [Core Components](#core-components)
5. [Implementation Phases](#implementation-phases)
6. [Technology Stack](#technology-stack)
7. [Deployment Strategy](#deployment-strategy)
8. [Security & Compliance](#security--compliance)
9. [Testing Strategy](#testing-strategy)
10. [Next Steps](#next-steps)

---

## Executive Summary

### Vision
Build a production-ready AI agent that automates network discovery, contact ranking, personalized outreach generation, and relationship pipeline management. The agent bridges the gap between expressing a need ("I need X") and actionable, ranked opportunities with ready-to-send communications.

### Key Capabilities
- **Multi-source signal ingestion**: LinkedIn (via Comet automation), RSS feeds, news, grants, jobs, events
- **Intelligent ranking**: Scores contacts based on relevance, relationship strength, recency, and connector leverage
- **Personalized outreach**: Generates tailored messages grounded in context and relationship history
- **Pipeline management**: Kanban board with automated follow-up scheduling and outcome tracking
- **Privacy-first**: Human-in-the-loop for LinkedIn, no scraping, requires explicit user confirmation for sends

### Success Criteria
- Agent successfully parses 'I need X' into actionable NeedSpec
- Returns ranked contact list with justification in <2 seconds
- Generates personalized outreach drafts with 90%+ user acceptance
- Pipeline board updates reflect all agent actions in real-time
- Zero security incidents, full compliance with privacy guidelines
- Cost: $0-50/month (free tier GCP + free tools)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERACTION LAYER                      │
│  - Web UI (Future: React/Next.js)                                   │
│  - API Interface (FastAPI via adk_base App)                         │
│  - Comet Integration (Browser automation for LinkedIn)               │
└──────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          AGENT CORE (ADK)                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  NeedSpec Parser │  │  Contact Ranker  │  │  Draft Generator │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  Follow-up Sched │  │  Pipeline Manager│  │  Signal Ingester │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  PostgreSQL DB   │  │  Cloud Storage   │  │  Vector Store   │  │
│  │  (Cloud SQL)     │  │  (Signal Dumps)  │  │  (Future: RAG)  │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                          SIGNAL SOURCES                              │
│  - LinkedIn (Comet automation)      - RSS Feeds                      │
│  - Google News API                  - Grants.gov                     │
│  - Job Boards                       - GitHub Releases                │
│  - Event Pages                      - Manual Imports                 │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **User Input**: "I need a packaging engineer with bioplastics experience in NYC"
2. **NeedSpec Parser**: Extracts objective, persona, geography, keywords
3. **Signal Retrieval**: Queries recent signal dumps + existing network DB
4. **Contact Ranking**: Scores and ranks all matches
5. **Draft Generation**: Creates personalized outreach for top N contacts
6. **Pipeline Creation**: Generates cards with follow-up schedule
7. **User Review**: Human approves/edits drafts before send

---

## Data Models & Schemas

### Core Entities

#### 1. NeedSpec
```python
class NeedSpec(BaseModel):
    id: str
    created_at: datetime
    user_id: str
    raw_input: str  # "I need X"
    objective_type: Literal["intro", "hire", "sell", "raise", "partner", "advisor", "press"]
    target_persona: dict  # {"title": [...], "industry": [...], "company_type": [...]}
    geography: Optional[List[str]]
    keywords_must: List[str]
    keywords_avoid: List[str]
    time_urgency: Literal["high", "medium", "low"]
    ask_shape: str  # "30-min intro call", "pilot partnership", etc.
```

#### 2. SignalDump
```python
class SignalDump(BaseModel):
    id: str
    source: Literal["linkedin_comet", "rss", "news", "jobs", "grants", "github", "events", "manual"]
    run_id: str
    run_ts: datetime
    query_pack_id: Optional[str]
    items: List[SignalItem]

class SignalItem(BaseModel):
    type: Literal["person", "company", "opportunity", "content"]
    data: Union[PersonLead, CompanyLead, OpportunityLead, ContentLead]
```

#### 3. Contact & Lead
```python
class Contact(BaseModel):
    id: str
    name: str
    title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    profile_url: Optional[str]
    relationship_strength: float  # 0-1
    last_interaction: Optional[datetime]
    tags: List[str]
    notes: str
```

#### 4. PipelineCard
```python
class PipelineCard(BaseModel):
    id: str
    need_spec_id: str
    contact_id: str
    stage: Literal["backlog", "candidates", "drafted", "sent", "follow_up_1", "follow_up_2", "warm_intro", "closed_won", "closed_lost"]
    rank_score: float
    rank_justification: str
    drafts: List[MessageDraft]
    next_action_date: datetime
    status_tags: List[str]
    outcome: Optional[str]
```

---

## Core Components

### 1. NeedSpec Parser Tool
**Input**: Free text string ("I need X")  
**Output**: Structured NeedSpec object

**Implementation**:
- ADK tool function
- Uses Gemini-2.5-flash with structured output
- Prompt includes examples of persona extraction, keyword identification
- Validates required fields, provides defaults for optional

### 2. Signal Ingestion System
**Two Lanes**:

**Lane A: Browser (LinkedIn via Comet)**
- Scheduled Comet workflows run saved LinkedIn searches
- Exports results to JSON
- Watcher uploads to Cloud Storage → triggers ingestion

**Lane B: API/Web**
- Cloud Run Jobs (scheduled hourly/daily)
- RSS parsers, Google News API, Grants.gov scraper
- All normalize to SignalDump schema

### 3. Contact Ranker Tool
**Ranking Algorithm**:
```
Score = w1*Relevance + w2*Relationship + w3*Recency + w4*Connector + w5*RiskDiscount

Where:
- Relevance: Keyword match + persona fit (0-1)
- Relationship: Direct connection (1.0), mutual (0.7), cold (0.3)
- Recency: Recent signal (1.0), 30 days (0.5), 90+ days (0.1)
- Connector: Can intro you (bonus +0.3)
- RiskDiscount: Unresponsive history (-0.2), competitor (-0.5)
```

### 4. Draft Generator Tool
**Templates**:
- LinkedIn DM (150 chars)
- Email (300 words)
- Warm intro request (to connector)
- Follow-up 1 (5 days later)
- Follow-up 2 (14 days later)

**Grounding**:
- Uses contact history, recent signals, mutual connections
- Gemini-2.5-flash with system prompt enforcing: brevity, specificity, ask clarity

### 5. Pipeline Manager Tool
**CRUD Operations**:
- Create cards from ranked contacts
- Update stage on user action
- Schedule follow-up tasks
- Archive closed cards

**Kanban Stages**: Backlog → Candidates → Drafted → Sent → Follow-up 1 → Follow-up 2 → Warm Intro Requested → Closed

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal**: Working agent with basic tools

- [ ] Initialize project with `uvx agent-starter-pack create`
- [ ] Set up Cloud SQL (PostgreSQL) with schema
- [ ] Implement NeedSpec parser tool
- [ ] Create mock signal dumps for testing
- [ ] Build contact ranker (simple version)
- [ ] Deploy to Cloud Run

**Deliverable**: Agent accepts "I need X", returns ranked contacts from mock data

### Phase 2: Signal Ingestion (Week 3)
**Goal**: Real data flows in

- [ ] Implement SignalDump schema
- [ ] Build Cloud Run Job for RSS ingestion
- [ ] Set up Cloud Storage bucket for dumps
- [ ] Create Comet LinkedIn automation scripts
- [ ] Configure Cloud Scheduler for daily runs

**Deliverable**: Agent queries real LinkedIn + RSS data

### Phase 3: Draft Generation (Week 4)
**Goal**: Personalized outreach

- [ ] Implement draft generator tool
- [ ] Create message templates
- [ ] Add contact history retrieval
- [ ] Build draft preview UI endpoint

**Deliverable**: Agent generates personalized drafts for top contacts

### Phase 4: Pipeline Board (Week 5)
**Goal**: Full workflow management

- [ ] Implement PipelineCard schema
- [ ] Build pipeline manager tool
- [ ] Create kanban board API endpoints
- [ ] Add follow-up scheduler
- [ ] Implement status update webhooks

**Deliverable**: Full pipeline from need → ranked contacts → drafts → scheduled follows

### Phase 5: Polish & Deploy (Week 6)
**Goal**: Production ready

- [ ] Add evaluation suite (Agent Starter Pack)
- [ ] Set up CI/CD (Cloud Build)
- [ ] Configure observability (Cloud Trace)
- [ ] Write documentation
- [ ] Security audit
- [ ] Load testing

**Deliverable**: Production deployment with monitoring

---

## Technology Stack

### Core Framework
- **Agent**: Google ADK (Agent Development Kit)
- **Model**: Gemini-2.5-flash
- **Backend**: FastAPI (via adk App)
- **Deployment**: Cloud Run

### Data & Storage
- **Database**: Cloud SQL (PostgreSQL) - Free tier (1 vCPU, 3.75GB)
- **Object Storage**: Cloud Storage - Free tier (5GB)
- **Vector Store**: (Future) Vertex AI Vector Search

### Ingestion
- **Browser Automation**: Comet (Perplexity)
- **Schedulers**: Cloud Scheduler + local cron
- **RSS**: feedparser (Python)
- **News**: Google News API (free tier)

### Development Tools
- **Package Manager**: uv
- **Linting**: ruff
- **Validation**: pydantic
- **Testing**: pytest
- **CI/CD**: Cloud Build or GitHub Actions

### Observability
- **Tracing**: Cloud Trace
- **Logging**: Cloud Logging
- **Metrics**: Cloud Monitoring
- **Evaluation**: Vertex AI (via Agent Starter Pack)

---

## Deployment Strategy

### Infrastructure as Code
```
terraform/
├── main.tf           # Cloud Run, Cloud SQL, Storage
├── scheduler.tf      # Cloud Scheduler jobs
├── iam.tf           # Service accounts
└── secrets.tf       # API keys, DB passwords
```

### CI/CD Pipeline
```yaml
On push to main:
  1. Run tests (pytest)
  2. Run linting (ruff)
  3. Build Docker image
  4. Push to Artifact Registry
  5. Deploy to Cloud Run (staging)
  6. Run integration tests
  7. Deploy to Cloud Run (production)
```

### Environments
- **Development**: Local with Cloud SQL proxy
- **Staging**: Cloud Run (min instances: 0)
- **Production**: Cloud Run (min instances: 1, max: 10)

### Cost Optimization
- Use free tiers: Cloud SQL (shared core), Cloud Run (2M requests/month)
- Min instances: 0 for staging, 1 for production
- Signal dumps stored in Nearline Storage after 30 days
- Scheduled jobs run outside peak hours

**Estimated Monthly Cost**: $10-30

---

## Security & Compliance

### Authentication & Authorization
- Service accounts with least privilege
- API requires Firebase Auth or Cloud Identity
- Secrets stored in Secret Manager
- Database encrypted at rest

### Privacy & Data Protection
- No LinkedIn scraping (Comet human-in-loop only)
- User data encrypted in transit (TLS)
- PII handling follows GDPR principles
- Contact data retention: 1 year (configurable)
- Audit logs for all data access

### LinkedIn Compliance
- Low-frequency searches (max 5/day)
- Human-paced automation via Comet
- No bulk data exports
- Respects robots.txt
- User-initiated only

---

## Testing Strategy

### Unit Tests
- NeedSpec parser: 10 test cases
- Ranking algorithm: Score validation
- Draft generation: Template rendering
- Pipeline CRUD: State transitions

### Integration Tests
- End-to-end: "I need X" → ranked list
- Signal ingestion: Mock dumps → DB
- API endpoints: HTTP request/response

### Evaluation (ADK)
- Relevance: Are top contacts actually relevant?
- Draft quality: Human evaluation (5-point scale)
- Latency: p50, p95, p99

---

## Next Steps

### Immediate Actions (Today)
1. ✅ Review ChatGPT specifications
2. ✅ Examine Agent Starter Pack documentation
3. ✅ Create implementation plan
4. ⏳ Initialize project with `uvx agent-starter-pack create --template adk_base`
5. ⏳ Set up GitHub repository structure
6. ⏳ Create database schema SQL

### This Week
- Implement NeedSpec parser tool
- Build mock signal dumps
- Deploy Phase 1 to Cloud Run
- Test end-to-end with sample queries

### Future Enhancements
- Web UI (React/Next.js)
- Email integration (Gmail API)
- CRM sync (Salesforce, HubSpot)
- Mobile app
- Multi-user support
- Advanced analytics dashboard

---

## References

- **Agent Starter Pack**: https://github.com/GoogleCloudPlatform/agent-starter-pack
- **ADK Documentation**: https://google.github.io/adk-docs/
- **ChatGPT Specification**: [See conversation: Agent starter pack use cases]
- **Comet Browser**: https://www.perplexity.ai/comet/
- **GCP Free Tier**: https://cloud.google.com/free

---

**Document Version**: 1.0  
**Last Updated**: December 19, 2025  
**Author**: Network Bounty Hunter Agent Team  
**Status**: Ready for Implementation
