# Energy Tracker

A Python package to track energy consumption and CO2 emissions for LLM models and other computational tasks. The package provides tools to track power usage of both CPU and GPU, as well as track system memory usage. It also estimates CO2 emissions based on energy consumption.

## Features

- tracks CPU power usage
- tracks GPU power usage (NVIDIA GPUs only)
- tracks memory usage
- Estimates CO2 emissions based on energy consumption

## Installation

You can install the package using pip:

```bash
pip install energy-tracker
```
## Usage

You can use the EnergyTracker class to start tracking energy consumption and CO2 emissions:

### Simple Usage
```python
from energy_tracker import EnergyTracker

# Initialize the energy tracker
tracker = EnergyTracker()

# Log energy consumption data
tracker.log_energy_consumption()

# Stop the emissions tracker and get CO2 emissions
tracker.stop_tracker()

# Shutdown the tracker
tracker.shutdown()
```

### LLM Usage
```py
from transformers import pipeline
from energy_tracker.tracker import EnergyTracker

# Load LLM
llm = pipeline("text-generation", model="gpt2")

# Initialize energy tracker
tracker = EnergyTracker()

try:
    # Tracks energy during inference
    print("Running LLM inference...")
    tracker.log_energy_consumption()
    result = llm("What is the capital of France?", max_length=10)
    print(result)
    tracker.log_energy_consumption()
finally:
    tracker.shutdown()
```

## Requirements

- Python 3.6+
- psutil
- pynvml (for NVIDIA GPU monitoring)
- codecarbon (for CO2 emissions tracking)