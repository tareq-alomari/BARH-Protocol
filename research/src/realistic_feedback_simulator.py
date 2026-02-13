"""
Realistic Feedback-Enabled Network Simulator
Closed-Loop Control System with Real Correction Effects
"""

import time
import math
import random
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
class CorrectionEffect:
    correction_type: str
    improvement_factor: float
    applied_at: float
    duration: float
    decay_rate: float = 0.1

class RealisticFeedbackSimulator:
    """Realistic simulator with correction feedback loop"""
    
    def __init__(self):
        self.base_condition = None
        self.active_corrections = deque(maxlen=50)
        self.correction_effects = {
            'buffer_optimization': {'latency': 0.45, 'jitter': 0.55, 'duration': 8.0},
            'connection_pooling': {'latency': 0.60, 'packet_loss': 0.40, 'duration': 12.0},
            'route_optimization': {'latency': 0.70, 'throughput': 0.45, 'duration': 15.0},
            'adaptive_compression': {'throughput': 0.35, 'packet_loss': 0.30, 'duration': 10.0},
            'parallel_connections': {'throughput': 0.60, 'latency': 0.35, 'duration': 20.0},
            'predictive_prefetch': {'latency': 0.50, 'jitter': 0.60, 'duration': 6.0}
        }
        
        # Network conditions
        self.conditions = {
            'wifi_optimal': {'latency': 5.0, 'var': 1.0, 'loss': 0.1, 'throughput': 100.0, 'instability': 0.1},
            'sudden_congestion': {'latency': 25.0, 'var': 12.0, 'loss': 3.5, 'throughput': 45.0, 'instability': 0.6},
            'intermittent_loss': {'latency': 18.0, 'var': 6.0, 'loss': 2.8, 'throughput': 65.0, 'instability': 0.4},
            '6g_simulation': {'latency': 1.2, 'var': 0.3, 'loss': 0.02, 'throughput': 280.0, 'instability': 0.02},
            'extreme_conditions': {'latency': 85.0, 'var': 35.0, 'loss': 8.5, 'throughput': 15.0, 'instability': 0.8}
        }
        
        self.time_start = time.time()
        self.set_condition('wifi_optimal')
    
    def set_condition(self, condition_name: str):
        """Set base network condition"""
        if condition_name in self.conditions:
            self.base_condition = self.conditions[condition_name]
    
    def apply_correction(self, correction_type: str, expected_improvement: float):
        """Apply correction with realistic feedback effect"""
        if correction_type in self.correction_effects:
            effect_config = self.correction_effects[correction_type]
            
            # Create correction effect with adaptive improvement
            effect = CorrectionEffect(
                correction_type=correction_type,
                improvement_factor=expected_improvement * 0.8,  # 80% efficiency
                applied_at=time.time(),
                duration=effect_config['duration'],
                decay_rate=0.1
            )
            
            self.active_corrections.append(effect)
            return True
        return False
    
    def _calculate_correction_impact(self, metric_type: str) -> float:
        """Calculate cumulative correction impact on specific metric"""
        current_time = time.time()
        total_improvement = 0.0
        
        # Remove expired corrections
        active_corrections = []
        for correction in self.active_corrections:
            if current_time - correction.applied_at < correction.duration:
                active_corrections.append(correction)
        
        self.active_corrections.clear()
        self.active_corrections.extend(active_corrections)
        
        # Calculate cumulative effect with decay
        for correction in self.active_corrections:
            effect_config = self.correction_effects.get(correction.correction_type, {})
            
            if metric_type in effect_config:
                # Time-based decay
                elapsed = current_time - correction.applied_at
                decay_factor = math.exp(-correction.decay_rate * elapsed)
                
                # Metric-specific improvement
                base_improvement = effect_config[metric_type]
                actual_improvement = base_improvement * correction.improvement_factor * decay_factor
                
                total_improvement += actual_improvement
        
        # Cap maximum improvement at 85%
        return min(0.85, total_improvement)
    
    def _generate_base_metrics(self) -> Dict:
        """Generate base network metrics with realistic variations"""
        if not self.base_condition:
            return {'latency': 10.0, 'packet_loss': 1.0, 'throughput': 50.0, 'jitter': 2.0}
        
        condition = self.base_condition
        
        # Box-Muller transform for normal distribution
        def normal_random(mean: float, std: float) -> float:
            u1, u2 = random.random(), random.random()
            z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            return mean + z * std
        
        # Generate base metrics
        base_latency = max(0.5, normal_random(condition['latency'], condition['var']))
        base_packet_loss = max(0.0, min(50.0, normal_random(condition['loss'], condition['var'] * 0.3)))
        base_throughput = max(5.0, normal_random(condition['throughput'], condition['var'] * 2))
        base_jitter = abs(normal_random(0, condition['var'] * 0.4))
        
        # Add instability spikes
        if random.random() < condition['instability']:
            spike = random.uniform(1.5, 2.5)
            base_latency *= spike
            base_packet_loss *= spike
            base_throughput /= spike
            base_jitter *= spike
        
        return {
            'latency': base_latency,
            'packet_loss': base_packet_loss,
            'throughput': base_throughput,
            'jitter': base_jitter
        }
    
    def get_current_metrics(self) -> NetworkMetrics:
        """Get current metrics with correction effects applied"""
        # Generate base metrics
        base = self._generate_base_metrics()
        
        # Apply correction improvements
        latency_improvement = self._calculate_correction_impact('latency')
        packet_loss_improvement = self._calculate_correction_impact('packet_loss')
        throughput_improvement = self._calculate_correction_impact('throughput')
        jitter_improvement = self._calculate_correction_impact('jitter')
        
        # Apply improvements with realistic bounds
        corrected_latency = base['latency'] * (1 - latency_improvement)
        corrected_packet_loss = base['packet_loss'] * (1 - packet_loss_improvement)
        corrected_throughput = base['throughput'] * (1 + throughput_improvement)
        corrected_jitter = base['jitter'] * (1 - jitter_improvement)
        
        # Ensure realistic bounds
        corrected_latency = max(0.1, min(1000.0, corrected_latency))
        corrected_packet_loss = max(0.0, min(100.0, corrected_packet_loss))
        corrected_throughput = max(1.0, min(500.0, corrected_throughput))
        corrected_jitter = max(0.0, min(corrected_latency * 0.3, corrected_jitter))
        
        return NetworkMetrics(
            latency=corrected_latency,
            packet_loss=corrected_packet_loss,
            throughput=corrected_throughput,
            jitter=corrected_jitter,
            timestamp=time.time(),
            network_type=self.base_condition.get('type', 'Simulated') if self.base_condition else 'Unknown'
        )
    
    def get_active_corrections_info(self) -> Dict:
        """Get information about active corrections"""
        current_time = time.time()
        active_info = []
        
        for correction in self.active_corrections:
            elapsed = current_time - correction.applied_at
            remaining = max(0, correction.duration - elapsed)
            
            active_info.append({
                'type': correction.correction_type,
                'elapsed': elapsed,
                'remaining': remaining,
                'effectiveness': math.exp(-correction.decay_rate * elapsed)
            })
        
        return {
            'active_corrections': len(self.active_corrections),
            'corrections_info': active_info,
            'total_latency_improvement': self._calculate_correction_impact('latency'),
            'total_packet_loss_improvement': self._calculate_correction_impact('packet_loss'),
            'total_throughput_improvement': self._calculate_correction_impact('throughput')
        }
    
    def reset_corrections(self):
        """Reset all active corrections"""
        self.active_corrections.clear()
        self.time_start = time.time()
    
    def simulate_scenario(self, scenario_name: str):
        """Set up scenario conditions"""
        scenario_mapping = {
            'stable_baseline': 'wifi_optimal',
            'sudden_congestion': 'sudden_congestion',
            'intermittent_loss': 'intermittent_loss',
            '6g_simulation': '6g_simulation',
            'extreme_conditions': 'extreme_conditions'
        }
        
        condition = scenario_mapping.get(scenario_name, 'wifi_optimal')
        self.set_condition(condition)
