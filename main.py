"""Entry point for running crawlers.

Reads crawler names from crawlers.json and runs every enabled one.

Usage:
    python main.py
    python main.py --config path/to/other.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "settings")

from scrapy.crawler import CrawlerProcess
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.project import get_project_settings

ROOT = Path(__file__).parent
DEFAULT_CONFIG = ROOT / "crawlers.json"


def load_config(path):
    with open(path) as f:
        entries = json.load(f)["crawlers"]
    return [entry for entry in entries if entry.get("enabled", True)]


def main():
    parser = argparse.ArgumentParser(description="Run crawlers listed in a JSON config.")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Path to crawler config (default: crawlers.json)")
    args = parser.parse_args()

    settings = get_project_settings()
    available = set(SpiderLoader.from_settings(settings).list())
    entries = load_config(args.config)

    if not entries:
        sys.exit(f"No enabled crawlers in {args.config}.")

    unknown = sorted({entry["name"] for entry in entries} - available)
    if unknown:
        sys.exit(f"Unknown crawler(s): {', '.join(unknown)}. Available: {', '.join(sorted(available))}")

    process = CrawlerProcess(settings)
    for entry in entries:
        name = entry["name"]
        output = ROOT / entry.get("output", f"output/{name}.jsonl")
        output.parent.mkdir(parents=True, exist_ok=True)

        crawler = process.create_crawler(name)
        crawler.settings.set(
            "FEEDS",
            {str(output): {"format": output.suffix.lstrip(".") or "jsonl", "overwrite": True}},
            priority="cmdline",
        )
        process.crawl(crawler, **entry.get("args", {}))

    process.start()


if __name__ == "__main__":
    main()
