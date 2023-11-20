import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load gage height and discharge datasets
gage_height_data = pd.read_csv('data/01302020_2022-11-17T21:55:18.097-05:00_to_2023-11-17T21:55:18.097-05:00_00065_data.tsv', sep='\t')
discharge_data = pd.read_csv('data/01302020_2022-11-17T21:55:18.097-05:00_to_2023-11-17T21:55:18.097-05:00_00060_data.tsv', sep='\t')

# Rename columns before merging
gage_height_data = gage_height_data.rename(columns={'106409_00065': 'Gage_Height'})
discharge_data = discharge_data.rename(columns={'106409_00060': 'Discharge'})

# Merge datasets based on a common column, assuming 'Timestamp' is common
merged_data = pd.merge(gage_height_data, discharge_data, on='datetime', how='inner')

# Define features (gage height and discharge) and target variable (flood)
features = merged_data[['Gage_Height', 'Discharge']]
target = merged_data['Flood']

# Set flood stage threshold (3 feet, adjust as needed)
flood_stage_threshold = 3.0

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize and train the RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

# Print results
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)
