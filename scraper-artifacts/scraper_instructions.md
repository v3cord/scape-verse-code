# Bright Data Scraper & Self-Healing Instructions

This document outlines the step-by-step procedure used to build, execute, and self-heal the e-commerce pricing scraper for **Market Sentinel** using the Bright Data CLI (`@brightdata/cli`).

---

## 1. Bright Data CLI Setup & Authentication

To ensure zero global dependency pollution, all Bright Data commands were executed via `npx`:

```bash
# Authenticate CLI with Bright Data account via browser OAuth
npx -p @brightdata/cli bdata login
```

Upon successful browser authentication, Bright Data CLI configured the active account key and created the required Web Unlocker zones (`cli_unlocker`, `cli_browser`).

---

## 2. Scraper Creation (Initial Template)

We created a Bright Data AI-driven scraper targeting public e-commerce product pages.

- **Target URL**: `https://shopalto.xyz/product/aurora-wireless-headphones`
- **Initial Extraction Schema**: `product_name`, `price`

```bash
npx -p @brightdata/cli bdata scraper create "https://shopalto.xyz/product/aurora-wireless-headphones" "Extract product name and price" --json --pretty
```

### Result:
- **Collector ID**: `c_msxfmm4911y5zyk7sq`
- **Status**: `done`

---

## 3. Proof of Self-Healing Capabilities (Schema Extension In-Place)

To demonstrate Bright Data's **AI Self-Healing** capabilities (satisfying Rule 9 requirements), we instructed the CLI to heal and extend collector `c_msxfmm4911y5zyk7sq` in-place.

### Healing Goal:
Extend the scraper schema to capture three additional fields: `description`, `image_url`, and `availability` alongside the original `product_name` and `price`.

### CLI Command Executed:
```bash
npx -p @brightdata/cli bdata scraper heal c_msxfmm4911y5zyk7sq "Also capture description, image_url, and availability alongside the existing product_name and price." --url "https://shopalto.xyz/product/aurora-wireless-headphones" --json --pretty
```

### Self-Healing Pipeline Execution:
1. **AI Flow**: The CLI triggered the `planner`, `control_preview_runner`, `code_fixer`, and `request_fulfillment_validator` stages.
2. **Approval Gate**: Returned state `awaiting_approval` with a diff preview of the extended fields.
3. **Approval Command**:
   ```bash
   npx -p @brightdata/cli bdata scraper approve c_msxfmm4911y5zyk7sq --url "https://shopalto.xyz/product/aurora-wireless-headphones"
   ```

> [!IMPORTANT]
> **Hackathon Self-Healing Proof**: The collector `c_msxfmm4911y5zyk7sq` was modified and healed in-place without generating a new ID or breaking existing API contracts. The self-healed code automatically extracted the expanded schema without manual selector maintenance.

---

## 4. Scraper Execution & Raw Output Artifact

We ran the healed collector against the target URL and saved the structured JSON response:

```bash
npx -p @brightdata/cli bdata scraper run c_msxfmm4911y5zyk7sq "https://shopalto.xyz/product/aurora-wireless-headphones" --pretty -o scraper-artifacts/raw_bright_data.json
```

### Saved Raw Output (`raw_bright_data.json`):
```json
[
  {
    "product_name": "Aurora Wireless Headphones",
    "price": {
      "value": 142.75,
      "currency": "USD",
      "symbol": "$"
    },
    "description": "Over-ear wireless headphones with 40 mm drivers, active noise cancellation, and high-fidelity audio.",
    "image_url": "https://loremflickr.com/800/800/headphones,audio?lock=0011&v=132",
    "availability": "In Stock",
    "input": {
      "url": "https://shopalto.xyz/product/aurora-wireless-headphones"
    }
  }
]
```

---

## 5. Discovery Scraper Creation & Pipeline Chaining

To support dynamic multi-product market discovery, we created a dedicated **Discovery Scraper** targeting e-commerce search query pages.

- **Target Search URL**: `https://shopalto.xyz/search?q=headphones`
- **Instruction**: Extract `product_url` for the top search results on the page.

### CLI Creation Command:
```bash
npx -p @brightdata/cli bdata scraper create "https://shopalto.xyz/search?q=headphones" "Extract ONLY the product_url for the top 5 search results on the page." --json --pretty
```

### Result:
- **Discovery Scraper Collector ID**: `c_msxihjnheicz27x5n`
- **Output Artifact**: Saved to [`./discovery_output.json`](./discovery_output.json).

### Chained Execution Pipeline:
1. **Stage 1 (Discovery)**: Collector `c_msxihjnheicz27x5n` scans search query pages to extract product URLs dynamically.
2. **Stage 2 (Extraction)**: Collector `c_msxfmm4911y5zyk7sq` ingests the discovered URLs to scrape detailed pricing and stock telemetry.

