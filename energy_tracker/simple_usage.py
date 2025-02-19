from energy_tracker.tracker import EnergyTracker

# Initialize the energy tracker
tracker = EnergyTracker()

# Log energy consumption data
tracker.log_energy_consumption()

# Stop the emissions tracker and get CO2 emissions
tracker.stop_tracker()

# Shutdown the tracker
tracker.shutdown()