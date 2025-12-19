# Network Bounty Hunter Agent 🎯

**AI-powered LinkedIn connector matchmaking system** that monitors LinkedIn posts for "I need X" requests and intelligently matches them with relevant contacts from your network.

Built with [Google Cloud Platform Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) (adk_base).

## ✨ What It Does

This agent transforms your LinkedIn network into a powerful matchmaking engine:

**Tell the agent about a LinkedIn post:**
> "I saw a post: Need sustainable packaging supplier for food products"

**The agent will:**
1. **Extract** the need from the post (e.g., sustainable packaging expertise, food industry experience)
2. **Match** contacts from your network based on skills, industry, and relevance
3. **Generate** personalized introduction messages tailored to the opportunity
4. **Summarize** the opportunity with actionable next steps

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

# Configure Google Cloud (if not already done)
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="global"
export GOOGLE_GENAI_USE_VERTEXAI="True"
```

### Usage

```bash
# Start the agent in chat mode
cd app
python -m google.adk.cli chat agent:app
```

**Example conversation:**
```
You: I saw this LinkedIn post: "Looking for a React developer with 5+ years experience for fintech startup in SF"

Agent: I've analyzed the post and found 3 strong matches from your network:

1. Sarah Chen (Relevance: 9.5/10)
   - Senior React Developer at Stripe
   - 7 years experience
   - Based in San Francisco
   - Skills match: React, TypeScript, Fintech

2. Michael Rodriguez (Relevance: 8.7/10)
   ...

Would you like me to generate an introduction message for Sarah?

You: Yes, generate intro for Sarah

Agent: Here's a personalized introduction:

"Hi [Post Author],

I noticed your search for a React developer with fintech experience. I'd like to introduce you to Sarah Chen, a Senior React Developer at Stripe with over 7 years of experience building production-grade fintech applications..."
```

## 🛠️ Architecture

### Core Components

- **`app/agent.py`** - Main agent with 4 connector tools:
  - `extract_need_from_post` - Parses LinkedIn posts to identify needs
  - `find_matching_contacts` - Ranks contacts by relevance
  - `generate_intro_message` - Creates personalized introductions
  - `create_opportunity_summary` - Provides actionable summaries

- **`app/models.py`** - Data models:
  - `Contact` - Network contact with skills, industry, location
  - `Need` - Extracted requirements from posts
  - `OpportunitySummary` - Matchmaking results and recommendations

### Contact Database

The agent uses a mock contact database in `app/agent.py`. Replace `MY_CONTACTS` with your actual network data:

```python
MY_CONTACTS = [
    Contact(
        id="c1",
        name="Your Contact Name",
        title="Their Job Title",
        company="Their Company",
        industry="Their Industry",
        location="City, State",
        skills=["Skill 1", "Skill 2", "Skill 3"],
        relationship_strength=9,  # 1-10 scale
        linkedin_url="https://linkedin.com/in/username"
    ),
    # Add more contacts...
]
```

## 📋 Use Cases

### 1. Talent Matchmaking
**Post:** "Hiring: ML Engineer with NLP experience for healthcare startup"
**Agent:** Matches contacts with ML/NLP skills in healthcare industry

### 2. Business Development
**Post:** "Looking for sustainable packaging suppliers for CPG brand"
**Agent:** Finds contacts in packaging/manufacturing with sustainability focus

### 3. Partnership Opportunities
**Post:** "Seeking co-founder with ops experience for SaaS startup"
**Agent:** Identifies contacts with operations background and startup experience

### 4. Consulting/Advisory
**Post:** "Need expert in FDA regulatory compliance for medical devices"
**Agent:** Matches regulatory affairs professionals in medical device sector

## 🔧 Customization

### Adjust Matching Algorithm

Edit scoring logic in `find_matching_contacts()` tool:

```python
# Adjust weights for different factors
skill_match_weight = 0.4  # 40% weight on skills
industry_match_weight = 0.3  # 30% weight on industry
relationship_weight = 0.2  # 20% weight on relationship strength
location_weight = 0.1  # 10% weight on location proximity
```

### Custom Introduction Templates

Modify message generation in `generate_intro_message()` tool to match your style.

## 🧪 Testing

```bash
# Test with sample scenarios
python -m google.adk.cli chat agent:app

# Sample test inputs:
> "Post says: Need React dev in NYC"
> "Show me matches for: sustainable packaging supplier"
> "Generate intro for contact ID c1"
```

## 📚 Documentation

See `docs/IMPLEMENTATION_PLAN.md` for detailed implementation notes and architecture decisions.

## 🔐 Privacy & Security

- Contact data stays local (no scraping)
- No automated LinkedIn posting
- You maintain full control over introductions
- All API calls use authenticated Google Cloud services

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 🙏 Acknowledgments

Built with [Google Cloud Platform Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)

---

**Ready to turn your network into a matchmaking engine?** Star this repo and start connecting! ⭐
