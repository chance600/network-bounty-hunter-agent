# Network Bounty Hunter Agent 🎯

**AI-powered network monitoring and outreach agent** that turns "I need X" into ranked contacts, tailored outreach drafts, follow-up schedules, and a pipeline board.

Built with [Google Cloud Platform Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) (adk_base).

## ✨ What It Does

Simply tell the agent what you need:

> "I need a packaging engineer with bioplastics experience in NYC"

The agent will:
1. **Parse** your need into structured criteria
2. **Rank** contacts from your network based on relevance, relationship strength, and recency
3. **Generate** personalized LinkedIn DMs and email drafts
4. **Recommend** next actions with a pipeline summary

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Cloud account with Vertex AI enabled
- `gcloud` CLI authenticated

### Installation

```bash
# Clone the repository
git clone https://github.com/chance600/network-bounty-hunter-agent.git
cd network-bounty-hunter-agent

# Install dependencies
pip install -r requirements.txt

# Or use uv (recommended)
uv pip install -r requirements.txt
```

### Run the Agent

```bash
# Set up GCP authentication
gcloud auth application-default login

# Run the agent
cd app
python -m google.adk.cli chat agent:app
```

### Example Interaction

```
You: I need a packaging engineer with bioplastics experience in NYC

Agent: I'll help you find the right packaging engineer with bioplastics expertise in NYC.

[Parsing need...]
[Ranking contacts...]

Found 3 strong candidates:

1. **Michael Rodriguez** - Materials Engineer at EcoMaterials Inc
   Score: 0.68 | Relevance: 0.90 (keyword matches), Relationship: 0.40, Recency: 0.80, Geographic match
   Next action: Draft personalized outreach

2. **Sarah Chen** - VP of Packaging Innovation at GreenPack Solutions
   Score: 0.62 | Relevance: 0.90 (keyword matches), Relationship: 0.70, Recency: 0.80
   Next action: Draft personalized outreach

3. **Dr. Amy Wong** - Director of Sustainable Packaging at BioCycle Corp
   Score: 0.60 | Relevance: 0.60 (keyword matches), Relationship: 0.80, Recency: 1.00
   Next action: Draft personalized outreach

Recommendations:
- Start with top 3 contacts for highest ROI
- Draft personalized messages (avoid templates)
- Schedule follow-up for non-responders in 5-7 days
```

## 📂 Project Structure

```
network-bounty-hunter-agent/
├── app/
│   ├── agent.py       # Main agent with ADK tools
│   └── models.py      # Pydantic data models
├── docs/
│   └── IMPLEMENTATION_PLAN.md  # Detailed architecture
├── README.md
├── requirements.txt
└── LICENSE
```

## 🛠️ Core Features

### 1. **NeedSpec Parser**
Extracts structured criteria from free text:
- Objective type (intro/hire/partner/raise)
- Target persona keywords
- Geography preferences
- Time urgency

### 2. **Contact Ranker**
Scores contacts using:
- **Relevance** (40%): Keyword matches in tags/title
- **Relationship** (30%): Connection strength
- **Recency** (20%): Last interaction date
- **Geography** (10%): Location match

### 3. **Draft Generator**
Creates personalized outreach:
- LinkedIn DM (150 char limit)
- Email with custom subject/body
- Grounded in contact's role, company, tags

### 4. **Pipeline Summary**
Provides actionable next steps:
- Ranked contact list with justifications
- Recommended outreach order
- Follow-up scheduling guidance

## 🔧 Configuration

### Mock Data (Current MVP)
The agent uses mock contacts in `agent.py`. To add your real contacts:

```python
MOCK_CONTACTS = [
    Contact(
        id="unique-id",
        name="Your Contact",
        title="Their Title",
        company="Their Company",
        location="City, State",
        relationship_strength=0.7,  # 0-1
        tags=["keyword1", "keyword2"],
        source="linkedin_comet"
    ),
]
```

### Future: Database Integration
See [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) for:
- PostgreSQL schema
- Signal ingestion (LinkedIn via Comet, RSS, news)
- Real-time pipeline board

## 📊 Roadmap

- [x] Core agent with ADK tools
- [x] Data models (Pydantic)
- [x] Mock contacts for testing
- [x] NeedSpec parser
- [x] Contact ranking algorithm
- [x] Draft generation
- [x] Pipeline summary
- [ ] PostgreSQL database
- [ ] Signal ingestion (LinkedIn via Comet)
- [ ] Web UI (React/Next.js)
- [ ] Real-time pipeline board
- [ ] Follow-up scheduling
- [ ] Email integration
- [ ] Deployment to Cloud Run

## 📖 Documentation

- **[Implementation Plan](docs/IMPLEMENTATION_PLAN.md)**: Complete architecture, data models, deployment strategy
- **[Agent Starter Pack Docs](https://googlecloudplatform.github.io/agent-starter-pack/)**: ADK framework documentation

## 🤝 Contributing

Contributions welcome! See the [implementation plan](docs/IMPLEMENTATION_PLAN.md) for areas to contribute.

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Built With

- [Google Agent Development Kit (ADK)](https://github.com/google/adk-python)
- [Gemini 2.5 Flash](https://ai.google.dev/)
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- [Pydantic](https://docs.pydantic.dev/)

---

**Status**: ✅ MVP Complete - Ready for Testing

Need help? Check the [implementation plan](docs/IMPLEMENTATION_PLAN.md) or open an issue!
