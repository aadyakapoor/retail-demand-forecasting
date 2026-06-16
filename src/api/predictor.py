import pickle
import pandas as pd
import numpy as np
import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

class DemandPredictor:
    def __init__(self):
        model_path = os.path.join(
            BASE_DIR,
            'src',
            'models',
            'lgbm_best.pkl'
        )

        features_path = os.path.join(
            BASE_DIR,
            'src',
            'models',
            'feature_cols.json'
        )

        data_path = os.path.join(
            BASE_DIR,
            'data',
            'latest_per_item.csv'
        )

        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

        with open(features_path, 'r') as f:
            self.feature_cols = json.load(f)

        self.df = pd.read_csv(
            data_path,
            parse_dates=['date']
        )

        print(
            f"Predictor loaded. "
            f"{len(self.feature_cols)} features. "
            f"{self.df['id'].nunique()} items available."
        )

    def get_available_items(self):
        return sorted(
            self.df['id'].unique().tolist()
        )

    def predict(self, item_id: str, horizon: int = 28):

        if item_id not in self.df['id'].values:
            raise ValueError(
                f"item_id '{item_id}' not found in dataset"
            )

        item_history = (
            self.df[self.df['id'] == item_id]
            .sort_values('date')
        )

        # if len(item_history) < 28:
        #     raise ValueError(
        #         f"Not enough history for item_id '{item_id}'"
        #     )

        last_date = item_history['date'].max()
        latest_row = item_history.iloc[-1]

        forecasts = []

        for day_ahead in range(1, horizon + 1):

            future_date = (
                last_date +
                pd.Timedelta(days=day_ahead)
            )

            row = latest_row[self.feature_cols].copy()

            row['day_of_week'] = future_date.dayofweek
            row['day_of_month'] = future_date.day
            row['week_of_year'] = future_date.isocalendar()[1]
            row['month'] = future_date.month
            row['year'] = future_date.year
            row['is_weekend'] = int(
                future_date.dayofweek >= 5
            )

            X = pd.DataFrame([row])[self.feature_cols]

            pred = float(
                np.clip(
                    self.model.predict(X)[0],
                    0,
                    None
                )
            )

            forecasts.append({
                "date": future_date.strftime("%Y-%m-%d"),
                "predicted_sales": round(pred, 2)
            })

        return forecasts


predictor = DemandPredictor()