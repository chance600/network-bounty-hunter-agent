# Where You'll Get Notified - Output & Notification Guide

## 📍 Current Output Locations

### 1. Terminal Output (Immediate)

**When you run the agent manually:**

```bash
cd network-bounty-hunter-agent
python -m app.agent
```

**You'll see results directly in your terminal:**

```
🔍 Processing LinkedIn post...
📋 Found bounty: "Designer with portfolio"

💼 Loading contacts from data/contacts.json...
✅ Found 6 contacts

🔎 Matching "designer" skills...

🏆 Top 3 Matches:

1. ⭐ Emily Park (Score: 0.95)
   - Role: Brand Designer & Illustrator
   - Company: Freelance
   - Why good match: Specializes in podcast cover art and brand identity for creators
   - Relationship: Client turned friend (last contact: Jan 5, 2025)
   - Availability: Actively seeking projects ✅
   
2. ⭐ Jane Smith (Score: 0.78)
   - Role: Senior Frontend Engineer  
   - Company: TechCorp Inc.
   - Why good match: React + Product Design + UX/UI expertise
   - Relationship: Close colleague (last contact: Jan 10, 2025)
   - Availability: Open to side projects
   
3. ⭐ Sarah Johnson (Score: 0.65)
   - Role: VP of Marketing
   - Company: Growth Partners
   - Why good match: Brand development and content marketing
   - Relationship: Professional acquaintance (last contact: Nov 15, 2024)
   - Availability: Limited availability

📝 Would you like introduction templates? (y/n):
```

### 2. Saved JSON Reports (Reviewable Later)

**Location**: `output/matches_YYYYMMDD_HHMMSS.json`

Every time you process a post, the agent automatically saves a detailed JSON report:

```json
{
  "timestamp": "2025-12-20T19:00:00",
  "linkedin_post": {
    "author": "Josh Jung",
    "role": "Chief of Staff @ Corgi",
    "post_text": "We're looking for our first designer at Corgi",
    "posted_date": "2 days ago",
    "bounty": {
      "what_they_need": "Designer",
      "skills_required": ["portfolio", "personal website", "design"],
      "urgency": "medium",
      "context": "First design hire for startup"
    }
  },
  "matches": [
    {
      "contact_name": "Emily Park",
      "email": "emily.park@example.com",
      "linkedin_url": "https://linkedin.com/in/emilypark",
      "relevance_score": 0.95,
      "why_good_match": "Specializes in podcast cover art and brand identity. Active freelancer seeking projects.",
      "relationship_strength": "client turned friend",
      "last_interaction": "2025-01-05",
      "intro_template": "Hi Emily! I saw a great opportunity..."
    }
  ]
}
```

**Check your results:**
```bash
ls -la output/  # Shows all your match reports

cat output/matches_20251220_190000.json | jq  # View formatted JSON
```

### 3. Perplexity Results (Your Inbox)

**Location**: Your Perplexity Library  
**URL**: https://www.perplexity.ai/library

When you run a Perplexity search, it automatically saves to your library:
- Search title: "Find recent LinkedIn posts where people say..."
- Results: 5-15 LinkedIn posts with author, role, and needs
- Saved for: ~30 days (Perplexity keeps history)

**How to review:**
1. Go to Perplexity Library
2. Find your LinkedIn search
3. See all the posts you found
4. Copy any new ones to process through the agent

## 🔔 Notification Options (Future Enhancements)

### Option A: Email Notifications (Coming Soon)

**Setup:**
```bash
# Add to .env file
EMAIL_NOTIFICATIONS=true
EMAIL_TO=your.email@example.com
EMAIL_FROM=agent@yourproject.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your-app-password
```

**You'll receive:**
- Subject: "🎯 New LinkedIn Match: Designer role at Corgi"
- Body: Top 3 matches with scores and intro templates
- Frequency: Immediately after processing each post

### Option B: Slack Notifications (Coming Soon)

**Setup:**
```bash
# Add to .env file
SLACK_WEBHOOK_URL=https://hooks.slack.com / services / YOUR / WEBHOOK / URL
SLACK_CHANNEL=#network-matches
```

**You'll receive:**
🔔 **New LinkedIn Match**
📬 "Designer role at Corgi" - Body: Top 3 matches with scores and intro templates
⏰ Frequency: Immediately after processing each post

## 📊 Quick Check (2 minutes)

**See latest matches:**
```bash
cd network-bounty-hunter-agent
ls -t output/ | head -5  # View latest 5 files
cat output/$(ls -t output/ | head -1)  # View most recent match
```

**Summary for all recent finds:**
```bash
jq '[.matches[] | {name: .contact_name, score: .relevance_score}]' output/*.json
```

## 🎯 Monthly Analytics (Optional)

**How many matches did you find this month:**
```bash
find output/ -name "matches_*.json" -mtime -30 | wc -l
```

**Top contacts this month:**
```bash
jq -s '[.[].matches[] | {name: .contact_name, score: .relevance_score}] | sort_by(.score) | reverse | .[0:10]' output/*.json
```
