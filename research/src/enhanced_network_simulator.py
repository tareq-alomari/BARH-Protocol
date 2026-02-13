"""
Enhanced Network Simulator with Advanced Scenarios
Supports 6G simulation, AI workloads, and extreme conditions
"""

import numpy as np
import time
import random
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enhanced_barh_protocol import NetworkMetrics

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

class EnhancedNetworkSimulator:
    """Advanced network simulator with realistic conditions"""
    
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
            '5g_variable': NetworkCondition(8.0, 12.0, 0.8, 0.5, 120.0, 40.0, 0.3, '5G'),
            '6g_simulation': NetworkCondition(1.0, 0.2, 0.01, 0.005, 300.0, 50.0, 0.02, '6G'),
            'satellite': NetworkCondition(600.0, 100.0, 1.0, 0.5, 25.0, 5.0, 0.8, 'Satellite'),
            'edge_computing': NetworkCondition(2.0, 0.3, 0.02, 0.01, 200.0, 30.0, 0.03, 'Edge')
        }
        
        self.set_condition('wifi_optimal')
    
    def set_condition(self, condition_name: str):
        """Set network condition"""
        if condition_name in self.network_conditions:
            self.current_condition = self.network_conditions[condition_name]
            print(f"Network condition set to: {condition_name}")
        else:
            print(f"Unknown condition: {condition_name}")
    
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
    
    def _simulate_handoff_event(self) -> float:
        """Simulate network handoff with temporary degradation"""
        if random.random() < 0.001:  # 0.1% chance per measurement
            return random.uniform(2.0, 5.0)  # Handoff penalty
        return 1.0
    
    def _simulate_burst_loss(self) -> float:
        """Simulate burst packet loss events"""
        if random.random() < 0.005:  # 0.5% chance of burst loss
            return random.uniform(5.0, 15.0)  # Burst loss percentage
        return 0.0
    
    def _simulate_thermal_throttling(self) -> float:
        """Simulate device thermal throttling effects"""
        current_time = time.time() - self.time_start
        # Simulate gradual performance degradation over time
        if current_time > 300:  # After 5 minutes
            throttling_factor = min((current_time - 300) / 1800, 0.3)  # Up to 30% degradation
            return 1.0 + throttling_factor
        return 1.0
    
    def get_current_metrics(self) -> NetworkMetrics:
        """Generate current network metrics with realistic variations"""
        if not self.current_condition:
            return NetworkMetrics(0, 0, 0, 0, time.time(), 'Unknown')
        
        # Base metrics from condition
        condition = self.current_condition
        
        # Add random variations
        latency = max(0.1, np.random.normal(
            condition.base_latency, 
            condition.latency_variance
        ))
        
        packet_loss = max(0.0, min(100.0, np.random.normal(
            condition.base_packet_loss,
            condition.loss_variance
        )))
        
        throughput = max(1.0, np.random.normal(
            condition.base_throughput,
            condition.throughput_variance
        ))
        
        # Calculate jitter as latency variation
        jitter = abs(np.random.normal(0, condition.latency_variance * 0.5))
        
        # Apply environmental factors
        interference = self._get_current_interference()
        congestion = self._get_current_congestion()
        handoff_penalty = self._simulate_handoff_event()
        burst_loss = self._simulate_burst_loss()
        thermal_factor = self._simulate_thermal_throttling()
        
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
        
        # Apply handoff penalty
        latency *= handoff_penalty
        
        # Apply burst loss
        if burst_loss > 0:
            packet_loss = max(packet_loss, burst_loss)
        
        # Apply thermal throttling
        latency *= thermal_factor
        throughput *= (2.0 - thermal_factor)  # Inverse relationship
        
        # Add instability factor
        instability = condition.instability_factor
        if random.random() < instability:
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
        print(f"Starting scenario: {scenario_name}")
        
        if scenario_name == "stable_baseline":
            self.set_condition('wifi_optimal')
            
        elif scenario_name == "sudden_congestion":
            self.set_condition('wifi_optimal')
            # Add congestion events
            self.add_congestion_event(10.0, 15.0, 0.8)
            self.add_congestion_event(35.0, 10.0, 0.6)
            
        elif scenario_name == "intermittent_loss":
            self.set_condition('lte_good')
            # Add burst loss events
            for i in range(5):
                start_time = random.uniform(5.0, duration - 10.0)
                self.add_interference_event(start_time, 3.0, 0.7)
                
        elif scenario_name == "handoff_stress":
            self.set_condition('lte_good')
            # Simulate frequent handoffs
            for i in range(10):
                start_time = i * (duration / 10)
                self.add_interference_event(start_time, 2.0, 0.5)
                
        elif scenario_name == "6g_simulation":
            self.set_condition('6g_simulation')
            # Add minimal interference for ultra-low latency testing
            self.add_interference_event(duration * 0.3, 5.0, 0.1)
            
        elif scenario_name == "edge_ai_workload":
            self.set_condition('edge_computing')
            # Simulate AI inference bursts
            for i in range(8):
                start_time = i * (duration / 8)
                self.add_congestion_event(start_time, 2.0, 0.3)
                
        elif scenario_name == "extreme_conditions":
            self.set_condition('satellite')
            # Add multiple stressors
            self.add_interference_event(5.0, 20.0, 0.9)
            self.add_congestion_event(15.0, 25.0, 0.8)
            self.add_interference_event(40.0, 15.0, 0.7)
            
        elif scenario_name == "long_term_stability":
            self.set_condition('5g_variable')
            # Add periodic stress events
            for i in range(int(duration / 30)):
                start_time = i * 30 + random.uniform(5, 25)
                self.add_congestion_event(start_time, 5.0, 0.4)
        
        print(f"Scenario '{scenario_name}' configured for {duration} seconds")
    
    def reset_events(self):
        """Reset all interference and congestion events"""
        self.interference_events.clear()
        self.congestion_events.clear()
        self.time_start = time.time()
        print("Network events reset")
    
    def get_scenario_info(self) -> Dict:
        """Get information about current scenario"""
        return {
            'condition': self.current_condition.network_type if self.current_condition else 'None',
            'interference_events': len(self.interference_events),
            'congestion_events': len(self.congestion_events),
            'current_interference': self._get_current_interference(),
            'current_congestion': self._get_current_congestion(),
            'simulation_time': time.time() - self.time_start
        }
