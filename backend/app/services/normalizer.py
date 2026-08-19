import json
import logging
import os
import re
from typing import Any, Dict
from fastapi import HTTPException

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from app.schemas import NormalizedProductData, RawProductData

logger = logging.getLogger("market_sentinel.normalizer")


def _fallback_normalize(raw_data: RawProductData) -> NormalizedProductData:
    product_name = raw_data.product_name or "Unknown Product"

    price_val = 0.0
    currency = "USD"

    if isinstance(raw_data.price, (int, float)):
        price_val = float(raw_data.price)
    elif raw_data.price and hasattr(raw_data.price, "value"):
        if raw_data.price.value is not None:
            price_val = float(raw_data.price.value)
        if raw_data.price.currency:
            currency = str(raw_data.price.currency)
    elif isinstance(raw_data.price, str):
        cleaned = re.sub(r"[^\d.]", "", raw_data.price)
        if cleaned:
            price_val = float(cleaned)

    avail_lower = (raw_data.availability or "").lower()
    if any(term in avail_lower for term in ["out of stock", "unavailable", "sold out"]):
        is_in_stock = False
    else:
        is_in_stock = True

    url = raw_data.input.url if raw_data.input else None

    return NormalizedProductData(
        product_name=product_name,
        price=price_val,
        is_in_stock=is_in_stock,
        currency=currency,
        description=raw_data.description,
        image_url=raw_data.image_url,
        url=url,
    )


async def normalize_product_data(raw_data: RawProductData) -> NormalizedProductData:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or not GENAI_AVAILABLE:
        return _fallback_normalize(raw_data)

    try:
        client = genai.Client(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        prompt = f"""
Normalize the following raw scraped product JSON into the exact JSON schema matching NormalizedProductData.

JSON Schema:
- product_name: (string)
- price: (float)
- is_in_stock: (boolean)
- currency: (string)
- description: (string or null)
- image_url: (string or null)
- url: (string or null)

Raw Input JSON:
{raw_data.model_dump_json()}

Return ONLY valid JSON.
"""

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )

        if not response or not response.text:
            raise ValueError("Empty response received from Gemini API")

        cleaned_json = response.text.strip()
        if cleaned_json.startswith("```"):
            cleaned_json = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned_json)
            cleaned_json = re.sub(r"\n?```$", "", cleaned_json).strip()

        return NormalizedProductData.model_validate_json(cleaned_json)

    except Exception as e:
        logger.error(f"Gemini API normalization error: {e}")
        try:
            return _fallback_normalize(raw_data)
        except Exception as fallback_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to normalize product data: {str(fallback_err)}",
            )
