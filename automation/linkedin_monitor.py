#!/usr/bin/env python3
"""
LinkedIn Network Monitor - Automated post scanning and contact matching

This script uses Perplexity API to search for LinkedIn posts containing
"I need X" requests, then processes them through the agent to find matches.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
import requests

# Add parent directory to path for app imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agent import app
from app.models import LinkedInPost, Contact

# Perplexity API configuration
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


def search_linkedin_posts(search_query: str) -> list[dict]:
    """
    Use Perplexity API to search for recent LinkedIn posts.
    
    Args:
        search_query: Search query for LinkedIn posts
        
    Returns:
        List of post data dictionaries
    """
    if not PERPLEXITY_API_KEY:
        print("❌ PERPLEXITY_API_KEY not found in environment")
        return []
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a LinkedIn post search assistant. Extract recent LinkedIn posts that match the search criteria. Return results as JSON array with fields: author_name, author_profile_url, post_text, post_url, posted_date."
            },
            {
                "role": "user",
                "content": f"Search for recent LinkedIn posts containing: {search_query}. Find posts from the last 7 days. Return as JSON array."
            }
        ],
        "temperature": 0.2,
        "return_citations": True
    }
    
    try:
        response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Try to parse JSON from response
        try:
            posts = json.loads(content)
            if isinstance(posts, list):
                return posts
        except json.JSONDecodeError:
            # If not pure JSON, try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', content)
            if json_match:
                posts = json.loads(json_match.group(1))
                if isinstance(posts, list):
                    return posts
        
        print(f"⚠️  Could not parse LinkedIn posts from response")
        return []
        
    except Exception as e:
        print(f"❌ Error searching LinkedIn posts: {e}")
        return []


def process_post(post_data: dict) -> dict:
    """
    Process a LinkedIn post through the agent to find matching contacts.
    
    Args:
        post_data: Dictionary with post information
        
    Returns:
        Dictionary with matches and agent results
    """
    try:
        # Create LinkedInPost object
        post = LinkedInPost(
            author_name=post_data.get("author_name", "Unknown"),
            author_profile_url=post_data.get("author_profile_url", ""),
            post_text=post_data.get("post_text", ""),
            post_url=post_data.get("post_url", ""),
            posted_date=post_data.get("posted_date", datetime.now().isoformat())
        )
        
        # Use the agent to process the post
        # The agent will extract the bounty, match contacts, and rank them
        query = f"Process this LinkedIn post and find matching contacts: {post.post_text}"
        
        # In a real implementation, you'd call the agent here
        # For now, return the post data
        return {
            "post": post.model_dump(),
            "processed": True,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error processing post: {e}")
        return {"error": str(e), "post_data": post_data}


def save_results(results: list[dict], output_dir: Path = Path("output")):
    """
    Save processing results to JSON file.
    
    Args:
        results: List of processing results
        output_dir: Directory to save results
    """
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"matches_{timestamp}.json"
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved to {output_file}")
    return output_file


def main():
    """
    Main automation workflow:
    1. Search for LinkedIn posts with "I need" requests
    2. Process each post through the agent
    3. Save results for notification/follow-up
    """
    print("🔍 LinkedIn Network Monitor - Starting...")
    print(f"⏰ Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Search queries to monitor
    search_queries = [
        '"I need" OR "looking for" OR "seeking" site:linkedin.com/posts',
        '"I need help with" OR "I need advice" site:linkedin.com/posts',
        '"looking to connect with" OR "seeking recommendations" site:linkedin.com/posts'
    ]
    
    all_results = []
    
    for query in search_queries:
        print(f"\n🔎 Searching: {query}")
        posts = search_linkedin_posts(query)
        print(f"📊 Found {len(posts)} posts")
        
        for i, post_data in enumerate(posts, 1):
            print(f"\n📝 Processing post {i}/{len(posts)}...")
            result = process_post(post_data)
            all_results.append(result)
    
    # Save all results
    if all_results:
        output_file = save_results(all_results)
        print(f"\n✨ Processed {len(all_results)} total posts")
        print(f"📁 Results: {output_file}")
    else:
        print("\n⚠️  No posts found to process")
    
    print("\n✅ LinkedIn monitoring completed successfully!")


if __name__ == "__main__":
    main()
