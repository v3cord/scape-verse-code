import os
import numpy as np
import pandas as pd
import lightgbm as lgb
from typing import List

from app.schemas import AnomalyReport, NormalizedProductData
from app.ml.trainer import MODEL_FILE_PATH, train_and_save_model

_booster_cache = None


def get_model() -> lgb.Booster:
    global _booster_cache
    if _booster_cache is not None:
        return _booster_cache

    if not os.path.exists(MODEL_FILE_PATH):
        train_and_save_model(MODEL_FILE_PATH)

    _booster_cache = lgb.Booster(model_file=MODEL_FILE_PATH)
    return _booster_cache


def evaluate_batch_anomalies(
    normalized_batch: List[NormalizedProductData],
) -> List[AnomalyReport]:
    if not normalized_batch:
        return []

    prices = [float(p.price) for p in normalized_batch]
    batch_median = float(np.median(prices)) if prices else 100.0

    bst = get_model()
    now = pd.Timestamp.now()
    features_df = pd.DataFrame(
        [
            {
                "day_of_week": now.dayofweek,
                "day_of_month": now.day,
                "rolling_7d_avg": batch_median,
            }
        ]
    )

    raw_pred = float(bst.predict(features_df)[0])
    scale_factor = batch_median / 145.0 if batch_median > 0 else 1.0
    lgb_expected = round(raw_pred * scale_factor, 2)

    expected_price_baseline = round(batch_median if len(prices) > 1 else lgb_expected, 2)

    reports: List[AnomalyReport] = []

    for item in normalized_batch:
        current_price = round(float(item.price), 2)
        expected_price = expected_price_baseline

        if expected_price > 0:
            price_diff = abs(current_price - expected_price)
            deviation_pct = price_diff / expected_price
        else:
            deviation_pct = 0.0

        is_anomaly = bool(deviation_pct > 0.20)

        if not is_anomaly:
            severity_score = round(min(0.2, (deviation_pct / 0.20) * 0.2), 3)
        else:
            severity_score = round(min(1.0, 0.2 + ((deviation_pct - 0.20) / 0.80) * 0.8), 3)

        reports.append(
            AnomalyReport(
                expected_price=expected_price,
                current_price=current_price,
                is_anomaly=is_anomaly,
                severity_score=severity_score,
            )
        )

    return reports


def evaluate_price_anomaly(normalized_data: NormalizedProductData) -> AnomalyReport:
    return evaluate_batch_anomalies([normalized_data])[0]
