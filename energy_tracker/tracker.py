import psutil
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetPowerUsage, nvmlShutdown
from codecarbon import EmissionsTracker

class EnergyTracker:
    def __init__(self, gpu_index=0):
        """
        Initialize the EnergyTracker class.
        
        :param gpu_index: Index of the GPU to monitor (default: 0)
        """
        self.gpu_index = gpu_index
        nvmlInit()
        self.gpu_handle = nvmlDeviceGetHandleByIndex(gpu_index)
        self.tracker = EmissionsTracker()
        self.tracker.start()

    def get_cpu_power(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_power = cpu_usage * 0.01 * self.estimate_cpu_power()
        return cpu_power

    def estimate_cpu_power(self):
        return 65.0  # Approximate CPU TDP in Watts

    def get_gpu_power(self):
        power_usage_mw = nvmlDeviceGetPowerUsage(self.gpu_handle)
        return power_usage_mw / 1000  # Convert mW to W

    def get_memory_usage(self):
        mem = psutil.virtual_memory()
        return mem.used / (1024 ** 3)  # Convert to GB

    def log_energy_consumption(self):
        cpu_power = self.get_cpu_power()
        gpu_power = self.get_gpu_power()
        memory_usage = self.get_memory_usage()

        total_power = cpu_power + gpu_power

        print(f"CPU Power: {cpu_power:.2f} W")
        print(f"GPU Power: {gpu_power:.2f} W")
        print(f"Memory Usage: {memory_usage:.2f} GB")
        print(f"Total Power Consumption: {total_power:.2f} W")

    def stop_tracker(self):
        emissions = self.tracker.stop()
        print(f"Estimated CO2 Emissions: {emissions:.4f} kgCO2")

    def shutdown(self):
        nvmlShutdown()