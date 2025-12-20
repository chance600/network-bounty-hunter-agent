# Network Bounty Hunter Agent - Usage Guide

## 🎯 What This System Does

The Network Bounty Hunter Agent is an AI-powered LinkedIn connector matchmaking system that:

1. **Monitors LinkedIn posts** - Automatically searches for posts containing "I need X" requests
2. **Extracts requirements** - Identifies what the person is looking for (the "bounty")
3. **Matches contacts** - Finds relevant people from your network who can help
4. **Ranks matches** - Scores connections based on relevance and relationship strength
5. **Facilitates intros** - Provides all the info you need to make warm introductions

## 🔧 Setup Instructions

### 1. Prerequisites

- Python 3.11+
- Google Cloud Platform account (free tier works)
- Perplexity API key (for LinkedIn search)
- Git

### 2. Clone the Repository

```bash
git clone https://github.com/chance600/network-bounty-hunter-agent.git
cd network-bounty-hunter-agent
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

Create a `.env` file in the project root:

```bash
# Google Cloud Platform
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=True

# Perplexity API for LinkedIn search
PERPLEXITY_API_KEY=your-perplexity-api-key
```

**How to get API keys:**

- **GCP**: 
  1. Go to https://console.cloud.google.com
  2. Create a new project or select existing
  3. Enable Vertex AI API
  4. Set up authentication (Application Default Credentials)

- **Perplexity**:
  1. Go to https://www.perplexity.ai
  2. Sign up for API access
  3. Get your API key from the dashboard

### 5. Configure GitHub Secrets (for automation)

For the automated LinkedIn monitoring workflow, add these secrets to your GitHub repository:

1. Go to repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `GOOGLE_CLOUD_PROJECT`
   - `GOOGLE_CLOUD_LOCATION`
   - `GOOGLE_GENAI_USE_VERTEXAI`
   - `PERPLEXITY_API_KEY`

## 📋 How to Use

### Option 1: Manual Mode (Interactive)

Run the agent locally with a specific LinkedIn post:

```bash
python -m app.agent
```

Then provide a LinkedIn post URL or paste the post content when prompted.

### Option 2: Automated Mode (Scheduled)

The system runs automatically via GitHub Actions:

- **Schedule**: Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- **What it does**: 
  1. Searches LinkedIn for recent "I need X" posts using Perplexity
  2. Processes each post through the agent
  3. Saves matches to `output/matches_TIMESTAMP.json`
  4. (Future) Sends notification with top matches

**To run manually:**

1. Go to Actions tab in GitHub
2. Select "LinkedIn Network Monitor"
3. Click "Run workflow"

### Option 3: Command Line (One-off)

Run the LinkedIn monitor script directly:

```bash
python automation/linkedin_monitor.py
```

This will:
- Search for recent LinkedIn posts
- Process them through the agent
- Save results to `output/` folder

## 🔍 Understanding the Output

The system generates JSON files with match data:

```json
{
  "post": {
    "author_name": "John Doe",
    "author_profile_url": "https://linkedin.com/in/johndoe",
    "post_text": "I need help finding a React developer for my startup...",
    "post_url": "https://linkedin.com/posts/...",
    "posted_date": "2025-01-15T10:30:00"
  },
  "bounty": {
    "what_they_need": "React developer",
    "context": "startup project",
    "urgency": "medium"
  },
  "matches": [
    {
      "contact_name": "Jane Smith",
      "relevance_score": 0.95,
      "why_good_match": "Senior React developer with startup experience",
      "relationship_strength": "close colleague",
      "introduction_template": "Hi Jane, I saw John is looking for..."
    }
  ]
}
```

## 📊 Agent Tools (What It Can Do)

The agent has 4 core tools:

### 1. `extract_bounty`
- Analyzes LinkedIn post text
- Identifies what the person needs
- Extracts context and urgency

### 2. `load_contacts`
- Loads your contact database
- Supports JSON format (future: CSV, vCard)
- Keeps all data local (no external uploads)

### 3. `match_contacts`
- Semantic search to find relevant people
- Uses AI to understand skill/need matching
- Returns ranked list of potential introductions

### 4. `rank_matches`
- Scores each match on:
  - Relevance (how well they fit the need)
  - Relationship strength (how well you know them)
  - Availability signals
- Provides introduction templates

## 💾 Managing Your Contact Data

### Format

Store contacts in `data/contacts.json`:

```json
[
  {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "linkedin_url": "https://linkedin.com/in/janesmith",
    "skills": ["React", "TypeScript", "Node.js"],
    "industry": "Tech",
    "relationship": "close colleague",
    "notes": "Former teammate, loves helping startups"
  }
]
```

### Privacy & Security

- **Local only**: All contact data stays on your machine
- **No scraping**: We don't scrape LinkedIn (manual entry only)
- **No sharing**: Contacts never leave your environment
- **Git-ignored**: `data/` folder is in `.gitignore`

## 🔄 Workflow Examples

### Example 1: Helping a Connection

1. See LinkedIn post: "I need a graphic designer for my podcast"
2. Agent extracts: Need = "graphic designer", Context = "podcast"
3. Agent matches: Finds 3 designers in your network
4. Agent ranks: Designer A (close friend, podcast experience) = 0.95
5. You make intro: "Hey Designer A, I saw this post..."

### Example 2: Automated Monitoring

1. GitHub Action runs every 6 hours
2. Perplexity searches: "I need" posts from last 6 hours
3. Agent processes: 5 posts found, 12 matches identified
4. Results saved: `output/matches_20250115_120000.json`
5. You review: Check file, make intros for top matches

## 🎨 Customization

### Search Queries

Edit `automation/linkedin_monitor.py` to change search terms:

```python
search_queries = [
    '"I need" OR "looking for" site:linkedin.com/posts',
    '"seeking recommendations" site:linkedin.com/posts',
    # Add your custom queries here
]
```

### Matching Logic

Edit `app/agent.py` tool definitions to adjust:
- Match scoring algorithm
- Relevance thresholds
- Introduction templates

### Schedule

Edit `.github/workflows/linkedin_monitor.yml` cron schedule:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # Change to: '0 9,17 * * 1-5' for 9am/5pm Mon-Fri only
```

## 🐛 Troubleshooting

### "PERPLEXITY_API_KEY not found"
- Check `.env` file exists in project root
- Verify API key is set correctly
- For GitHub Actions, check repository secrets

### "No posts found"
- Perplexity may not have indexed recent posts yet
- Try broader search queries
- Check API rate limits

### "No matches found"
- Ensure `data/contacts.json` exists and has data
- Check contact skills/industries match the need
- Review bounty extraction (may have misunderstood the post)

### Import Errors
- Run `pip install -r requirements.txt` again
- Check Python version (need 3.11+)
- Verify virtual environment is activated

## 📈 Future Enhancements

- [ ] Email/Slack notifications for new matches
- [ ] Web dashboard for reviewing matches
- [ ] CRM integration (HubSpot, Salesforce)
- [ ] LinkedIn authentication for direct posting
- [ ] Match confidence explanations
- [ ] Batch introduction drafting

## 🤝 Contributing

This is an open-source project! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 💬 Support

Questions? Issues? Ideas?
- Open an issue on GitHub
- Check the Implementation Plan in `docs/IMPLEMENTATION_PLAN.md`
- Review the agent code in `app/agent.py`

---

**Built with ❤️ using Google Cloud Platform Agent Starter Pack**
