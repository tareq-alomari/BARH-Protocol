"""
BARH Protocol - Deviation Detector (Algorithm 2)
خوارزمية اكتشاف الانحراف - الخوارزمية الثانية
"""

import time
import math
from typing import List, Optional, Dict
from data_structures import NetworkMetrics, Deviation, Statistics
from config import *

class DeviationDetector:
    """كاشف الانحرافات - ينفذ الخوارزمية الثانية من BARH"""
    
    def __init__(self):
        self.baseline_stats = {}  # Statistics for each metric type
        self.detection_history = []  # History of detected deviations
        
    def analyze_metrics(self, current_metrics: NetworkMetrics, 
                       historical_metrics: List[NetworkMetrics]) -> List[Deviation]:
        """تحليل المقاييس الحالية واكتشاف الانحرافات"""
        
        if len(historical_metrics) < MIN_SAMPLES_FOR_BASELINE:
            return []  # Not enough data for analysis
        
        deviations = []
        
        # Check each metric type
        for metric_type in ["latency", "packet_loss", "throughput"]:
            deviation = self._detect_deviation_for_metric(
                current_metrics, historical_metrics, metric_type
            )
            if deviation and deviation.detected:
                deviations.append(deviation)
                self.detection_history.append(deviation)
        
        return deviations
    
    def _detect_deviation_for_metric(self, current_metrics: NetworkMetrics,
                                   historical_metrics: List[NetworkMetrics],
                                   metric_type: str) -> Optional[Deviation]:
        """اكتشاف الانحراف لنوع مقياس محدد"""
        
        # Extract values for the metric
        historical_values = self._extract_metric_values(historical_metrics, metric_type)
        current_value = self._get_current_metric_value(current_metrics, metric_type)
        
        if not historical_values:
            return None
        
        # Calculate baseline statistics
        baseline_stats = self._calculate_baseline_statistics(historical_values)
        self.baseline_stats[metric_type] = baseline_stats
        
        # Calculate thresholds
        thresholds = self._calculate_thresholds(baseline_stats, metric_type)
        
        # Check for deviation
        deviation_detected = self._is_deviation(current_value, thresholds)
        
        if deviation_detected:
            severity = self._calculate_severity(current_value, baseline_stats)
            
            return Deviation(
                detected=True,
                severity=severity,
                metric_type=metric_type,
                current_value=current_value,
                baseline_value=baseline_stats.mean,
                timestamp=time.time()
            )
        
        return Deviation(
            detected=False,
            severity=0.0,
            metric_type=metric_type,
            current_value=current_value,
            baseline_value=baseline_stats.mean,
            timestamp=time.time()
        )
    
    def _extract_metric_values(self, metrics_list: List[NetworkMetrics], 
                              metric_type: str) -> List[float]:
        """استخراج قيم مقياس محدد من قائمة المقاييس"""
        values = []
        for metrics in metrics_list:
            if metric_type == "latency":
                values.append(metrics.latency)
            elif metric_type == "packet_loss":
                values.append(metrics.packet_loss)
            elif metric_type == "throughput":
                values.append(metrics.throughput)
        return values
    
    def _get_current_metric_value(self, metrics: NetworkMetrics, metric_type: str) -> float:
        """الحصول على قيمة المقياس الحالي"""
        if metric_type == "latency":
            return metrics.latency
        elif metric_type == "packet_loss":
            return metrics.packet_loss
        elif metric_type == "throughput":
            return metrics.throughput
        return 0.0
    
    def _calculate_baseline_statistics(self, values: List[float]) -> Statistics:
        """حساب إحصائيات الخط الأساسي"""
        n = len(values)
        mean = sum(values) / n
        
        # Calculate variance using Welford's algorithm for numerical stability
        variance = sum((x - mean) ** 2 for x in values) / n
        std_deviation = math.sqrt(variance)
        
        return Statistics(
            mean=mean,
            variance=variance,
            std_deviation=std_deviation,
            min_value=min(values),
            max_value=max(values),
            sample_count=n
        )
    
    def _calculate_thresholds(self, baseline_stats: Statistics, metric_type: str) -> Dict[str, float]:
        """حساب عتبات الانحراف"""
        
        # Base sensitivity factor
        sensitivity = SENSITIVITY_FACTOR
        
        # Adjust sensitivity based on metric type
        if metric_type == "latency":
            # Latency is more sensitive to increases
            upper_sensitivity = sensitivity * 1.2
            lower_sensitivity = sensitivity * 0.8
        elif metric_type == "packet_loss":
            # Packet loss is very sensitive to increases
            upper_sensitivity = sensitivity * 1.5
            lower_sensitivity = sensitivity * 0.5
        elif metric_type == "throughput":
            # Throughput is sensitive to decreases
            upper_sensitivity = sensitivity * 0.8
            lower_sensitivity = sensitivity * 1.2
        else:
            upper_sensitivity = lower_sensitivity = sensitivity
        
        # Calculate thresholds
        upper_threshold = baseline_stats.mean + (upper_sensitivity * baseline_stats.std_deviation)
        lower_threshold = baseline_stats.mean - (lower_sensitivity * baseline_stats.std_deviation)
        
        # Apply metric-specific constraints
        if metric_type == "packet_loss":
            lower_threshold = max(0.0, lower_threshold)  # Cannot be negative
            upper_threshold = min(50.0, upper_threshold)  # Cap at 50%
        elif metric_type == "latency":
            lower_threshold = max(1.0, lower_threshold)   # Minimum 1ms
        elif metric_type == "throughput":
            lower_threshold = max(1.0, lower_threshold)   # Minimum 1 Mbps
        
        return {
            "upper": upper_threshold,
            "lower": lower_threshold,
            "upper_sensitivity": upper_sensitivity,
            "lower_sensitivity": lower_sensitivity
        }
    
    def _is_deviation(self, current_value: float, thresholds: Dict[str, float]) -> bool:
        """فحص ما إذا كانت القيمة الحالية تمثل انحراف"""
        return (current_value > thresholds["upper"] or 
                current_value < thresholds["lower"])
    
    def _calculate_severity(self, current_value: float, baseline_stats: Statistics) -> float:
        """حساب شدة الانحراف"""
        if baseline_stats.std_deviation == 0:
            return 0.0
        
        # Calculate how many standard deviations away from mean
        severity = abs(current_value - baseline_stats.mean) / baseline_stats.std_deviation
        
        # Normalize to 0-1 scale (cap at 5 standard deviations)
        normalized_severity = min(severity / 5.0, 1.0)
        
        return normalized_severity
    
    def get_detection_summary(self) -> Dict:
        """الحصول على ملخص الاكتشافات"""
        if not self.detection_history:
            return {
                "total_detections": 0,
                "by_metric": {},
                "average_severity": 0.0
            }
        
        # Count detections by metric type
        by_metric = {}
        total_severity = 0.0
        
        for deviation in self.detection_history:
            metric_type = deviation.metric_type
            by_metric[metric_type] = by_metric.get(metric_type, 0) + 1
            total_severity += deviation.severity
        
        return {
            "total_detections": len(self.detection_history),
            "by_metric": by_metric,
            "average_severity": total_severity / len(self.detection_history),
            "recent_detections": len([d for d in self.detection_history 
                                    if time.time() - d.timestamp < 60])  # Last minute
        }
    
    def get_current_baselines(self) -> Dict:
        """الحصول على خطوط الأساس الحالية"""
        baselines = {}
        for metric_type, stats in self.baseline_stats.items():
            baselines[metric_type] = {
                "mean": stats.mean,
                "std_deviation": stats.std_deviation,
                "sample_count": stats.sample_count
            }
        return baselines
    
    def clear_history(self):
        """مسح تاريخ الاكتشافات"""
        self.detection_history.clear()
        print("🗑️ Detection history cleared")
