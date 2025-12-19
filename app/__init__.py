"""Network Bounty Hunter Agent - Connector Matchmaking System.

Monitors LinkedIn posts for needs and matches them with your contacts.
"""

from app.agent import app
from app.models import Contact, Need, OpportunitySummary

__all__ = ['app', 'Contact', 'Need', 'OpportunitySummary']
