# Quick Start Guide - Network Bounty Hunter Agent

## 🚀 5-Minute Setup

### Step 1: Clone & Install

```bash
# Clone the repository
git clone https://github.com/chance600/network-bounty-hunter-agent.git
cd network-bounty-hunter-agent

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Add Your Contacts

Edit `data/contacts.json` with your network:

```json
{
  "contacts": [
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "linkedin_url": "https://linkedin.com/in/janesmith",
      "current_role": "Senior Product Designer",
      "current_company": "Figma",
      "skills": ["UI/UX", "product design", "prototyping"],
      "industries": ["SaaS", "design tools"],
      "relationship_strength": "close colleague",
      "last_interaction": "2025-12-15",
      "availability": "open to projects",
      "location": "San Francisco"
    }
  ]
}
```

**Pro tip:** Start with 10-20 of your strongest contacts who are:
- Open to new opportunities
- Have specialized/valuable skills
- You've interacted with recently
- Would appreciate good intros

### Step 3: You're Ready! No API keys needed.

The agent runs locally with no external API requirements.

---

## 📋 Daily Workflow (10 minutes/day)

### Morning Routine

**1. Find LinkedIn Posts with Perplexity (5 min)**

Open Perplexity.ai and search:
```
Find recent LinkedIn posts where people say "I need" or "looking for" help with:
- designer
- engineer  
- developer
- consultant
- freelancer
```

**Copy 3-5 interesting posts that look like paid opportunities.**

Example post:
```
"We're looking for our first designer at Corgi. 
Must have portfolio and personal website. 
DM me if interested!"
- Josh Jung, Chief of Staff @ Corgi
- Posted 2 days ago
```

**2. Process Posts Through Agent (3 min)**

```bash
cd network-bounty-hunter-agent
python -m app.agent
```

Paste the LinkedIn post when prompted.

The agent will:
- ✅ Extract what they need ("designer with portfolio")
- ✅ Match your contacts (finds top 3)
- ✅ Show relevance scores (0-1.0)
- ✅ Explain why each is a good match
- ✅ Draft introduction templates
- ✅ Save detailed report to `output/matches_[timestamp].json`

**3. Review & Act (2 min)**

Look at the top match. If score > 0.70:
- ✅ Good fit! Proceed to outreach
- ❌ Low score? Process next post

---

## 💬 Making Money: The Outreach Process

### Template A: Message to Person with Need

```
Hi [Name],

Saw your post about needing a [X]. I specialize in connecting 
professionals and have someone perfect in my network.

[Contact Name] is a [Role] with [Key Experience]. They've done 
[Relevant Achievement].

Happy to make a warm intro. If it works out and you work together, 
standard 10% referral fee on the first project. Sound good?

Best,
[Your Name]
```

### Template B: Message to Your Contact

```
Hey [Contact],

Quick opportunity: [Person] at [Company] is looking for a [Role].

They need:
- [Skill 1]
- [Skill 2]  
- [Skill 3]

Project scope: [Estimated size, e.g., "3-month contract, ~$10K"]

Interested? I can make the intro. Would appreciate standard 10% 
referral fee if it leads to a contract.

LMK!
[Your Name]
```

### Template C: Simple Referral Agreement

Send this after both parties say yes:

```
Referral Agreement - [Date]

Parties:
- Connector: [Your Name]
- Client: [Person with need]
- Provider: [Your contact]

Terms:
- [Your Name] introduced [Provider] to [Client]
- If they work together, [Client] or [Provider] pays [Your Name] 
  a 10% referral fee on the first project/contract value
- Payment due within 30 days of contract signing
- Fee applies to first engagement only

Agreed:
[Client] ___________  Date: _____
[Provider] _________  Date: _____
[Your Name] ________  Date: _____
```

---

## 📊 Tracking Your Pipeline

### Create Simple Spreadsheet

| Date | Need | Person | Contact Matched | Est. Value | Fee % | Status | Actual Fee |
|------|------|--------|----------------|-----------|-------|--------|------------|
| 12/20 | Designer | Josh @Corgi | Emily Park | $8K | 10% | Intro made | - |
| 12/21 | Engineer | Sarah @Startup | David Chen | $15K | 10% | Meeting set | - |
| 12/18 | Consultant | Mike @Agency | Lisa Wang | $5K | 10% | Contract signed | $500 ✅ |

**Status stages:**
1. Discovered
2. Outreach sent
3. Intro made
4. Meeting scheduled  
5. Contract discussed
6. Deal closed
7. Invoice sent
8. PAID 💰

---

## 🎯 Success Tips

### Make Quality Matches
- **Only intro if score > 0.70** - High relevance = better outcomes
- **Check availability** - Contact must be open to work
- **Consider relationship strength** - Stronger relationships = easier asks
- **Recent contact wins** - People you've talked to in last 60 days respond better

### Set Expectations
- **Be transparent** - Always disclose you earn a referral fee
- **Offer value** - You're saving them time finding qualified people
- **Follow up weekly** - Gentle reminders keep deals moving
- **Be patient** - Some connections take 2-4 weeks to close

### Scale Smart
- **Start with 3 posts/day** - Don't overwhelm yourself
- **Focus on $5K+ opportunities** - Worth your time
- **Build templates** - Reuse successful messages
- **Track everything** - Learn what works

---

## 📅 Weekly Schedule

### Monday (Setup)
- Review your contacts.json
- Check Perplexity Library for saved searches
- Plan week's outreach targets

### Tuesday-Thursday (Hunt & Process)
- 10 min/day: Find 3-5 LinkedIn posts via Perplexity
- 5 min/day: Process through agent
- 10 min/day: Send outreach messages

### Friday (Follow-ups)
- Check spreadsheet for intros needing follow-up
- Send gentle reminders
- Make new warm intros for positive responses

### Weekend (Admin)
- Update pipeline statuses
- Calculate potential earnings (feel good!)
- Invoice any closed deals
- Review output/ folder for insights

---

## 🔍 LinkedIn Search Strategies (via Perplexity)

### Best Search Queries

**Generic:**
```
LinkedIn posts: "I need" OR "looking for" OR "hiring"
```

**By Role:**
```
LinkedIn posts: "need designer" OR "looking for developer" 
```

**By Industry:**
```
LinkedIn posts: "startup hiring" OR "early stage looking for"
```

**By Urgency:**
```
LinkedIn posts: "urgent need" OR "ASAP" OR "immediately"
```

**By Company Stage:**
```
LinkedIn posts: "series A" OR "just raised" + "hiring"
```

### Perplexity Pro Tips
- Add date filter: "past week" for fresh opportunities
- Use collections to organize by niche
- Save successful search queries
- Results stay in Library ~30 days

---

## 💡 Example Session

**Monday 9am - 15 minutes**

1. Open Perplexity, search: "LinkedIn posts need designer OR developer"
2. Find post: "Looking for React developer for 3-month project" - Sarah @ TechStartup
3. Run agent: `python -m app.agent`
4. Paste post
5. Agent returns: David Chen (score 0.88) - Perfect match!
6. Message Sarah: "Hi Sarah, saw your React post. I have David Chen..."
7. Message David: "Hey David, quick opportunity at TechStartup..."
8. Update spreadsheet: "Sarah - David - $12K - 10% - Outreach sent"
9. Done! Potential $1,200 earned in 15 minutes of work.

**Repeat 3x per day = 3 potential deals/day = ~$3K-5K/week potential.**

---

## 📁 Output Files

### Where Your Results Live

**`output/matches_YYYYMMDD_HHMMSS.json`**

Every processed post creates a detailed report:
```json
{
  "timestamp": "2025-12-20T21:00:00",
  "linkedin_post": {
    "author": "Sarah Johnson",
    "need": "React developer",
    "urgency": "high"
  },
  "matches": [
    {
      "contact_name": "David Chen",
      "relevance_score": 0.88,
      "why_good_match": "5 years React + startup experience",
      "intro_template": "Hi Sarah! Meet David..."
    }
  ]
}
```

**View all reports:**
```bash
ls -lt output/  # List by most recent
cat output/matches_20251220_210000.json | jq  # Pretty print
```

---

## 🚨 Troubleshooting

### "No matches found"
- ✅ Check contacts.json has relevant skills for this need
- ✅ Try lowering score threshold (0.50 instead of 0.70)
- ✅ Add more contacts to your network

### "Low scores (< 0.50)"
- ✅ Post might be too niche
- ✅ Your network lacks that specialty
- ✅ Skip and process next post

### "Agent crashes"
- ✅ Check requirements.txt installed: `pip install -r requirements.txt`
- ✅ Verify contacts.json is valid JSON
- ✅ Run from repo root: `cd network-bounty-hunter-agent`

---

## 📚 Next Steps

### After Your First Week
1. **Read BOUNTY_MONETIZATION_STRATEGY.md** - Scale to $10K+/month
2. **Review OUTPUT_AND_NOTIFICATIONS.md** - Set up alerts
3. **Check PERPLEXITY_WORKFLOW.md** - Advanced search strategies

### After Your First $1,000
1. Build Phase 2 tools (deal qualifier, bounty calculator)
2. Hire VA for outreach
3. Create referral partner network
4. Consider white-label service

---

## ✅ Daily Checklist

**Morning (10 min):**
- [ ] Perplexity search for 3-5 LinkedIn posts
- [ ] Process through agent
- [ ] Send outreach to top 2 opportunities

**Midday (5 min):**
- [ ] Check responses
- [ ] Make intros if both sides said yes

**End of day (5 min):**
- [ ] Update pipeline spreadsheet
- [ ] Set follow-up reminders
- [ ] Review output/ folder

**Weekly (15 min):**
- [ ] Follow up on pending intros
- [ ] Invoice closed deals
- [ ] Add new contacts to contacts.json
- [ ] Calculate earnings 💰

---

## 🎯 Your Goal: First $500 in 30 Days

**The Math:**
- Find 3 posts/day × 20 working days = 60 opportunities
- 30% get positive response = 18 interested parties
- 20% convert to intros = ~4 successful connections
- Avg contract $6K × 10% fee = $600 per connection
- **Total: $2,400 potential in first month**

**But realistically:**
- 2-3 connections close in month 1 = **$1,200-$1,800**
- Rest close in month 2-3 (longer sales cycles)

**You're not selling. You're making valuable intros. The money follows quality matches.**

---

**Ready to start?** Run `python -m app.agent` and paste your first LinkedIn post! 🚀💰
