"""Network Bounty Hunter Agent - Main agent implementation."""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict
import google.auth

from google.adk.agents import Agent
from google.adk.apps.app import App

from models import (
    NeedSpec, Contact, RankedContact, MessageDraft,
    NeedSpecResponse, RankingResponse, DraftResponse
)

# Configure GCP
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# ============================================================================
# MOCK DATA (for MVP)
# ============================================================================

MOCK_CONTACTS = [
    Contact(
        id="c1",
        name="Sarah Chen",
        title="VP of Packaging Innovation",
        company="GreenPack Solutions",
        location="San Francisco, CA",
        profile_url="linkedin.com/in/sarachen",
        relationship_strength=0.7,
        tags=["packaging", "bioplastics", "sustainability"],
        source="linkedin_comet"
    ),
    Contact(
        id="c2",
        name="Michael Rodriguez",
        title="Materials Engineer",
        company="EcoMaterials Inc",
        location="New York, NY",
        relationship_strength=0.4,
        tags=["materials", "bioplastics", "R&D"],
        source="linkedin_comet"
    ),
    Contact(
        id="c3",
        name="Dr. Amy Wong",
        title="Director of Sustainable Packaging",
        company="BioCycle Corp",
        location="Boston, MA",
        relationship_strength=0.8,
        last_interaction=datetime.now() - timedelta(days=30),
        tags=["packaging", "compostable", "innovation"],
        source="manual"
    ),
]

# ============================================================================
# AGENT TOOLS
# ============================================================================

def parse_need_spec(user_input: str) -> str:
    """
    Parse user's free-text need into structured NeedSpec.
    
    Args:
        user_input: Free text like "I need a packaging engineer with bioplastics experience in NYC"
        
    Returns:
        JSON string of NeedSpec with extracted objective, persona, geography, keywords
    """
    # This is a simplified parser - in production, use LLM with structured output
    keywords = []
    geography = []
    objective_type = "intro"
    
    input_lower = user_input.lower()
    
    # Extract keywords
    if "packaging" in input_lower:
        keywords.append("packaging")
    if "bioplastics" in input_lower or "bioplastic" in input_lower:
        keywords.append("bioplastics")
    if "engineer" in input_lower:
        keywords.append("engineer")
    if "compostable" in input_lower:
        keywords.append("compostable")
    if "sustainable" in input_lower or "sustainability" in input_lower:
        keywords.append("sustainability")
        
    # Extract geography
    if "nyc" in input_lower or "new york" in input_lower:
        geography.append("New York, NY")
    if "sf" in input_lower or "san francisco" in input_lower:
        geography.append("San Francisco, CA")
    if "boston" in input_lower:
        geography.append("Boston, MA")
        
    # Determine objective
    if "hire" in input_lower or "hiring" in input_lower:
        objective_type = "hire"
    elif "partner" in input_lower:
        objective_type = "partner"
    elif "raise" in input_lower or "investor" in input_lower:
        objective_type = "raise"
        
    need_spec = NeedSpec(
        id=str(uuid.uuid4()),
        raw_input=user_input,
        objective_type=objective_type,
        target_persona={"keywords": keywords},
        geography=geography if geography else None,
        keywords_must=keywords,
        keywords_avoid=[],
        time_urgency="medium"
    )
    
    response = NeedSpecResponse(need_spec=need_spec)
    return json.dumps(response.model_dump(), default=str)


def rank_contacts(need_spec_json: str, top_n: int = 5) -> str:
    """
    Rank contacts based on NeedSpec criteria.
    
    Args:
        need_spec_json: JSON string of NeedSpec
        top_n: Number of top contacts to return
        
    Returns:
        JSON string of RankingResponse with ranked contacts
    """
    start_time = datetime.now()
    
    # Parse NeedSpec
    need_data = json.loads(need_spec_json)
    if "need_spec" in need_data:
        need_data = need_data["need_spec"]
    
    keywords_must = need_data.get("keywords_must", [])
    geography = need_data.get("geography", [])
    
    ranked = []
    
    for contact in MOCK_CONTACTS:
        # Calculate relevance score
        relevance = 0
        for keyword in keywords_must:
            if any(keyword.lower() in tag.lower() for tag in contact.tags):
                relevance += 0.3
            if contact.title and keyword.lower() in contact.title.lower():
                relevance += 0.2
        relevance = min(relevance, 1.0)
        
        # Relationship score (already in contact)
        relationship = contact.relationship_strength
        
        # Recency score
        recency = 0.5  # Default
        if contact.last_interaction:
            days_since = (datetime.now() - contact.last_interaction).days
            if days_since <= 30:
                recency = 1.0
            elif days_since <= 90:
                recency = 0.7
            else:
                recency = 0.3
        else:
            recency = 0.8  # Never contacted - fresh opportunity
            
        # Geography match
        geo_match = False
        if geography and contact.location:
            for geo in geography:
                if geo.lower() in contact.location.lower():
                    geo_match = True
                    break
        
        # Calculate final score
        # Score = 0.4*Relevance + 0.3*Relationship + 0.2*Recency + 0.1*Geo
        score = (0.4 * relevance + 
                 0.3 * relationship + 
                 0.2 * recency +
                 (0.1 if geo_match else 0))
        
        justification = f"Relevance: {relevance:.2f} (keyword matches), "
        justification += f"Relationship: {relationship:.2f}, "
        justification += f"Recency: {recency:.2f}"
        if geo_match:
            justification += ", Geographic match"
        
        ranked.append(RankedContact(
            contact=contact,
            rank_score=score,
            rank_justification=justification,
            relevance_score=relevance,
            relationship_score=relationship,
            recency_score=recency
        ))
    
    # Sort by score
    ranked.sort(key=lambda x: x.rank_score, reverse=True)
    ranked = ranked[:top_n]
    
    elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
    
    response = RankingResponse(
        ranked_contacts=ranked,
        total_candidates=len(MOCK_CONTACTS),
        ranking_time_ms=elapsed_ms
    )
    
    return json.dumps(response.model_dump(), default=str)


def generate_outreach_drafts(contact_json: str, need_context: str = "") -> str:
    """
    Generate personalized outreach drafts for a contact.
    
    Args:
        contact_json: JSON string of Contact
        need_context: Context about what user needs
        
    Returns:
        JSON string of DraftResponse with LinkedIn DM and email drafts
    """
    start_time = datetime.now()
    
    contact_data = json.loads(contact_json)
    if "contact" in contact_data:
        contact_data = contact_data["contact"]
    
    name = contact_data.get("name", "there")
    title = contact_data.get("title", "")
    company = contact_data.get("company", "")
    
    # LinkedIn DM (150 char limit)
    linkedin_dm = f"Hi {name.split()[0]}, impressed by your work in {title.split()[-2] if title else 'packaging'}. "
    linkedin_dm += "Would love to connect and learn about your experience. Coffee chat?"
    
    # Email (short, professional)
    email_subject = f"Quick intro - {need_context.split()[0:4]}"
    email_body = f"Hi {name},\n\n"
    email_body += f"I came across your profile and was impressed by your work as {title} at {company}.\n\n"
    email_body += f"I'm working on {need_context.lower()} and thought you'd be a great person to connect with given your experience in {', '.join(contact_data.get('tags', ['this space'])[:2])}.\n\n"
    email_body += "Would you be open to a brief 15-20 minute call to learn from your experience?\n\n"
    email_body += "Best regards"
    
    drafts = [
        MessageDraft(
            channel="linkedin_dm",
            body=linkedin_dm,
            char_count=len(linkedin_dm)
        ),
        MessageDraft(
            channel="email",
            subject=email_subject,
            body=email_body,
            char_count=len(email_body)
        )
    ]
    
    elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
    
    response = DraftResponse(
        drafts=drafts,
        contact_id=contact_data.get("id", "unknown"),
        generation_time_ms=elapsed_ms
    )
    
    return json.dumps(response.model_dump(), default=str)


def create_pipeline_summary(ranked_contacts_json: str) -> str:
    """
    Create a summary of the pipeline with next actions.
    
    Args:
        ranked_contacts_json: JSON string of RankingResponse
        
    Returns:
        Human-readable summary of pipeline with recommendations
    """
    data = json.loads(ranked_contacts_json)
    ranked = data.get("ranked_contacts", [])
    
    if not ranked:
        return "No contacts matched your criteria. Try broadening your search."
    
    summary = f"Found {len(ranked)} strong candidates:\n\n"
    
    for i, rc in enumerate(ranked, 1):
        contact = rc["contact"]
        summary += f"{i}. **{contact['name']}** - {contact['title']} at {contact['company']}\n"
        summary += f"   Score: {rc['rank_score']:.2f} | {rc['rank_justification']}\n"
        summary += f"   Next action: Draft personalized outreach\n\n"
    
    summary += "\nRecommendations:\n"
    summary += "- Start with top 3 contacts for highest ROI\n"
    summary += "- Draft personalized messages (avoid templates)\n"
    summary += "- Schedule follow-up for non-responders in 5-7 days\n"
    
    return summary


# ============================================================================
# AGENT DEFINITION
# ============================================================================

root_agent = Agent(
    name="network_bounty_hunter",
    model="gemini-2.5-flash",
    instruction="""
    You are a Network Bounty Hunter Agent that helps users find and connect with the right people.
    
    When a user says "I need X", you:
    1. Parse their need into structured criteria using parse_need_spec
    2. Rank contacts based on relevance using rank_contacts
    3. Generate personalized outreach drafts using generate_outreach_drafts
    4. Provide a pipeline summary with next actions
    
    Always be helpful, concise, and actionable. Explain your reasoning but keep it brief.
    Focus on the top 3-5 most relevant contacts to avoid overwhelming the user.
    """,
    tools=[
        parse_need_spec,
        rank_contacts,
        generate_outreach_drafts,
        create_pipeline_summary
    ],
)

app = App(root_agent=root_agent, name="network-bounty-hunter-agent")
