from typing import Optional, Union
from pydantic import BaseModel, Field


class RawPriceInfo(BaseModel):
    value: Optional[float] = Field(default=None, description="Numerical price value")
    currency: Optional[str] = Field(default=None, description="Currency string (e.g., USD)")
    symbol: Optional[str] = Field(default=None, description="Currency symbol (e.g., $)")


class RawInputInfo(BaseModel):
    url: Optional[str] = Field(default=None, description="Target product URL")


class RawProductData(BaseModel):
    product_name: Optional[str] = Field(default=None, description="Raw product title/name")
    price: Optional[Union[RawPriceInfo, float, str]] = Field(
        default=None, description="Raw price as nested object, float, or string"
    )
    description: Optional[str] = Field(default=None, description="Raw product description text")
    image_url: Optional[str] = Field(default=None, description="Raw image URL string")
    availability: Optional[str] = Field(
        default=None, description="Raw stock availability string (e.g. 'In Stock')"
    )
    input: Optional[RawInputInfo] = Field(default=None, description="Raw request input details")


class NormalizedProductData(BaseModel):
    product_name: str = Field(..., description="Cleaned product title")
    price: float = Field(..., description="Strict float representation of product price")
    is_in_stock: bool = Field(
        ..., description="Strict boolean indicating whether product is in stock"
    )
    currency: str = Field(default="USD", description="Standardized currency code (e.g., USD)")
    description: Optional[str] = Field(default=None, description="Cleaned product description")
    image_url: Optional[str] = Field(default=None, description="Cleaned product image URL")
    url: Optional[str] = Field(default=None, description="Product canonical URL")


class AnomalyReport(BaseModel):
    expected_price: float = Field(..., description="ML predicted expected market price")
    current_price: float = Field(..., description="Actual current price from scraped data")
    is_anomaly: bool = Field(..., description="Flag indicating if price deviates by >15%")
    severity_score: float = Field(
        ..., description="Anomaly severity score scaled between 0.0 and 1.0"
    )


class FinalAnalysisResponse(BaseModel):
    product_data: NormalizedProductData = Field(..., description="Normalized product details")
    anomaly_report: AnomalyReport = Field(..., description="LightGBM price anomaly evaluation")
