import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

#download cleaned data
df = pd.read_csv('data/daily_sales_cleaned.csv')
df["datum"] = pd.to_datetime(df['datum'])

#Best-selling medicine
target_drug = 'N02BE'
data = df[['datum', target_drug]].copy()
data = data.rename(columns={'datum': 'ds', target_drug: 'y'})

#split data (seperate top 70 row for train and last 30 row for test)
train = data.iloc[:-30]
test = data.iloc[-30:]

#Initialize and train model (AI part)
model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
model.fit(train)

#make prediction
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

#evaluation
predictions = forecast.iloc[-30:]['yhat']
actuals = test['y']

mae = mean_absolute_error(actuals, predictions)
mape = mean_absolute_percentage_error(actuals, predictions)

'''print(f"--- Model Evaluation for {target_drug} ---")
print(f"Mean Absolute Error (MAE): {mae:.2f} units")
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")'''

#simple baseline: moving average (predict: tomorrow = average last 7 days)
''' data['moving_avg'] = data['y'].rolling(window=7).mean()

 plt.figure(figsize=(12,6))
 plt.plot(train['ds'], train['y'], label='Train Data')
 plt.plot(test['ds'], test['y'], label='Actual Test Data', color='green')
 plt.title(f'Sales Forecasting for {target_drug}')
 plt.legend()
 plt.show()'''

#visulization
'''fig1 = model.plot(forecast)
plt.title(f'Prophet Forecast for {target_drug} Sales')
plt.show()

fig2 = model.plot_components(forecast)
plt.show()'''

#Inventory optimization
std_error = (actuals - predictions).std()

z_score = 1.645 #for digital health we want 95%
safety_stock = z_score * std_error

# calculate Re-order Point
# สูตร: (ยอดขายเฉลี่ยที่ AI ทายไว้ * ระยะเวลารอของ) + Safety Stock
# สมมติ Lead Time (ระยะเวลาจากสั่งจนของมาส่ง) = 3 วัน
lead_time = 3
average_forecast = predictions.mean()

reorder_point = (average_forecast * lead_time) + safety_stock

'''print(f"\n--- Inventory Strategy for {target_drug} ---")
print(f"Safety Stock Needed: {safety_stock:.2f} units")
print(f"Re-order Point (ROP): {reorder_point:.2f} units")
print(f"💡 Action: If strock less than {reorder_point:.0f} item. Order now!")

plt.figure(figsize=(12, 5))
plt.plot(test['ds'], actuals, label='Actual Demand', color='black', alpha=0.3)
plt.plot(test['ds'], predictions, label='AI Forecast', color='blue', linestyle='--')
plt.axhline(y=reorder_point, color='red', linestyle='-', label='Re-order Point (ROP)')
plt.fill_between(test['ds'], predictions, reorder_point, color='red', alpha=0.1, label='Buffer Zone')
plt.title(f'AI-Driven Inventory Control for {target_drug}')
plt.legend()
plt.show()'''


drug_cols = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

plt.figure(figsize=(10, 8))
correlation_matrix = df[drug_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")

plt.title('Drug Sales Correlation Analysis')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.show()