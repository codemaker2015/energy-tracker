"""
EnergyTracker Module

This module provides tools to monitor the energy consumption of computational tasks, 
including CPU and GPU power usage, memory usage, and estimated CO2 emissions.

Dependencies:
- psutil
- pynvml
- codecarbon
"""

import psutil
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetPowerUsage, nvmlShutdown
from codecarbon import EmissionsTracker


class EnergyTracker:
    """
    EnergyTracker class for monitoring energy consumption and CO2 emissions.

    This class uses system monitoring tools (psutil, pynvml) and the CodeCarbon 
    library to track energy usage of CPUs and GPUs, as well as estimate CO2 emissions.
    
    Attributes:
        gpu_index (int): Index of the GPU to monitor.
        tracker (EmissionsTracker): Instance of CodeCarbon's emissions tracker.
        gpu_handle: Handle to the GPU device initialized by NVIDIA Management Library (NVML).
    """

    def __init__(self, gpu_index=0):
        """
        Initialize the EnergyTracker class.
        
        :param gpu_index: Index of the GPU to monitor (default: 0).
        """
        self.gpu_index = gpu_index
        nvmlInit()
        self.gpu_handle = nvmlDeviceGetHandleByIndex(gpu_index)
        self.tracker = EmissionsTracker()
        self.tracker.start()

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
        
        :return: GPU power consumption in Watts.
        """
        power_usage_mw = nvmlDeviceGetPowerUsage(self.gpu_handle)
        return power_usage_mw / 1000  # Convert mW to W

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
        print(f"Estimated CO2 Emissions: {emissions:.4f} kgCO2")

    def shutdown(self):
        """
        Shutdown the NVML (NVIDIA Management Library) for GPU monitoring.
        """
        nvmlShutdown()
