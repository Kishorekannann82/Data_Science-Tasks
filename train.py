from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
X, y = load_breast_cancer(return_X_y=True)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    min_samples_split=2,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved successfully!")