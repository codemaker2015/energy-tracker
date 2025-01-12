if __name__ == "__main__":
    from energy_tracker.tracker import EnergyTracker
    
    tracker = EnergyTracker()
    try:
        print("Starting energy tracking...")
        tracker.log_energy_consumption()
    finally:
        tracker.stop_tracker()
        tracker.shutdown()
