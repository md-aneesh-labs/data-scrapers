# data-scrapers

Scrapy crawlers, each in its own package under `crawlers/`, run from `main.py`.

## Setup

Uses the `scrapers` conda environment.

```bash
conda activate scrapers
pip install -r requirements.txt
```

## Run

Run from the project root:

```bash
python main.py
```

This runs every enabled crawler in `crawlers.json`.

## Project structure

```
data-scrapers/
├── main.py            # reads crawlers.json and runs the enabled crawlers
├── crawlers.json      # which crawlers to run
├── settings.py        # shared Scrapy settings (output, logging, delays)
├── scrapy.cfg         # points Scrapy to settings.py
├── crawlers/
│   ├── pipelines.py   # item pipelines
│   └── quotes/
│       └── spider.py  # quotes.toscrape.com crawler
└── output/            # scraped data (not committed)
```

## crawlers.json

```json
[
  { "name": "quotes", "enabled": true }
]
```

- `name`: the spider's `name` attribute
- `enabled`: `false` skips the crawler
- `args` (optional): passed to the spider and available as `self.<name>`. Values arrive as strings.

## How a crawler runs

1. `start()` sends the first request.
2. Scrapy downloads it and calls the request's `callback` (usually `parse`) with the response.
3. `parse()` yields items (dicts), which are saved to the output file, and new requests (such as the next page), which go back to step 2.
4. The crawl ends when there are no requests left.

Use `meta` (read with `response.meta`) or `cb_kwargs` to pass values like the page number from one request to the next callback.

## Output

Each crawler writes its items to `output/<crawler name>_<time>.json`, for example:

```
output/quotes_2026-10-08T21-34-20+00-00.json
```

The time is in UTC. The filename pattern is set by `FEEDS` in `settings.py`.

The quotes crawler yields one item per page:

```json
[
  {
    "page": 1,
    "data": [
      { "quote": "...", "author_name": "...", "tags": ["..."] }
    ]
  }
]
```

## Item pipelines

Pipelines in `crawlers/pipelines.py` receive every item before it's saved, which makes them the place to clean, modify or drop items. Enable a pipeline for one crawler through `custom_settings` on its spider:

```python
custom_settings = {
    "ITEM_PIPELINES": {"crawlers.pipelines.QuotesPipeline": 300},
}
```

`process_item` must `return item`, or the item won't be saved.

## Adding a crawler

1. Create `crawlers/<name>/__init__.py` (empty) and `crawlers/<name>/spider.py` with a `scrapy.Spider` subclass. Its `name` attribute is what goes in `crawlers.json`.
2. Add it to `crawlers.json`.

Shared settings live in `settings.py`. Override them for one crawler with `custom_settings` on its spider.

## Logs

Set `LOG_LEVEL` in `settings.py`:

- `"INFO"`: one line per page, plus a summary at the end
- `"WARNING"`: only warnings and errors, which makes your own `print()` output easy to see
- `"DEBUG"`: everything, including every request and item

## Testing selectors

```bash
scrapy shell "https://quotes.toscrape.com/"
>>> response.xpath("//small[@class='author']/text()").getall()
```
