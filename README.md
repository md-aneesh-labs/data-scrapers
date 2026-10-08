# data-scrapers

Scrapy crawlers, each in its own package under `crawlers/`, run from `main.py`.

## Run

```bash
conda activate scrapers
python main.py                      # runs every enabled crawler in crawlers.json
python main.py --config other.json  # use a different config file
```

## crawlers.json

```json
{
  "crawlers": [
    { "name": "quotes", "enabled": true, "output": "output/quotes.jsonl", "args": {} }
  ]
}
```

- `name`: the spider's `name` attribute
- `enabled`: set to `false` to skip it (default `true`)
- `output`: output file; the format comes from the extension (`.jsonl`, `.json`, `.csv`, `.xml`). Default is `output/<name>.jsonl`
- `args`: keyword arguments passed to the spider

## Adding a crawler

1. Create `crawlers/<name>/__init__.py` and `crawlers/<name>/spider.py` with a `scrapy.Spider` subclass.
2. Add an entry to `crawlers.json`.

Shared settings live in `settings.py`. Override them for one crawler with `custom_settings` on its spider.
