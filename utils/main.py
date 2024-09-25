import json
from deeppavlov import build_model, train_model

# Load the configuration from the JSON file
config_path = "ner_onnotes_bert.json"


# Train the model
def train_model_from_config(config_path):
    # Load the configuration
    # with open(config_path, "r", encoding="utf-8") as f:
    #     config = json.load(f)

    # Build and train the model
    model = train_model(config_path)

    return model


if __name__ == "__main__":
    model = train_model_from_config(config_path)
    print("Model training complete.")
