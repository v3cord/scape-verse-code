import json
import logging
import os
import subprocess
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException

logger = logging.getLogger("market_sentinel.scraper_chain")

router = APIRouter(prefix="/api/scraper", tags=["scraper"])

DISCOVERY_COLLECTOR_ID = os.getenv("DISCOVERY_COLLECTOR_ID", "c_msxihjnheicz27x5n")
EXTRACTION_COLLECTOR_ID = os.getenv("EXTRACTION_COLLECTOR_ID", "c_msxfmm4911y5zyk7sq")
SCRAPER_ARTIFACTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "scraper-artifacts",
)


def run_discovery_scraper(search_url: str) -> List[str]:
    output_file = os.path.join(SCRAPER_ARTIFACTS_DIR, "discovery_output.json")
    cmd = [
        "npx",
        "-p",
        "@brightdata/cli",
        "bdata",
        "scraper",
        "run",
        DISCOVERY_COLLECTOR_ID,
        search_url,
        "--pretty",
        "-o",
        output_file,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            discovered_urls = []
            for item in data:
                main_url = item.get("product_page_url") or item.get("product_url")
                if main_url and main_url not in discovered_urls:
                    discovered_urls.append(main_url)

                related = item.get("related_products", [])
                for rel_url in related:
                    if rel_url and rel_url not in discovered_urls:
                        discovered_urls.append(rel_url)

            return discovered_urls[:5]

        return [search_url]
    except Exception as e:
        logger.error(f"Discovery scraper error: {e}")
        return [search_url]


def run_extraction_scraper(product_urls: List[str]) -> List[Dict[str, Any]]:
    output_file = os.path.join(SCRAPER_ARTIFACTS_DIR, "raw_bright_data.json")
    urls_str = ",".join(product_urls)

    cmd = [
        "npx",
        "-p",
        "@brightdata/cli",
        "bdata",
        "scraper",
        "run",
        EXTRACTION_COLLECTOR_ID,
        "--urls",
        urls_str,
        "--pretty",
        "-o",
        output_file,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                return json.load(f)

        return []
    except Exception as e:
        logger.error(f"Extraction scraper error: {e}")
        return []


@router.post("/chain")
async def trigger_chained_scraper(payload: Dict[str, str]) -> Dict[str, Any]:
    search_url = payload.get(
        "search_url", "https://shopalto.xyz/search?q=headphones"
    )

    discovered_urls = run_discovery_scraper(search_url)
    extracted_data = run_extraction_scraper(discovered_urls)

    return {
        "status": "success",
        "discovery_collector_id": DISCOVERY_COLLECTOR_ID,
        "extraction_collector_id": EXTRACTION_COLLECTOR_ID,
        "discovered_urls": discovered_urls,
        "extracted_data": extracted_data,
    }
