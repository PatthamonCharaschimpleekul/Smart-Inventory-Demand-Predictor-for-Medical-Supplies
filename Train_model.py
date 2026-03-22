import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import joblib

# Load cleaned data
df = pd.read_csv('data/daily_sales_cleaned.csv')
df["datum"] = pd.to_datetime(df['datum'])

# Best-selling medicines selected for prototype
target_drugs = ['N02BE', 'N05B', 'R03']

# Start Loop for Multi-Drug Training
for drug in target_drugs:
    print(f"\n🚀 Training Model for: {drug}")
    
    # Prepare data for Prophet
    data = df[['datum', drug]].copy()
    data = data.rename(columns={'datum': 'ds', drug: 'y'})

    # Split data (top rows for train and last 30 rows for test)
    train = data.iloc[:-30]
    test = data.iloc[-30:]

    # Initialize and train model (AI part)
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(train)

    # Make prediction
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Evaluation
    predictions = forecast.iloc[-30:]['yhat']
    actuals = test['y']

    mae = mean_absolute_error(actuals, predictions)
    mape = mean_absolute_percentage_error(actuals, predictions)

    print(f"--- Model Evaluation for {drug} ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f} units")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

    # [ORIGINAL COMMENTS KEPT FOR DOCUMENTATION]
    # simple baseline: moving average (predict: tomorrow = average last 7 days)
    ''' data['moving_avg'] = data['y'].rolling(window=7).mean()

    plt.figure(figsize=(12,6))
    plt.plot(train['ds'], train['y'], label='Train Data')
    plt.plot(test['ds'], test['y'], label='Actual Test Data', color='green')
    plt.title(f'Sales Forecasting for {drug}')
    plt.legend()
    plt.show()'''

    # visualization
    '''fig1 = model.plot(forecast)
    plt.title(f'Prophet Forecast for {drug} Sales')
    plt.show()

    fig2 = model.plot_components(forecast)
    plt.show()'''

    # Inventory optimization
    std_error = (actuals - predictions).std()
    z_score = 1.645 # 95% Confidence Level for Digital Health
    safety_stock = z_score * std_error

    # Re-order Point Calculation
    # Formula: (Avg Forecasted Demand * Lead Time) + Safety Stock
    # Assuming Lead Time = 3 days
    lead_time = 3
    average_forecast = predictions.mean()
    reorder_point = (average_forecast * lead_time) + safety_stock

    # [ORIGINAL COMMENTS KEPT FOR DOCUMENTATION]
    '''print(f"\n--- Inventory Strategy for {drug} ---")
    print(f"Safety Stock Needed: {safety_stock:.2f} units")
    print(f"Re-order Point (ROP): {reorder_point:.2f} units")
    print(f"💡 Action: If stock is less than {reorder_point:.0f} units, order now!")

    plt.figure(figsize=(12, 5))
    plt.plot(test['ds'], actuals, label='Actual Demand', color='black', alpha=0.3)
    plt.plot(test['ds'], predictions, label='AI Forecast', color='blue', linestyle='--')
    plt.axhline(y=reorder_point, color='red', linestyle='-', label='Re-order Point (ROP)')
    plt.fill_between(test['ds'], predictions, reorder_point, color='red', alpha=0.1, label='Buffer Zone')
    plt.title(f'AI-Driven Inventory Control for {drug}')
    plt.legend()
    plt.show()'''

    # Save individual Prophet models for each drug
    model_filename = f'prophet_model_{drug.lower()}.pkl'
    joblib.dump(model, model_filename)
    print(f"✅ Success: '{model_filename}' has been created!")

# --- Correlation Analysis (Run once after the loop) ---
drug_cols = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

plt.figure(figsize=(10, 8))
correlation_matrix = df[drug_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")

plt.title('Drug Sales Correlation Analysis')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.show()

print("\n🏁 Process Complete: All models trained and saved successfully.")