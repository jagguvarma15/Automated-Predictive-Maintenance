# Variables
PYTHON = /home/codespace/.python/current/bin/python
DATA_DIR = /workspaces/Automated-Predictive-Maintenance/data
RAW_DATA = $(DATA_DIR)/raw/MetroPT3(AirCompressor).csv
PROCESSED_DATA = $(DATA_DIR)/processed/MetroPT3_cleaned.parquet
MODEL_DIR = /workspaces/Automated-Predictive-Maintenance/models
MODEL_FILE = $(MODEL_DIR)/xgboost_model.json
ALERTS_FILE = /workspaces/Automated-Predictive-Maintenance/alerts/alerts.txt

# Default target
.PHONY: all
all: ingestion etl train_model inference alert

# Step 1: Ingest raw data
.PHONY: ingestion
ingestion:
	@echo "Running data ingestion..."
	$(PYTHON) scripts/ingestion.py

# Step 2: Run ETL
.PHONY: etl
etl: $(RAW_DATA)
	@echo "Running ETL to process raw data..."
	$(PYTHON) scripts/etl.py

# Step 3: Train the model
.PHONY: train_model
train_model: $(PROCESSED_DATA)
	@echo "Training the model..."
	$(PYTHON) scripts/train_script.py

# Step 4: Run training process
.PHONY: training
training: $(MODEL_FILE)
	@echo "Running training process..."
	$(PYTHON) scripts/training.py

# Step 5: Run inference and log alert
.PHONY: inference
inference: $(MODEL_FILE)
	@echo "Running inference..."
	@echo "Generating alerts..."
	$(PYTHON) scripts/inference.py

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning up generated files..."
	rm -rf $(MODEL_DIR)/*.json $(ALERTS_FILE)
	@echo "Cleaned up!"
