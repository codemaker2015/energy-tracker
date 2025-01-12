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
