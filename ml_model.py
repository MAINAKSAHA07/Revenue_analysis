import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

conn = psycopg2.connect(
    dbname="revenue_analysis",
    user="adminuser",
    password="SecurePassword123!",
    host="revenue-analysis-db.postgres.database.azure.com",
    port="5432"
)

query = "SELECT * FROM predictions"
df = pd.read_sql(query, conn)
conn.close()

print(df.head())

X = df[['predicted_demand', 'refund_amount']]
y = df['actual_revenue']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred_complete = model.predict(X)
y_pred_test = model.predict(X_test)

mse_complete = mean_squared_error(y, y_pred_complete)
rmse_complete = mse_complete ** 0.5
r2_complete = r2_score(y, y_pred_complete)

# Evaluate on test set for comparison
mse_test = mean_squared_error(y_test, y_pred_test)
rmse_test = mse_test ** 0.5
r2_test = r2_score(y_test, y_pred_test)

print(f"Complete Dataset Metrics:")
print(f"RMSE: {rmse_complete:.2f}")
print(f"R²: {r2_complete:.2f}")
print(f"\nTest Set Metrics:")
print(f"RMSE: {rmse_test:.2f}")
print(f"R²: {r2_test:.2f}")

plt.figure(figsize=(12, 6))

# Plot actual vs predicted values for complete dataset
plt.scatter(y, y_pred_complete, alpha=0.5, color='blue', label='Actual vs Predicted')

# Plot refund points in red
refund_points = df[df['refund_amount'] > 0]
plt.scatter(refund_points['actual_revenue'], 
           refund_points['predicted_demand'] - refund_points['refund_amount'],
           color='red', 
           alpha=0.7, 
           label='Refund Points')

# Add perfect prediction line
min_val = min(y.min(), y_pred_complete.min())
max_val = max(y.max(), y_pred_complete.max())
plt.plot([min_val, max_val], [min_val, max_val], 'k--', label='Perfect Prediction')

plt.xlabel('Actual Revenue')
plt.ylabel('Predicted Revenue')
plt.title('Actual vs Predicted Revenue (Complete Dataset)')
plt.legend()

# Add metrics annotations
metrics_text = f'Complete Dataset:\nRMSE: {rmse_complete:.2f}\nR²: {r2_complete:.2f}\n\n'
metrics_text += f'Test Set:\nRMSE: {rmse_test:.2f}\nR²: {r2_test:.2f}'
plt.annotate(metrics_text, 
            xy=(0.05, 0.95), 
            xycoords='axes fraction', 
            bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('revenue_prediction_complete.png')
plt.close()

results_df = pd.DataFrame({
    'Actual_Revenue': y,
    'Predicted_Revenue': y_pred_complete,
    'Refund_Amount': df['refund_amount'],
    'Predicted_Demand': df['predicted_demand']
})
results_df.to_csv('results_complete.csv', index=False)
print("\nComplete results saved to 'results_complete.csv'")

conn = psycopg2.connect(
    dbname="revenue_analysis",
    user="adminuser",
    password="SecurePassword123!",
    host="revenue-analysis-db.postgres.database.azure.com",
    port="5432"
)
cursor = conn.cursor()

# Example correction logic (if predicted value deviates by more than 5%)
for idx, row in results_df.iterrows():
    if abs(row['Actual_Revenue'] - row['Predicted_Revenue']) / row['Actual_Revenue'] > 0.05:
        corrected_value = float(row['Predicted_Revenue'])  # Convert to float to avoid numpy type issues
        cursor.execute(
            "UPDATE predictions SET actual_revenue = %s WHERE id = %s",
            (corrected_value, idx + 1)  # Using index + 1 as database ID
        )

conn.commit()
conn.close()
print("\nDatabase updated with corrected values!")
