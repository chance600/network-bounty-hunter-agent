"""Data models for Network Bounty Hunter Agent."""
from datetime import datetime
from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


# ============================================================================
# CORE ENTITIES
# ============================================================================

class NeedSpec(BaseModel):
    """Structured representation of user's networking need."""
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: str = "default_user"
    raw_input: str  # "I need X"
    objective_type: Literal["intro", "hire", "sell", "raise", "partner", "advisor", "press"]
    target_persona: dict  # {"title": [...], "industry": [...], "company_type": [...]}
    geography: Optional[List[str]] = None
    keywords_must: List[str] = Field(default_factory=list)
    keywords_avoid: List[str] = Field(default_factory=list)
    time_urgency: Literal["high", "medium", "low"] = "medium"
    ask_shape: str = "intro call"  # "30-min intro call", "pilot partnership", etc.


class Contact(BaseModel):
    """A contact in the network."""
    id: str
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    profile_url: Optional[str] = None
    relationship_strength: float = Field(default=0.3, ge=0, le=1)  # 0-1
    last_interaction: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    notes: str = ""
    source: str = "manual"  # "linkedin_comet", "manual", etc.


class PersonLead(BaseModel):
    """A person discovered via signal ingestion."""
    name: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    profile_url: Optional[str] = None
    snippet: str = ""
    why_relevant: str = ""
    confidence: float = Field(default=0.5, ge=0, le=1)
    mutuals: Optional[int] = None
    last_seen: datetime = Field(default_factory=datetime.now)


class CompanyLead(BaseModel):
    """A company discovered via signal ingestion."""
    company: str
    industry: Optional[str] = None
    size: Optional[str] = None
    event: str  # "raised", "hiring", "new product", "expanding"
    url: Optional[str] = None
    snippet: str = ""


class OpportunityLead(BaseModel):
    """An opportunity (grant, job, RFP, event)."""
    title: str
    type: Literal["grant", "job", "rfp", "event"]
    deadline: Optional[datetime] = None
    url: Optional[str] = None
    snippet: str = ""


class ContentLead(BaseModel):
    """Content mentioning keywords (post, article)."""
    title: str
    author: Optional[str] = None
    url: Optional[str] = None
    snippet: str = ""


class SignalItem(BaseModel):
    """A single signal item from any source."""
    type: Literal["person", "company", "opportunity", "content"]
    data: Union[PersonLead, CompanyLead, OpportunityLead, ContentLead]


class SignalDump(BaseModel):
    """A batch of signals from a single source run."""
    id: str
    source: Literal["linkedin_comet", "rss", "news", "jobs", "grants", "github", "events", "manual"]
    run_id: str
    run_ts: datetime = Field(default_factory=datetime.now)
    query_pack_id: Optional[str] = None
    items: List[SignalItem] = Field(default_factory=list)


# ============================================================================
# RANKING & OUTREACH
# ============================================================================

class RankedContact(BaseModel):
    """A contact with ranking score and justification."""
    contact: Contact
    rank_score: float = Field(ge=0, le=1)
    rank_justification: str
    relevance_score: float = Field(default=0.5, ge=0, le=1)
    relationship_score: float = Field(default=0.3, ge=0, le=1)
    recency_score: float = Field(default=0.5, ge=0, le=1)
    connector_bonus: float = Field(default=0, ge=0, le=0.5)
    risk_discount: float = Field(default=0, ge=-0.5, le=0)


class MessageDraft(BaseModel):
    """A draft message for outreach."""
    channel: Literal["linkedin_dm", "email", "warm_intro"]
    subject: Optional[str] = None
    body: str
    tone: str = "professional"
    char_count: int = 0


class PipelineCard(BaseModel):
    """A card in the outreach pipeline."""
    id: str
    need_spec_id: str
    contact_id: str
    stage: Literal[
        "backlog",
        "candidates",
        "drafted",
        "sent",
        "follow_up_1",
        "follow_up_2",
        "warm_intro",
        "closed_won",
        "closed_lost"
    ]
    rank_score: float
    rank_justification: str
    drafts: List[MessageDraft] = Field(default_factory=list)
    next_action_date: Optional[datetime] = None
    status_tags: List[str] = Field(default_factory=list)
    outcome: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ============================================================================
# API RESPONSES
# ============================================================================

class NeedSpecResponse(BaseModel):
    """Response from NeedSpec parser."""
    need_spec: NeedSpec
    parsed_successfully: bool = True
    errors: List[str] = Field(default_factory=list)


class RankingResponse(BaseModel):
    """Response from contact ranker."""
    ranked_contacts: List[RankedContact]
    total_candidates: int
    ranking_time_ms: float


class DraftResponse(BaseModel):
    """Response from draft generator."""
    drafts: List[MessageDraft]
    contact_id: str
    generation_time_ms: float
