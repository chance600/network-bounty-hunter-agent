"""Network Bounty Hunter Agent - Connector Matchmaking System.

Monitors LinkedIn posts for needs, matches them with your contacts, facilitates intros.
"""
import os
import json
import uuid
from datetime import datetime
from typing import List
import google.auth

from google.adk.agents import Agent
from google.adk.apps.app import App

from models import Contact

# Configure GCP
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# ============================================================================
# MOCK DATA - YOUR CONTACT DATABASE
# ============================================================================

MY_CONTACTS = [
    Contact(
        id="c1",
        name="Sarah Chen",
        title="VP of Packaging Innovation",
        company="GreenPack Solutions",
        location="San Francisco, CA",
        relationship_strength=0.9,
        tags=["packaging", "bioplastics", "sustainability", "compostable", "materials-science"],
        notes="Expert in bioplastics. Loves connecting with innovators. Open to consulting."
    ),
    Contact(
        id="c2",
        name="Michael Rodriguez",  
        title="Lead Materials Engineer",
        company="EcoMaterials Inc",
        location="New York, NY",
        relationship_strength=0.7,
        tags=["materials", "bioplastics", "R&D", "polymer-engineering", "testing"],
        notes="Technical expert, hands-on with polymer testing. Always willing to help."
    ),
    Contact(
        id="c3",
        name="Dr. Amy Wong",
        title="Director of Sustainable Packaging",
        company="BioCycle Corp",
        location="Boston, MA",
        relationship_strength=0.8,
        tags=["packaging", "compostable", "certification", "regulatory", "supply-chain"],
        notes="Deep regulatory knowledge. Can help navigate certifications."
    ),
    Contact(
        id="c4",
        name="James Park",
        title="Founder & CEO",
        company="PackTech Ventures",
        location="Austin, TX",
        relationship_strength=0.6,
        tags=["packaging", "investment", "startups", "innovation", "scaling"],
        notes="Investor in packaging tech. Mentors early-stage founders."
    ),
    Contact(
        id="c5",
        name="Lisa Thompson",
        title="Head of Product Development",
        company="Natural Foods Co",
        location="Seattle, WA",
        relationship_strength=0.8,
        tags=["food-packaging", "consumer-products", "sourcing", "partnerships"],
        notes="Always looking for sustainable packaging solutions for food products."
    ),
]

# ============================================================================
# AGENT TOOLS
# ============================================================================

def extract_need_from_post(post_text: str, author_name: str = "someone") -> str:
    """
    Extract what someone needs from their LinkedIn post.
    
    Args:
        post_text: The full text of the LinkedIn post
        author_name: Name of the person who posted
        
    Returns:
        JSON with extracted need: {"author", "need_type", "keywords", "context"}
    """
    post_lower = post_text.lower()
    
    # Detect need patterns
    keywords = []
    need_type = "unknown"
    
    # Common patterns
    if "looking for" in post_lower or "need" in post_lower or "seeking" in post_lower:
        if "packaging" in post_lower:
            keywords.append("packaging")
        if "bioplastic" in post_lower or "bio-plastic" in post_lower:
            keywords.append("bioplastics")
        if "sustainable" in post_lower or "sustainability" in post_lower:
            keywords.append("sustainability")
        if "material" in post_lower:
            keywords.append("materials")
        if "engineer" in post_lower:
            keywords.append("engineer")
        if "supplier" in post_lower or "vendor" in post_lower:
            keywords.append("supplier")
        if "investor" in post_lower or "funding" in post_lower:
            keywords.append("investment")
        if "partner" in post_lower:
            keywords.append("partnerships")
        if "advice" in post_lower or "help" in post_lower:
            keywords.append("advice")
        if "certification" in post_lower or "certified" in post_lower:
            keywords.append("certification")
        if "food" in post_lower:
            keywords.append("food-packaging")
            
        # Determine need type
        if "hire" in post_lower or "hiring" in post_lower:
            need_type = "hire"
        elif "invest" in post_lower or "funding" in post_lower:
            need_type = "investment"
        elif "partner" in post_lower:
            need_type = "partnership"
        elif "supplier" in post_lower or "vendor" in post_lower:
            need_type = "supplier"
        else:
            need_type = "advice/intro"
    
    result = {
        "author": author_name,
        "need_type": need_type,
        "keywords": keywords,
        "context": post_text[:200]  # First 200 chars for context
    }
    
    return json.dumps(result)


def find_matching_contacts(need_json: str, top_n: int = 3) -> str:
    """
    Find contacts from YOUR network who could help with the posted need.
    
    Args:
        need_json: JSON from extract_need_from_post
        top_n: Number of top matches to return
        
    Returns:
        JSON with matched contacts and match scores
    """
    need = json.loads(need_json)
    keywords = need.get("keywords", [])
    
    if not keywords:
        return json.dumps({"matches": [], "message": "No clear need detected in post"})
    
    matches = []
    
    for contact in MY_CONTACTS:
        # Calculate match score
        relevance = 0
        matching_tags = []
        
        for keyword in keywords:
            for tag in contact.tags:
                if keyword.lower() in tag.lower() or tag.lower() in keyword.lower():
                    relevance += 0.25
                    matching_tags.append(tag)
        
        relevance = min(relevance, 1.0)
        
        # Boost by relationship strength (you know them well = better intro)
        final_score = (0.7 * relevance) + (0.3 * contact.relationship_strength)
        
        if relevance > 0.2:  # Only include if somewhat relevant
            matches.append({
                "contact": contact.model_dump(),
                "match_score": round(final_score, 2),
                "relevance": round(relevance, 2),
                "matching_expertise": list(set(matching_tags)),
                "why_good_match": f"{contact.name} has expertise in {', '.join(list(set(matching_tags))[:3])}"
            })
    
    # Sort by score
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    matches = matches[:top_n]
    
    result = {
        "author_need": need.get("author", "someone") + " needs " + need.get("need_type", "help"),
        "keywords": keywords,
        "matches": matches,
        "total_found": len(matches)
    }
    
    return json.dumps(result, default=str)


def generate_intro_message(match_json: str, to_poster: bool = True) -> str:
    """
    Generate introduction message to facilitate the connection.
    
    Args:
        match_json: JSON with a single match from find_matching_contacts
        to_poster: If True, message to person who posted. If False, message to your contact.
        
    Returns:
        Draft message text
    """
    match = json.loads(match_json)
    
    if isinstance(match, dict) and "matches" in match:
        # Handle full result
        if not match["matches"]:
            return "No matches found to introduce"
        match = match["matches"][0]
    
    contact = match["contact"]
    expertise = match.get("matching_expertise", [])
    
    if to_poster:
        # Message to the person who posted the need
        message = f"Hi! Saw your post and thought I could help connect you with someone perfect.\n\n"
        message += f"I'd like to introduce you to {contact['name']}, {contact['title']} at {contact['company']}. "
        message += f"They have deep expertise in {', '.join(expertise[:2])} which aligns directly with what you're looking for.\n\n"
        message += f"Notes: {contact.get('notes', 'They are excellent in their field.')}\n\n"
        message += f"Would you be open to a quick intro call? Happy to facilitate."
    else:
        # Message to your contact asking if they're interested
        message = f"Hi {contact['name'].split()[0]},\n\n"
        message += f"I came across someone on LinkedIn who's looking for help with {', '.join(expertise[:2])} - "
        message += f"right up your alley!\n\n"
        message += f"They seem like a great fit for your expertise. Would you be open to a quick intro? "
        message += f"Happy to connect you if you have 15-20 mins to chat with them.\n\n"
        message += f"Let me know!"
    
    return message


def create_opportunity_summary(matches_json: str) -> str:
    """
    Create a summary of connector opportunities with action items.
    
    Args:
        matches_json: JSON from find_matching_contacts
        
    Returns:
        Human-readable summary
    """
    data = json.loads(matches_json)
    matches = data.get("matches", [])
    
    if not matches:
        return "No connector opportunities found. Keep monitoring for posts that match your network's expertise."
    
    summary = f"**CONNECTOR OPPORTUNITY**\n\n"
    summary += f"Someone needs: {', '.join(data.get('keywords', []))}\n\n"
    summary += f"Found {len(matches)} contacts from your network who could help:\n\n"
    
    for i, match in enumerate(matches, 1):
        contact = match["contact"]
        summary += f"{i}. **{contact['name']}** ({contact['title']}) - Match: {match['match_score']}\n"
        summary += f"   Expertise: {', '.join(match['matching_expertise'])}\n"
        summary += f"   Why: {match['why_good_match']}\n\n"
    
    summary += f"\n**NEXT ACTIONS:**\n"
    summary += f"1. Message your top contact ({matches[0]['contact']['name']}) to gauge interest\n"
    summary += f"2. If interested, intro them to the person who posted\n"
    summary += f"3. Track outcome - successful intros build your connector reputation\n\n"
    summary += f"**VALUE**: By facilitating this intro, you:\n"
    summary += f"- Help someone in your network find what they need\n"
    summary += f"- Strengthen relationship with your contact by sending them opportunities\n"
    summary += f"- Build reputation as a valuable connector\n"
    
    return summary


# ============================================================================
# AGENT DEFINITION  
# ============================================================================

root_agent = Agent(
    name="connector_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a Connector Agent that helps people facilitate valuable introductions.
    
    Your workflow:
    1. When you see a LinkedIn post expressing a need, use extract_need_from_post
    2. Find matching contacts from the user's network using find_matching_contacts
    3. Generate intro messages using generate_intro_message
    4. Provide an opportunity summary with clear next actions
    
    You create VALUE by:
    - Helping people find what they need through warm intros
    - Sending your contacts relevant opportunities  
    - Building the user's reputation as a connector
    
    Always explain WHY each match is good and what the user should do next.
    Be enthusiastic about connector opportunities - they're valuable for everyone!
    """,
    tools=[
        extract_need_from_post,
        find_matching_contacts,
        generate_intro_message,
        create_opportunity_summary
    ],
)

app = App(root_agent=root_agent, name="network_bounty_hunter_agent")
