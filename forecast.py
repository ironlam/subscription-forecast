import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from typing import Tuple
import gradio as gr
from gradio.components import Slider, Radio
import os
from PIL import Image

plt.switch_backend('agg')


def read_data(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    data['created_at'] = pd.to_datetime(data['created_at'])
    return data


def prepare_data(data: pd.DataFrame, source: str) -> pd.DataFrame:
    filtered_data = data[data['source'] == source]
    filtered_data['created_at'] = pd.to_datetime(filtered_data['created_at'])
    prepared_data = filtered_data.groupby(
        [filtered_data['created_at'].dt.date, 'subscription_level']).size().reset_index()
    prepared_data.columns = ['ds', 'subscription_level', 'y']
    prepared_data['ds'] = pd.to_datetime(prepared_data['ds'])
    return prepared_data


def forecast_subscriptions(data: pd.DataFrame, periods: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    subscription_levels = data['subscription_level'].unique()
    future_frames = []
    forecast_frames = []

    for level in subscription_levels:
        level_data = data[data['subscription_level'] == level]
        m = Prophet(yearly_seasonality=True, daily_seasonality=False)
        m.fit(level_data)
        future = m.make_future_dataframe(periods=periods)
        future['subscription_level'] = level
        forecast = m.predict(future)
        forecast['subscription_level'] = level

        # Ensure that the subscription counts are greater than or equal to 0
        forecast[['yhat', 'yhat_lower', 'yhat_upper']] = forecast[['yhat', 'yhat_lower', 'yhat_upper']].clip(lower=0)

        future_frames.append(future[['ds', 'subscription_level']])
        forecast_frames.append(forecast[['ds', 'subscription_level', 'yhat', 'yhat_lower', 'yhat_upper']])

    future = pd.concat(future_frames, ignore_index=True)
    forecast = pd.concat(forecast_frames, ignore_index=True)

    return future, forecast


def plot_forecast(prepared_data: pd.DataFrame, future: pd.DataFrame, forecast: pd.DataFrame, source: str) -> plt.Figure:
    subscription_levels = prepared_data['subscription_level'].unique()
    fig, ax = plt.subplots(figsize=(12, 8))

    for level in subscription_levels:
        level_prepared_data = prepared_data[prepared_data['subscription_level'] == level]
        level_future = future[future['subscription_level'] == level]
        level_forecast = forecast[forecast['subscription_level'] == level]

        ax.plot(level_prepared_data['ds'], level_prepared_data['y'], '.', label=f'{level} (actual)')
        ax.plot(level_future['ds'], level_forecast['yhat'], '-', label=f'{level} (forecast)')
        ax.fill_between(level_future['ds'].values, level_forecast['yhat_lower'], level_forecast['yhat_upper'],
                        alpha=0.2)

    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Subscriptions')
    ax.set_title(f'Subscription Forecast for {source}')
    ax.legend()

    # Set the X-axis limits to focus only on the forecasted range
    last_date_in_data = prepared_data['ds'].max()
    ax.set_xlim(last_date_in_data, future['ds'].max())

    plt.tight_layout()

    return fig


def forecast_and_plot(source: str, periods: int = 180) -> Image:
    file_path = os.path.join('dataset', 'subscriptions.csv')
    data = read_data(file_path)
    prepared_data = prepare_data(data, source)
    future, forecast = forecast_subscriptions(prepared_data, periods)
    return plot_forecast(prepared_data, future, forecast, source)


sources = ['Android', 'iOS', 'web']
gr.Interface(
    fn=forecast_and_plot,
    inputs=[
        Radio(sources, label="Source", value="web"),
        Slider(1, 365, 120, label="Days to Forecast")
    ],
    outputs="plot",
    title="Subscription Forecast",
    width=1
).launch()
