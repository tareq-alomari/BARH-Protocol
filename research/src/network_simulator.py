"""
BARH Protocol - Network Simulator
محاكي الشبكة لاختبار بروتوكول BARH
"""

import random
import time
import math
from typing import Dict, List
from data_structures import NetworkMetrics
from config import *

class NetworkSimulator:
    """محاكي ظروف الشبكة المختلفة"""
    
    def __init__(self):
        # Base network conditions (stable)
        self.base_latency = 15.0        # 15ms baseline
        self.base_packet_loss = 1.0     # 1% baseline
        self.base_throughput = 50.0     # 50 Mbps baseline
        
        # Instability parameters
        self.instability_active = False
        self.instability_start_time = 0
        self.instability_duration = 0
        self.instability_type = "none"
        
        # Noise parameters
        self.noise_factor = 0.1  # 10% random variation
        
    def get_current_metrics(self) -> NetworkMetrics:
        """الحصول على مقاييس الشبكة الحالية"""
        
        # Check if we should trigger instability
        if not self.instability_active and random.random() < NETWORK_INSTABILITY_PROBABILITY:
            self._trigger_instability()
        
        # Check if instability should end
        if self.instability_active:
            if time.time() - self.instability_start_time > self.instability_duration:
                self.instability_active = False
                self.instability_type = "none"
        
        # Calculate current metrics
        latency = self._calculate_latency()
        packet_loss = self._calculate_packet_loss()
        throughput = self._calculate_throughput()
        
        return NetworkMetrics(
            latency=latency,
            packet_loss=packet_loss,
            throughput=throughput,
            timestamp=time.time()
        )
    
    def _trigger_instability(self):
        """تفعيل عدم استقرار الشبكة"""
        self.instability_active = True
        self.instability_start_time = time.time()
        self.instability_duration = random.uniform(5, 15)  # 5-15 seconds
        
        # Choose type of instability
        instability_types = ["high_latency", "packet_loss", "low_throughput", "mixed"]
        self.instability_type = random.choice(instability_types)
        
        print(f"🚨 Network instability triggered: {self.instability_type} for {self.instability_duration:.1f}s")
    
    def _calculate_latency(self) -> float:
        """حساب زمن الاستجابة"""
        latency = self.base_latency
        
        # Add random noise
        latency += random.uniform(-self.noise_factor * latency, self.noise_factor * latency)
        
        # Add instability effects
        if self.instability_active:
            if self.instability_type in ["high_latency", "mixed"]:
                # Increase latency by 2-5x during instability
                multiplier = random.uniform(2.0, 5.0)
                latency *= multiplier
        
        return max(1.0, latency)  # Minimum 1ms
    
    def _calculate_packet_loss(self) -> float:
        """حساب نسبة فقدان الحزم"""
        packet_loss = self.base_packet_loss
        
        # Add random noise
        packet_loss += random.uniform(-0.2, 0.2)
        
        # Add instability effects
        if self.instability_active:
            if self.instability_type in ["packet_loss", "mixed"]:
                # Increase packet loss significantly
                packet_loss += random.uniform(3.0, 8.0)
        
        return max(0.0, min(50.0, packet_loss))  # 0-50% range
    
    def _calculate_throughput(self) -> float:
        """حساب معدل النقل"""
        throughput = self.base_throughput
        
        # Add random noise
        throughput += random.uniform(-self.noise_factor * throughput, self.noise_factor * throughput)
        
        # Add instability effects
        if self.instability_active:
            if self.instability_type in ["low_throughput", "mixed"]:
                # Reduce throughput by 30-70%
                reduction = random.uniform(0.3, 0.7)
                throughput *= (1 - reduction)
        
        return max(1.0, throughput)  # Minimum 1 Mbps
    
    def simulate_correction_effect(self, metrics: NetworkMetrics, correction_type: str) -> NetworkMetrics:
        """محاكاة تأثير التصحيح على المقاييس"""
        
        # Simulate correction improvements based on research paper targets
        improved_latency = metrics.latency
        improved_packet_loss = metrics.packet_loss
        improved_throughput = metrics.throughput
        
        if correction_type == "buffer_optimization":
            # Primarily improves latency
            improved_latency *= 0.7  # 30% improvement
            improved_throughput *= 1.05  # 5% improvement
            
        elif correction_type == "retransmission_control":
            # Primarily improves packet loss
            improved_packet_loss *= 0.4  # 60% improvement
            improved_latency *= 0.9  # 10% improvement
            
        elif correction_type == "interface_switch":
            # Improves all metrics moderately
            improved_latency *= 0.8
            improved_packet_loss *= 0.6
            improved_throughput *= 1.1
        
        # Add some randomness to make it realistic
        noise = 0.05  # 5% noise
        improved_latency *= random.uniform(1-noise, 1+noise)
        improved_packet_loss *= random.uniform(1-noise, 1+noise)
        improved_throughput *= random.uniform(1-noise, 1+noise)
        
        return NetworkMetrics(
            latency=max(1.0, improved_latency),
            packet_loss=max(0.0, improved_packet_loss),
            throughput=max(1.0, improved_throughput),
            timestamp=time.time()
        )
    
    def get_network_status(self) -> Dict:
        """الحصول على حالة الشبكة الحالية"""
        return {
            "stable": not self.instability_active,
            "instability_type": self.instability_type,
            "instability_remaining": max(0, self.instability_duration - (time.time() - self.instability_start_time)) if self.instability_active else 0
        }
