"""
BARH Protocol - Network Monitor (Algorithm 1)
خوارزمية مراقبة الشبكة - الخوارزمية الأولى
"""

import asyncio
import time
from collections import deque
from typing import List, Optional
from data_structures import NetworkMetrics, Statistics
from network_simulator import NetworkSimulator
from config import *

class NetworkMonitor:
    """مراقب الشبكة - ينفذ الخوارزمية الأولى من BARH"""
    
    def __init__(self, simulator: NetworkSimulator):
        self.simulator = simulator
        self.metrics_buffer = deque(maxlen=METRICS_BUFFER_SIZE)
        self.is_monitoring = False
        self.monitoring_task = None
        
    async def start_monitoring(self):
        """بدء مراقبة الشبكة"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        print("🔍 Network monitoring started")
        
    async def stop_monitoring(self):
        """إيقاف مراقبة الشبكة"""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        print("⏹️ Network monitoring stopped")
        
    async def _monitoring_loop(self):
        """الحلقة الرئيسية للمراقبة"""
        try:
            while self.is_monitoring:
                # Algorithm 1: Network Monitoring
                start_time = time.time()
                
                # Collect current metrics
                metrics = self.simulator.get_current_metrics()
                
                # Store in buffer
                self.metrics_buffer.append(metrics)
                
                # Calculate monitoring overhead
                monitoring_time = (time.time() - start_time) * 1000  # Convert to ms
                
                # Log metrics periodically
                if len(self.metrics_buffer) % 50 == 0:  # Every 5 seconds
                    self._log_current_status(metrics, monitoring_time)
                
                # Wait for next monitoring interval
                await asyncio.sleep(MONITOR_INTERVAL)
                
        except asyncio.CancelledError:
            print("🔍 Monitoring loop cancelled")
            
    def _log_current_status(self, metrics: NetworkMetrics, monitoring_time: float):
        """تسجيل الحالة الحالية"""
        network_status = self.simulator.get_network_status()
        status_icon = "🟢" if network_status["stable"] else "🔴"
        
        print(f"{status_icon} Latency: {metrics.latency:.1f}ms | "
              f"Loss: {metrics.packet_loss:.1f}% | "
              f"Throughput: {metrics.throughput:.1f}Mbps | "
              f"Monitor Time: {monitoring_time:.2f}ms")
              
        if not network_status["stable"]:
            remaining = network_status["instability_remaining"]
            print(f"   ⚠️ Instability: {network_status['instability_type']} ({remaining:.1f}s remaining)")
    
    def get_recent_metrics(self, count: int = 10) -> List[NetworkMetrics]:
        """الحصول على آخر مقاييس"""
        if len(self.metrics_buffer) < count:
            return list(self.metrics_buffer)
        return list(self.metrics_buffer)[-count:]
    
    def get_baseline_metrics(self) -> Optional[List[NetworkMetrics]]:
        """الحصول على مقاييس الخط الأساسي"""
        if len(self.metrics_buffer) < BASELINE_WINDOW_SIZE:
            return None
        return list(self.metrics_buffer)[-BASELINE_WINDOW_SIZE:]
    
    def calculate_statistics(self, metric_type: str) -> Optional[Statistics]:
        """حساب الإحصائيات لنوع مقياس معين"""
        if len(self.metrics_buffer) < MIN_SAMPLES_FOR_BASELINE:
            return None
            
        # Extract values for the specified metric
        values = []
        for metrics in self.metrics_buffer:
            if metric_type == "latency":
                values.append(metrics.latency)
            elif metric_type == "packet_loss":
                values.append(metrics.packet_loss)
            elif metric_type == "throughput":
                values.append(metrics.throughput)
        
        if not values:
            return None
            
        # Calculate statistics
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_deviation = variance ** 0.5
        min_value = min(values)
        max_value = max(values)
        
        return Statistics(
            mean=mean,
            variance=variance,
            std_deviation=std_deviation,
            min_value=min_value,
            max_value=max_value,
            sample_count=len(values)
        )
    
    def get_monitoring_performance(self) -> dict:
        """الحصول على أداء المراقبة"""
        return {
            "buffer_size": len(self.metrics_buffer),
            "buffer_capacity": METRICS_BUFFER_SIZE,
            "monitoring_active": self.is_monitoring,
            "samples_collected": len(self.metrics_buffer)
        }
