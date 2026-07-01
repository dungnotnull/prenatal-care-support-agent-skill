# -*- coding: utf-8 -*-
"""
knowledge_updater.py — Self-improving knowledge pipeline for `prenatal-care-support` (idea #86).

Crawls authoritative Health, Wellness & Psychology sources with crawl4ai, scores entries by
recency and domain relevance, and appends new, de-duplicated entries to SECOND-KNOWLEDGE-BRAIN.md.

Schedule: weekly (cron). Cluster: health-wellness.

Author: prenatal-care-support skill
Version: 1.0.0
Last Updated: 2026-07-01
"""

import os
import re
import json
import hashlib
import datetime
import argparse
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Configuration
BRAIN_PATH = Path(__file__).parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"
CACHE_PATH = Path(__file__).parent.parent / ".cache" / "knowledge_cache.json"
ARXIV_API_URL = "http://export.arxiv.org/api/query"

ARXIV_CATEGORIES = ['q-bio.QM', 'q-bio.PE', 'q-bio.TO', 'stat.AP', 'stat.ME']
SEARCH_QUERIES = [
    'antenatal care WHO guideline',
    'pregnancy danger signs screening',
    'prenatal nutrition evidence',
    'gestational diabetes screening',
    'preeclampsia early detection',
    'prenatal mental health EPDS',
    'pregnancy care schedule',
    'folic acid supplementation pregnancy',
    'prenatal vitamins guidelines',
    'pregnancy lifestyle recommendations'
]

DOMAIN_SOURCES = {
    'WHO': 'https://www.who.int/health-topics/pregnancy',
    'ACOG': 'https://www.acog.org/womens-health',
    'NICE': 'https://www.nice.org.uk/guidance/ng/pregnancy',
    'CDC': 'https://www.cdc.gov/reproductivehealth/pregnancy',
    'Cochrane': 'https://www.cochranelibrary.com/browse/pregnancy-and-childbirth'
}

DOMAIN_KEYWORDS = [
    'antenatal', 'pregnancy', 'prenatal', 'maternal', 'gestational',
    'obstetric', 'perinatal', 'postpartum', 'fetal', 'neonatal',
    'epds', 'edinburgh', 'preeclampsia', 'eclampsia', 'gestational diabetes',
    'folic acid', 'prenatal vitamin', 'midwife', 'obstetrician'
]

EVIDENCE_TIERS = {
    'systematic review': 5,
    'meta-analysis': 5,
    'rct': 4,
    'randomized controlled': 4,
    'cohort': 3,
    'case-control': 3,
    'guideline': 4,
    'expert opinion': 2,
    'review': 3,
    'recommendation': 3
}


@dataclass
class KnowledgeEntry:
    """A single knowledge entry with scoring metadata."""
    title: str
    authors: str
    year: str
    venue: str
    url: str
    abstract: str = ""
    relevance_score: float = 0.0
    evidence_tier: int = 0
    entry_hash: str = ""

    def to_markdown_row(self) -> str:
        """Format as markdown table row."""
        title_esc = self.title[:80].replace("|", "\\|")
        authors_esc = (self.authors or "Unknown")[:40].replace("|", "\\|")
        return (
            f"| {title_esc} | {authors_esc} | {self.year} | "
            f"{self.venue[:30]} | {self.url[:60]} | "
            f"tier-{self.evidence_tier}, score-{self.relevance_score:.1f} | "
            f"<!--h:{self.entry_hash}-->"
        )


class KnowledgeCache:
    """Persistent cache for fetched entries to avoid re-fetching."""

    def __init__(self, cache_path: Path = CACHE_PATH):
        self.cache_path = cache_path
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.cache_path.exists():
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save(self):
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, key: str) -> Optional[Dict]:
        return self.data.get(key)

    def set(self, key: str, value: Dict, ttl_days: int = 7):
        expiry = (datetime.date.today() + datetime.timedelta(days=ttl_days)).isoformat()
        self.data[key] = {**value, '_cache_expiry': expiry}
        self._save()

    def is_expired(self, key: str) -> bool:
        entry = self.data.get(key)
        if not entry or '_cache_expiry' not in entry:
            return True
        expiry = datetime.date.fromisoformat(entry['_cache_expiry'])
        return datetime.date.today() > expiry

    def clean_expired(self):
        today = datetime.date.today().isoformat()
        expired = [k for k, v in self.data.items()
                   if v.get('_cache_expiry', '') < today]
        for k in expired:
            del self.data[k]
        if expired:
            self._save()


def compute_entry_hash(entry: Dict[str, Any]) -> str:
    """Generate stable hash from URL or title+authors."""
    content = entry.get('url', '') or entry.get('title', '') + entry.get('authors', '')
    return hashlib.sha256(content.encode('utf-8', errors='ignore')).hexdigest()[:12]


def score_entry(entry: Dict[str, Any]) -> float:
    """
    Score an entry by recency and domain relevance.

    Returns:
        Float score (higher = more relevant/recent)
    """
    score = 0.0

    # Recency scoring (more recent = better)
    try:
        year = int(entry.get('year', '0'))
        base_year = 2018
        recency_score = max(0, year - base_year) * 0.3
        score += recency_score
    except (ValueError, TypeError):
        pass

    # Domain relevance scoring
    text = (
        entry.get('title', '') + ' ' +
        entry.get('abstract', '') + ' ' +
        entry.get('venue', '')
    ).lower()

    # Primary keyword matches (weighted higher)
    primary_hits = sum(3.0 for kw in ['pregnancy', 'prenatal', 'antenatal', 'maternal']
                      if kw in text)
    score += primary_hits

    # Secondary keyword matches
    secondary_hits = sum(1.5 for kw in DOMAIN_KEYWORDS[4:]
                        if kw.lower() in text)
    score += secondary_hits

    # Evidence tier bonus
    venue_lower = entry.get('venue', '').lower()
    abstract_lower = entry.get('abstract', '').lower()
    for tier_name, tier_score in EVIDENCE_TIERS.items():
        if tier_name in venue_lower or tier_name in abstract_lower:
            score += tier_score * 0.2
            break

    return round(score, 2)


def detect_evidence_tier(entry: Dict[str, Any]) -> int:
    """Detect evidence tier from venue and abstract."""
    venue = entry.get('venue', '').lower()
    abstract = entry.get('abstract', '').lower()
    combined = venue + ' ' + abstract

    for tier_name, tier_score in EVIDENCE_TIERS.items():
        if tier_name in combined:
            return tier_score
    return 2  # Default to expert opinion


def fetch_arxiv_papers(categories: List[str], max_results: int = 25) -> List[Dict]:
    """
    Fetch recent papers from ArXiv API.

    Args:
        categories: List of ArXiv category IDs
        max_results: Maximum results per category

    Returns:
        List of paper dictionaries
    """
    import urllib.request
    import urllib.parse
    import xml.etree.ElementTree as ET

    entries = []

    for cat in categories:
        params = urllib.parse.urlencode({
            "search_query": f"cat:{cat}",
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": max_results,
        })
        url = f"{ARXIV_API_URL}?{params}"

        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                xml_data = response.read().decode('utf-8', errors='ignore')

            root = ET.fromstring(xml_data)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', namespace):
                # Extract authors
                authors = []
                for author in entry.findall('atom:author', namespace):
                    name_elem = author.find('atom:name', namespace)
                    if name_elem is not None:
                        authors.append(name_elem.text)

                # Extract paper details
                title_elem = entry.find('atom:title', namespace)
                summary_elem = entry.find('atom:summary', namespace)
                id_elem = entry.find('atom:id', namespace)
                published_elem = entry.find('atom:published', namespace)

                paper = {
                    'title': (title_elem.text or '').replace('\n', ' ').strip(),
                    'authors': ', '.join(authors[:5]),  # Limit to 5 authors
                    'year': (published_elem.text or '')[:4] if published_elem else '',
                    'venue': f'arXiv:{cat}',
                    'url': id_elem.text if id_elem else '',
                    'abstract': (summary_elem.text or '').replace('\n', ' ').strip()
                }

                entries.append(paper)

        except Exception as e:
            print(f"[ArXiv] Failed to fetch {cat}: {e}")

    return entries


def parse_existing_entries(brain_text: str) -> set:
    """Extract existing entry hashes from markdown comments."""
    return set(re.findall(r'<!--h:([0-9a-f]{12})-->', brain_text))


def append_new_entries(entries: List[Dict], brain_path: Path, dry_run: bool = False) -> int:
    """
    Append new entries to SECOND-KNOWLEDGE-BRAIN.md with deduplication.

    Args:
        entries: List of entry dictionaries
        brain_path: Path to the knowledge brain file
        dry_run: If True, don't actually write changes

    Returns:
        Number of new entries appended
    """
    # Read existing brain
    try:
        with open(brain_path, 'r', encoding='utf-8') as f:
            brain_content = f.read()
    except IOError:
        print(f"[ERROR] Could not read {brain_path}")
        return 0

    existing_hashes = parse_existing_entries(brain_content)

    # Score and rank entries
    scored_entries = []
    for entry in entries:
        if not entry.get('title') or not entry.get('url'):
            continue

        entry_hash = compute_entry_hash(entry)
        if entry_hash in existing_hashes:
            continue  # Skip duplicates

        # Create KnowledgeEntry
        knowledge_entry = KnowledgeEntry(
            title=entry['title'],
            authors=entry.get('authors', ''),
            year=entry.get('year', ''),
            venue=entry.get('venue', ''),
            url=entry['url'],
            abstract=entry.get('abstract', ''),
            relevance_score=score_entry(entry),
            evidence_tier=detect_evidence_tier(entry),
            entry_hash=entry_hash
        )
        scored_entries.append(knowledge_entry)
        existing_hashes.add(entry_hash)

    # Sort by relevance score
    scored_entries.sort(key=lambda e: e.relevance_score, reverse=True)

    if not scored_entries:
        print("[INFO] No new entries to append.")
        return 0

    # Build markdown block
    today = datetime.date.today().isoformat()
    header = f"\n- **{today}** — Auto-crawl appended {len(scored_entries)} new entries.\n"
    table_header = "| Title | Authors | Year | Venue | DOI/URL | Relevance |\n"
    table_header += "|-------|---------|------|-------|----------|-----------|\n"

    rows = []
    for entry in scored_entries:
        rows.append(entry.to_markdown_row())

    markdown_block = header + table_header + '\n'.join(rows) + '\n'

    if dry_run:
        print("[DRY RUN] Would append:")
        print(markdown_block)
        return len(scored_entries)

    # Append to brain
    try:
        with open(brain_path, 'a', encoding='utf-8') as f:
            f.write(markdown_block)
        print(f"[SUCCESS] Appended {len(scored_entries)} new entries to {brain_path.name}")
        return len(scored_entries)
    except IOError as e:
        print(f"[ERROR] Could not write to {brain_path}: {e}")
        return 0


def run_crawl_pipeline(arxiv: bool = True, web_sources: bool = False,
                       max_results: int = 25, dry_run: bool = False,
                       cache: Optional[KnowledgeCache] = None) -> int:
    """
    Execute the full crawl pipeline.

    Args:
        arxiv: Fetch from ArXiv
        web_sources: Fetch from domain web sources
        max_results: Maximum results per source
        dry_run: Don't write changes
        cache: KnowledgeCache instance

    Returns:
        Total number of new entries
    """
    if cache is None:
        cache = KnowledgeCache()

    cache.clean_expired()

    all_entries = []

    # ArXiv fetch
    if arxiv:
        print("[ArXiv] Fetching papers...")
        cache_key = f"arxiv_{','.join(ARXIV_CATEGORIES)}_{max_results}"

        if not cache.is_expired(cache_key):
            cached = cache.get(cache_key)
            if cached:
                all_entries.extend(cached.get('entries', []))
                print(f"[ArXiv] Using cached data ({len(cached['entries'])} entries)")
        else:
            arxiv_entries = fetch_arxiv_papers(ARXIV_CATEGORIES, max_results)
            cache.set(cache_key, {'entries': arxiv_entries}, ttl_days=7)
            all_entries.extend(arxiv_entries)
            print(f"[ArXiv] Fetched {len(arxiv_entries)} papers")

    # Domain sources (placeholder for crawl4ai integration)
    if web_sources:
        print("[Web] Domain source crawling requires crawl4ai integration.")
        print("[Web] Skipping for now (would crawl: WHO, ACOG, NICE, CDC, Cochrane)")

    # Deduplicate across sources
    seen_urls = {}
    unique_entries = []
    for entry in all_entries:
        url = entry.get('url', '')
        if url and url not in seen_urls:
            seen_urls[url] = True
            unique_entries.append(entry)
        elif not url:
            # Keep entries without URL but with title
            title = entry.get('title', '')
            if title and title not in seen_urls:
                seen_urls[title] = True
                unique_entries.append(entry)

    print(f"[Pipeline] Total unique entries: {len(unique_entries)}")

    # Append to brain
    return append_new_entries(unique_entries, BRAIN_PATH, dry_run)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Update SECOND-KNOWLEDGE-BRAIN.md with latest research'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Show what would be added without writing'
    )
    parser.add_argument(
        '--max-results', '-m',
        type=int,
        default=25,
        help='Maximum results per source (default: 25)'
    )
    parser.add_argument(
        '--no-arxiv',
        action='store_true',
        help='Skip ArXiv fetching'
    )
    parser.add_argument(
        '--web-sources',
        action='store_true',
        help='Include web domain sources (requires crawl4ai)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Ignore cache and force re-fetch'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Prenatal Care Support — Knowledge Updater")
    print("=" * 60)

    cache = KnowledgeCache()
    if args.force:
        print("[INFO] Force mode: clearing cache")
        cache.data = {}
        cache._save()

    total_new = run_crawl_pipeline(
        arxiv=not args.no_arxiv,
        web_sources=args.web_sources,
        max_results=args.max_results,
        dry_run=args.dry_run,
        cache=cache
    )

    print("=" * 60)
    if args.dry_run:
        print(f"[DRY RUN] Would add {total_new} new entries")
    else:
        print(f"[COMPLETE] Added {total_new} new entries")
    print("=" * 60)


if __name__ == "__main__":
    main()
