from typing import Any, Dict, List, Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    AnomalyReport,
    FinalAnalysisResponse,
    NormalizedProductData,
    RawProductData,
)
from app.services.normalizer import normalize_product_data
from app.ml.inference import evaluate_batch_anomalies
from app.scraper.webhook import run_discovery_scraper, run_extraction_scraper

app = FastAPI(
    title="Market Sentinel API",
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "online", "service": "Market Sentinel API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/ingest", response_model=Union[List[NormalizedProductData], NormalizedProductData])
async def ingest_product(
    raw_data: Union[List[RawProductData], RawProductData]
) -> Union[List[NormalizedProductData], NormalizedProductData]:
    try:
        if isinstance(raw_data, list):
            results = []
            for item in raw_data:
                norm = await normalize_product_data(item)
                results.append(norm)
            return results
        else:
            return await normalize_product_data(raw_data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Data ingestion failed: {str(e)}"
        )


@app.post("/api/analyze", response_model=List[FinalAnalysisResponse])
async def analyze_products(
    raw_data: Union[List[RawProductData], RawProductData]
) -> List[FinalAnalysisResponse]:
    try:
        items_to_process: List[RawProductData] = (
            raw_data if isinstance(raw_data, list) else [raw_data]
        )

        normalized_batch: List[NormalizedProductData] = []
        for item in items_to_process:
            norm = await normalize_product_data(item)
            normalized_batch.append(norm)

        anomaly_reports: List[AnomalyReport] = evaluate_batch_anomalies(normalized_batch)

        results: List[FinalAnalysisResponse] = []
        for norm_item, report in zip(normalized_batch, anomaly_reports):
            results.append(
                FinalAnalysisResponse(
                    product_data=norm_item,
                    anomaly_report=report,
                )
            )

        return results
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Analysis failed: {str(e)}"
        )


@app.post("/api/scraper/chain")
async def trigger_chained_scraper(payload: Dict[str, str]) -> Dict[str, Any]:
    search_url = payload.get(
        "search_url", "https://shopalto.xyz/search?q=headphones"
    )

    try:
        discovered_urls = run_discovery_scraper(search_url)
        extracted_data = run_extraction_scraper(discovered_urls)

        return {
            "status": "success",
            "discovery_collector_id": "c_msxihjnheicz27x5n",
            "extraction_collector_id": "c_msxfmm4911y5zyk7sq",
            "discovered_urls": discovered_urls,
            "extracted_data": extracted_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Scraper execution failed: {str(e)}"
        )
