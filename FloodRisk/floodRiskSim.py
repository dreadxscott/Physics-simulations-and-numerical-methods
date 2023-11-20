import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Sample data (replace with your actual data)
data = {
    'Date': pd.date_range(start='2023-01-01', end='2023-12-31', freq='D'),
    'Gage_Height': np.random.uniform(5, 15, 365),
    'Discharge': np.random.uniform(20, 100, 365),
    'Historical_Flood': np.random.choice([0, 1], size=365, p=[0.9, 0.1])
}

df = pd.DataFrame(data)
df.set_index('Date', inplace=True)

# Feature engineering
df['Max_Gage_Height'] = df['Gage_Height'].rolling(window=7).max()  # 7-day max gage height
df['Max_Discharge'] = df['Discharge'].rolling(window=7).max()  # 7-day max discharge

# Train-test split
train_size = int(0.8 * len(df))
train, test = df.iloc[:train_size], df.iloc[train_size:]

# Linear regression model
features = ['Max_Gage_Height', 'Max_Discharge']
target = 'Historical_Flood'

X_train, y_train = train[features].values, train[target].values
X_test, y_test = test[features].values, test[target].values

model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

# Evaluation
train_rmse = np.sqrt(mean_squared_error(y_train, train_predictions))
test_rmse = np.sqrt(mean_squared_error(y_test, test_predictions))

print(f'Train RMSE: {train_rmse:.2f}')
print(f'Test RMSE: {test_rmse:.2f}')

# Visualization
plt.figure(figsize=(10, 5))

plt.plot(df.index[:train_size], y_train, label='Train (Actual)', color='blue')
plt.plot(df.index[train_size:], y_test, label='Test (Actual)', color='green')
plt.plot(df.index[:train_size], train_predictions, label='Train (Predicted)', linestyle='dashed', color='red')
plt.plot(df.index[train_size:], test_predictions, label='Test (Predicted)', linestyle='dashed', color='orange')

plt.title('Historical Flood Prediction')
plt.xlabel('Date')
plt.ylabel('Historical Flood (0: No Flood, 1: Flood)')
plt.legend()
plt.show()
