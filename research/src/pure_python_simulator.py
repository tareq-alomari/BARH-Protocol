"""
Pure Python Network Simulator - No External Dependencies
"""

import time
import random
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from collections import deque

@dataclass
class NetworkMetrics:
    latency: float
    packet_loss: float
    throughput: float
    jitter: float
    timestamp: float
    network_type: str

@dataclass
class NetworkCondition:
    base_latency: float
    latency_variance: float
    base_packet_loss: float
    loss_variance: float
    base_throughput: float
    throughput_variance: float
    instability_factor: float
    network_type: str

class PurePythonNetworkSimulator:
    """Pure Python network simulator"""
    
    def __init__(self):
        self.current_condition = None
        self.time_start = time.time()
        self.interference_events = []
        self.congestion_events = []
        
        # Define network conditions
        self.network_conditions = {
            'wifi_optimal': NetworkCondition(5.0, 1.0, 0.1, 0.05, 100.0, 10.0, 0.1, 'WiFi'),
            'wifi_congested': NetworkCondition(15.0, 8.0, 2.0, 1.0, 60.0, 20.0, 0.4, 'WiFi'),
            'lte_good': NetworkCondition(20.0, 5.0, 0.5, 0.2, 80.0, 15.0, 0.2, '4G LTE'),
            'lte_poor': NetworkCondition(45.0, 15.0, 3.0, 2.0, 30.0, 10.0, 0.6, '4G LTE'),
            '5g_excellent': NetworkCondition(3.0, 0.5, 0.05, 0.02, 150.0, 20.0, 0.05, '5G'),
            '6g_simulation': NetworkCondition(1.0, 0.2, 0.01, 0.005, 300.0, 50.0, 0.02, '6G'),
            'extreme_conditions': NetworkCondition(100.0, 50.0, 8.0, 3.0, 20.0, 5.0, 0.9, 'Poor')
        }
        
        self.set_condition('wifi_optimal')
    
    def set_condition(self, condition_name: str):
        """Set network condition"""
        if condition_name in self.network_conditions:
            self.current_condition = self.network_conditions[condition_name]
        
    def add_interference_event(self, start_time: float, duration: float, intensity: float):
        """Add interference event"""
        self.interference_events.append({
            'start': start_time,
            'end': start_time + duration,
            'intensity': intensity
        })
    
    def add_congestion_event(self, start_time: float, duration: float, severity: float):
        """Add congestion event"""
        self.congestion_events.append({
            'start': start_time,
            'end': start_time + duration,
            'severity': severity
        })
    
    def _get_current_interference(self) -> float:
        """Calculate current interference level"""
        current_time = time.time() - self.time_start
        interference = 0.0
        
        for event in self.interference_events:
            if event['start'] <= current_time <= event['end']:
                interference += event['intensity']
        
        return min(interference, 1.0)
    
    def _get_current_congestion(self) -> float:
        """Calculate current congestion level"""
        current_time = time.time() - self.time_start
        congestion = 0.0
        
        for event in self.congestion_events:
            if event['start'] <= current_time <= event['end']:
                congestion += event['severity']
        
        return min(congestion, 1.0)
    
    def get_current_metrics(self) -> NetworkMetrics:
        """Generate current network metrics"""
        if not self.current_condition:
            return NetworkMetrics(0, 0, 0, 0, time.time(), 'Unknown')
        
        condition = self.current_condition
        
        # Generate random variations using Box-Muller transform
        def normal_random(mean: float, std: float) -> float:
            u1 = random.random()
            u2 = random.random()
            z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            return mean + z * std
        
        # Base metrics with variations
        latency = max(0.1, normal_random(condition.base_latency, condition.latency_variance))
        packet_loss = max(0.0, min(100.0, normal_random(condition.base_packet_loss, condition.loss_variance)))
        throughput = max(1.0, normal_random(condition.base_throughput, condition.throughput_variance))
        jitter = abs(normal_random(0, condition.latency_variance * 0.5))
        
        # Apply environmental factors
        interference = self._get_current_interference()
        congestion = self._get_current_congestion()
        
        # Apply interference effects
        if interference > 0:
            latency *= (1 + interference * 2)
            packet_loss += interference * 5
            throughput *= (1 - interference * 0.5)
        
        # Apply congestion effects
        if congestion > 0:
            latency *= (1 + congestion * 3)
            packet_loss += congestion * 8
            throughput *= (1 - congestion * 0.7)
        
        # Add instability spikes
        if random.random() < condition.instability_factor:
            spike_factor = random.uniform(1.5, 3.0)
            latency *= spike_factor
            packet_loss *= spike_factor
            throughput *= (1.0 / spike_factor)
        
        # Ensure realistic bounds
        latency = max(0.1, min(5000.0, latency))
        packet_loss = max(0.0, min(100.0, packet_loss))
        throughput = max(0.1, min(1000.0, throughput))
        jitter = max(0.0, min(latency * 0.5, jitter))
        
        return NetworkMetrics(
            latency=latency,
            packet_loss=packet_loss,
            throughput=throughput,
            jitter=jitter,
            timestamp=time.time(),
            network_type=condition.network_type
        )
    
    def simulate_scenario(self, scenario_name: str, duration: float = 60.0):
        """Simulate specific network scenarios"""
        if scenario_name == "stable_baseline":
            self.set_condition('wifi_optimal')
            
        elif scenario_name == "sudden_congestion":
            self.set_condition('wifi_optimal')
            self.add_congestion_event(5.0, 10.0, 0.8)
            
        elif scenario_name == "intermittent_loss":
            self.set_condition('lte_good')
            for i in range(3):
                start_time = random.uniform(2.0, duration - 5.0)
                self.add_interference_event(start_time, 3.0, 0.7)
                
        elif scenario_name == "6g_simulation":
            self.set_condition('6g_simulation')
            
        elif scenario_name == "extreme_conditions":
            self.set_condition('extreme_conditions')
            self.add_interference_event(2.0, 15.0, 0.9)
            self.add_congestion_event(8.0, 20.0, 0.8)
    
    def reset_events(self):
        """Reset all events"""
        self.interference_events.clear()
        self.congestion_events.clear()
        self.time_start = time.time()
