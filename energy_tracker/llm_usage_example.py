"""
LLM Inference with Energy Tracking

This script demonstrates how to monitor energy consumption and CO2 emissions 
while performing inference using a large language model (LLM). 

The script uses:
- `transformers` library for loading and running an LLM.
- `EnergyTracker` from the `energy_tracker` package to monitor CPU and GPU power usage 
  and track CO2 emissions during the LLM inference process.
"""

from transformers import pipeline
from energy_tracker.tracker import EnergyTracker

# Load LLM
llm = pipeline("text-generation", model="gpt2")

# Initialize energy tracker
tracker = EnergyTracker()

try:
    # Monitor energy during inference
    print("Running LLM inference...")
    tracker.log_energy_consumption()
    result = llm("What is the capital of France?", max_length=10)
    print(result)
    tracker.log_energy_consumption()
finally:
    tracker.shutdown()
