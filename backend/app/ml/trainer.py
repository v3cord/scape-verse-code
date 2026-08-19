import os
import numpy as np
import pandas as pd
import lightgbm as lgb

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE_PATH = os.path.join(MODEL_DIR, "lgbm_model.txt")


def generate_synthetic_data(num_days: int = 30, base_price: float = 145.0) -> pd.DataFrame:
    """Generates 30 days of synthetic pricing data with seasonality and noise."""
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=num_days, freq="D")
    
    # Seasonality: higher price on weekends (days 5 & 6)
    seasonality = np.sin(dates.dayofweek * (2 * np.pi / 7)) * 3.5
    noise = np.random.normal(0, 1.5, size=num_days)
    
    prices = base_price + seasonality + noise
    
    df = pd.DataFrame({"date": dates, "price": prices})
    
    # Feature engineering: day_of_week, day_of_month, and 7-day rolling average
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_month"] = df["date"].dt.day
    df["rolling_7d_avg"] = df["price"].rolling(window=7, min_periods=1).mean()
    
    return df


def train_and_save_model(output_path: str = MODEL_FILE_PATH) -> str:
    """Trains LightGBM regressor on synthetic historical price features and saves model file."""
    df = generate_synthetic_data(num_days=60, base_price=145.0)
    
    feature_cols = ["day_of_week", "day_of_month", "rolling_7d_avg"]
    X = df[feature_cols]
    y = df["price"]
    
    train_data = lgb.Dataset(X, label=y)
    params = {
        "objective": "regression",
        "metric": "rmse",
        "learning_rate": 0.05,
        "num_leaves": 15,
        "verbose": -1,
        "seed": 42,
    }
    
    model = lgb.train(params, train_data, num_boost_round=50)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    model.save_model(output_path)
    print(f"Successfully trained LightGBM model and saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    train_and_save_model()
