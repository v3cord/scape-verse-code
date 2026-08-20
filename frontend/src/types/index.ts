export interface RawPriceInfo {
  value?: number;
  currency?: string;
  symbol?: string;
}

export interface RawInputInfo {
  url?: string;
}

export interface RawProductData {
  product_name?: string;
  price?: RawPriceInfo | number | string;
  description?: string;
  image_url?: string;
  availability?: string;
  input?: RawInputInfo;
}

export interface NormalizedProductData {
  product_name: string;
  price: number;
  is_in_stock: boolean;
  currency: string;
  description?: string | null;
  image_url?: string | null;
  url?: string | null;
}

export interface AnomalyReport {
  expected_price: number;
  current_price: number;
  is_anomaly: boolean;
  severity_score: number;
}

export interface FinalAnalysisResponse {
  product_data: NormalizedProductData;
  anomaly_report: AnomalyReport;
}
