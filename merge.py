import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# List of file paths
file_paths = [
    '/home/cev/project/brake/output.csv',
    '/home/cev/project/handle/turn_speed.csv',
    '/home/cev/project/ultrasound/2023-05-01_08-02-09.csv'
]

# Read the first file to create the initial DataFrame
merged_data = pd.read_csv(file_paths[0])

# Loop through the remaining files and merge them by column
for file_path in file_paths[1:]:
    data = pd.read_csv(file_path)
    merged_data = pd.concat([merged_data, data], axis=1)

# Write the merged data to a new CSV file (optional)
merged_data.to_csv('merged.csv', index=False)

# Assuming the 'label' column is the target variable indicating good (1) or bad (0) driver
# If you don't have this, you'll need to create it based on your criteria
# For example: merged_data['label'] = [1, 0, 1, 0, 1, ...] 

# Features (X) and target (y)
X = merged_data.drop('label', axis=1)  # Drop the target variable from the features
y = merged_data['label']  # Target variable

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = rf_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)
