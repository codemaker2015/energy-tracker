import psutil
from codecarbon import EmissionsTracker

try:
    from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetPowerUsage, nvmlShutdown
    NVML_AVAILABLE = True
except (ImportError, FileNotFoundError):
    NVML_AVAILABLE = False


class EnergyTracker:
    """
    EnergyTracker class for monitoring energy consumption and CO2 emissions.

    This class uses system monitoring tools (psutil, pynvml) and the CodeCarbon 
    library to track energy usage of CPUs and GPUs, as well as estimate CO2 emissions.
    """

    def __init__(self, gpu_index=0):
        """
        Initialize the EnergyTracker class.
        
        :param gpu_index: Index of the GPU to monitor (default: 0).
        """
        global NVML_AVAILABLE  # Ensure we refer to the global variable
        self.gpu_index = gpu_index
        self.tracker = EmissionsTracker()
        self.tracker.start()

        if NVML_AVAILABLE:
            try:
                nvmlInit()
                self.gpu_handle = nvmlDeviceGetHandleByIndex(gpu_index)
            except Exception as e:
                print(f"Warning: Failed to initialize NVML. GPU tracking disabled. Error: {e}")
                NVML_AVAILABLE = False  # Disable GPU tracking if initialization fails
        else:
            print("NVML is not available. GPU tracking will be disabled.")

    def get_cpu_power(self):
        """
        Get the estimated power consumption of the CPU in Watts.
        
        :return: CPU power consumption in Watts.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_power = cpu_usage * 0.01 * self.estimate_cpu_power()
        return cpu_power

    def estimate_cpu_power(self):
        """
        Estimate the power consumption of the CPU based on its TDP.
        
        :return: Approximate CPU TDP in Watts.
        """
        return 65.0  # Approximate CPU TDP in Watts

    def get_gpu_power(self):
        """
        Get the power consumption of the GPU in Watts.
        
        :return: GPU power consumption in Watts, or 0 if NVML is unavailable.
        """
        if NVML_AVAILABLE:
            try:
                power_usage_mw = nvmlDeviceGetPowerUsage(self.gpu_handle)
                return power_usage_mw / 1000  # Convert mW to W
            except Exception as e:
                print(f"Warning: Failed to get GPU power usage. Error: {e}")
                return 0.0
        return 0.0

    def get_memory_usage(self):
        """
        Get the current memory usage in gigabytes (GB).
        
        :return: Memory usage in GB.
        """
        mem = psutil.virtual_memory()
        return mem.used / (1024 ** 3)  # Convert to GB

    def log_energy_consumption(self):
        """
        Log the energy consumption details including CPU and GPU power,
        memory usage, and total power consumption.
        """
        cpu_power = self.get_cpu_power()
        gpu_power = self.get_gpu_power()
        memory_usage = self.get_memory_usage()

        total_power = cpu_power + gpu_power

        print(f"CPU Power: {cpu_power:.2f} W")
        print(f"GPU Power: {gpu_power:.2f} W")
        print(f"Memory Usage: {memory_usage:.2f} GB")
        print(f"Total Power Consumption: {total_power:.2f} W")

    def stop_tracker(self):
        """
        Stop the CO2 emissions tracker and print the estimated emissions.
        """
        emissions = self.tracker.stop()

        # Environmental equivalence calculations
        trees_needed = emissions / 0.057  # One tree absorbs ~0.057 kg CO2 per day
        cycling_km = emissions / 0.251  # Cycling avoids 0.251 kg CO2 per km
        public_transport_km = emissions / 0.18  # Public transport saves 0.18 kg CO2 per km
        internet_free_hours = emissions / 0.06  # One hour of internet emits 0.06 kg CO2

        print(f"Estimated CO2 Emissions: {emissions:.4f} kgCO2")

        if any(val >= 0.1 for val in [trees_needed, cycling_km, public_transport_km, internet_free_hours]):
            print("To offset this, you could:")
            if trees_needed >= 0.1:
                print(f"- Let {trees_needed:.2f} trees absorb CO2 for a day 🌳")
            if cycling_km >= 0.1:
                print(f"- Cycle for {cycling_km:.2f} km instead of driving 🚴")
            if public_transport_km >= 0.1:
                print(f"- Take public transport for {public_transport_km:.2f} km instead of driving 🚆")
            if internet_free_hours >= 0.1:
                print(f"- Stay offline for {internet_free_hours:.2f} hours 📵")

    def shutdown(self):
        """
        Shutdown the NVML (NVIDIA Management Library) for GPU monitoring.
        """
        if NVML_AVAILABLE:
            try:
                nvmlShutdown()
            except Exception as e:
                print(f"Warning: Failed to shut down NVML. Error: {e}")
