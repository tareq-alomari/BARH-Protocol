"""
BARH Protocol - Machine Learning Enhanced Deviation Detector
كاشف الانحرافات المحسن بالتعلم الآلي
"""

import time
import math
# Simple numpy replacement for basic operations
class SimpleNumPy:
    @staticmethod
    def array(data):
        return data
    
    @staticmethod
    def mean(data):
        return sum(data) / len(data) if data else 0
    
    @staticmethod
    def std(data):
        if not data or len(data) < 2:
            return 0
        mean_val = sum(data) / len(data)
        variance = sum((x - mean_val) ** 2 for x in data) / len(data)
        return variance ** 0.5
    
    @staticmethod
    def var(data):
        if not data or len(data) < 2:
            return 0
        mean_val = sum(data) / len(data)
        return sum((x - mean_val) ** 2 for x in data) / len(data)
    
    @staticmethod
    def min(data):
        return min(data) if data else 0
    
    @staticmethod
    def max(data):
        return max(data) if data else 0
    
    @staticmethod
    def median(data):
        if not data:
            return 0
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2-1] + sorted_data[n//2]) / 2
        return sorted_data[n//2]
    
    @staticmethod
    def percentile(data, p):
        if not data:
            return 0
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * p / 100
        f = int(k)
        c = k - f
        if f + 1 < len(sorted_data):
            return sorted_data[f] * (1 - c) + sorted_data[f + 1] * c
        return sorted_data[f]
    
    @staticmethod
    def eye(n):
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    @staticmethod
    def exp(data):
        import math
        if isinstance(data, list):
            return [math.exp(x) for x in data]
        return math.exp(data)
    
    @staticmethod
    def linspace(start, stop, num):
        if num <= 1:
            return [start]
        step = (stop - start) / (num - 1)
        return [start + i * step for i in range(num)]
    
    @staticmethod
    def average(data, weights=None):
        if not data:
            return 0
        if weights is None:
            return sum(data) / len(data)
        
        if len(data) != len(weights):
            return sum(data) / len(data)
        
        weighted_sum = sum(d * w for d, w in zip(data, weights))
        weight_sum = sum(weights)
        return weighted_sum / weight_sum if weight_sum > 0 else 0
    
    @staticmethod
    def random_uniform(low, high):
        import random
        return random.uniform(low, high)

np = SimpleNumPy()
from typing import List, Optional, Dict, Tuple
from collections import deque
from data_structures import NetworkMetrics, Deviation, Statistics
from advanced_config import *

class MLEnhancedDeviationDetector:
    """كاشف انحرافات محسن بالتعلم الآلي للدقة القصوى"""
    
    def __init__(self):
        self.baseline_stats = {}
        self.detection_history = []
        self.adaptive_thresholds = {}
        
        # Machine Learning Components
        self.prediction_weights = {"latency": 0.5, "packet_loss": 0.5, "throughput": 0.5}
        self.learning_buffer = deque(maxlen=ML_ADAPTATION_WINDOW)
        self.prediction_accuracy = {"latency": 0.5, "packet_loss": 0.5, "throughput": 0.5}
        
        # Advanced Statistics
        self.micro_trends = {"latency": [], "packet_loss": [], "throughput": []}
        self.correlation_matrix = np.eye(3)  # latency, packet_loss, throughput correlations
        
    def analyze_metrics_advanced(self, current_metrics: NetworkMetrics, 
                                historical_metrics: List[NetworkMetrics]) -> List[Deviation]:
        """تحليل متقدم للمقاييس مع التعلم الآلي"""
        
        if len(historical_metrics) < MIN_SAMPLES_FOR_BASELINE:
            return []
        
        deviations = []
        
        # Enhanced analysis for each metric
        for metric_type in ["latency", "packet_loss", "throughput"]:
            # Traditional detection
            traditional_deviation = self._detect_traditional_deviation(
                current_metrics, historical_metrics, metric_type
            )
            
            # ML-enhanced prediction
            ml_deviation = self._detect_ml_enhanced_deviation(
                current_metrics, historical_metrics, metric_type
            )
            
            # Combine results with confidence weighting
            final_deviation = self._combine_detection_results(
                traditional_deviation, ml_deviation, metric_type
            )
            
            if final_deviation and final_deviation.detected:
                deviations.append(final_deviation)
                self.detection_history.append(final_deviation)
        
        # Update ML models
        self._update_ml_models(current_metrics, historical_metrics, deviations)
        
        return deviations
    
    def _detect_traditional_deviation(self, current_metrics: NetworkMetrics,
                                    historical_metrics: List[NetworkMetrics],
                                    metric_type: str) -> Optional[Deviation]:
        """الكشف التقليدي المحسن"""
        
        historical_values = self._extract_metric_values(historical_metrics, metric_type)
        current_value = self._get_current_metric_value(current_metrics, metric_type)
        
        # Enhanced statistical analysis
        baseline_stats = self._calculate_enhanced_statistics(historical_values)
        self.baseline_stats[metric_type] = baseline_stats
        
        # Adaptive thresholds based on recent trends
        thresholds = self._calculate_adaptive_thresholds(baseline_stats, metric_type, historical_values)
        
        # Multi-level deviation detection
        deviation_detected, severity = self._multi_level_deviation_check(
            current_value, thresholds, baseline_stats
        )
        
        return Deviation(
            detected=deviation_detected,
            severity=severity,
            metric_type=metric_type,
            current_value=current_value,
            baseline_value=baseline_stats.mean,
            timestamp=time.time()
        )
    
    def _detect_ml_enhanced_deviation(self, current_metrics: NetworkMetrics,
                                    historical_metrics: List[NetworkMetrics],
                                    metric_type: str) -> Optional[Deviation]:
        """الكشف المحسن بالتعلم الآلي"""
        
        if not ML_PREDICTION_ENABLED or len(self.learning_buffer) < 10:
            return None
        
        # Predict expected value using ML
        predicted_value = self._predict_metric_value(historical_metrics, metric_type)
        current_value = self._get_current_metric_value(current_metrics, metric_type)
        
        # Calculate prediction error
        prediction_error = abs(current_value - predicted_value) / max(predicted_value, 1.0)
        
        # ML-based deviation threshold
        ml_threshold = self._calculate_ml_threshold(metric_type)
        
        deviation_detected = prediction_error > ml_threshold
        severity = min(1.0, prediction_error / ml_threshold) if deviation_detected else 0.0
        
        return Deviation(
            detected=deviation_detected,
            severity=severity * 0.8,  # Weight ML detection slightly lower
            metric_type=metric_type,
            current_value=current_value,
            baseline_value=predicted_value,
            timestamp=time.time()
        )
    
    def _combine_detection_results(self, traditional: Optional[Deviation], 
                                 ml_enhanced: Optional[Deviation],
                                 metric_type: str) -> Optional[Deviation]:
        """دمج نتائج الكشف التقليدي والمحسن بالتعلم الآلي"""
        
        if not traditional:
            return ml_enhanced
        if not ml_enhanced:
            return traditional
        
        # Weighted combination based on prediction accuracy
        ml_weight = self.prediction_accuracy.get(metric_type, 0.5)
        traditional_weight = 1.0 - ml_weight
        
        # Combine detection decisions
        combined_detected = traditional.detected or ml_enhanced.detected
        
        # Weighted severity
        combined_severity = (
            traditional.severity * traditional_weight + 
            ml_enhanced.severity * ml_weight
        )
        
        # Use traditional baseline but enhanced severity
        return Deviation(
            detected=combined_detected,
            severity=combined_severity,
            metric_type=metric_type,
            current_value=traditional.current_value,
            baseline_value=traditional.baseline_value,
            timestamp=time.time()
        )
    
    def _calculate_enhanced_statistics(self, values: List[float]) -> Statistics:
        """حساب إحصائيات محسنة مع تحليل متقدم"""
        
        if not values:
            return Statistics(0, 0, 0, 0, 0, 0)
        
        values_array = np.array(values)
        
        # Basic statistics
        mean = np.mean(values_array)
        variance = np.var(values_array)
        std_deviation = np.std(values_array)
        min_value = np.min(values_array)
        max_value = np.max(values_array)
        
        # Enhanced statistics
        median = np.median(values_array)
        q75 = np.percentile(values_array, 75)
        q25 = np.percentile(values_array, 25)
        iqr = q75 - q25
        
        # Trend analysis
        if len(values) > 10:
            recent_trend = np.mean(values_array[-10:]) - np.mean(values_array[:-10])
        else:
            recent_trend = 0
        
        return Statistics(
            mean=mean,
            variance=variance,
            std_deviation=std_deviation,
            min_value=min_value,
            max_value=max_value,
            sample_count=len(values)
        )
    
    def _calculate_adaptive_thresholds(self, baseline_stats: Statistics, 
                                     metric_type: str, historical_values: List[float]) -> Dict[str, float]:
        """حساب عتبات تكيفية متقدمة"""
        
        base_sensitivity = SENSITIVITY_FACTOR
        
        # Adaptive sensitivity based on recent volatility
        if len(historical_values) > 20:
            recent_volatility = np.std(historical_values[-20:])
            historical_volatility = baseline_stats.std_deviation
            
            if recent_volatility > historical_volatility * 1.5:
                # High recent volatility - reduce sensitivity
                adaptive_sensitivity = base_sensitivity * 0.8
            elif recent_volatility < historical_volatility * 0.5:
                # Low recent volatility - increase sensitivity
                adaptive_sensitivity = base_sensitivity * 1.3
            else:
                adaptive_sensitivity = base_sensitivity
        else:
            adaptive_sensitivity = base_sensitivity
        
        # Metric-specific adjustments
        if metric_type == "latency":
            upper_sensitivity = adaptive_sensitivity * 1.1
            lower_sensitivity = adaptive_sensitivity * 0.9
        elif metric_type == "packet_loss":
            upper_sensitivity = adaptive_sensitivity * 1.4
            lower_sensitivity = adaptive_sensitivity * 0.6
        else:  # throughput
            upper_sensitivity = adaptive_sensitivity * 0.9
            lower_sensitivity = adaptive_sensitivity * 1.1
        
        upper_threshold = baseline_stats.mean + (upper_sensitivity * baseline_stats.std_deviation)
        lower_threshold = baseline_stats.mean - (lower_sensitivity * baseline_stats.std_deviation)
        
        # Apply constraints
        if metric_type == "packet_loss":
            lower_threshold = max(0.0, lower_threshold)
            upper_threshold = min(50.0, upper_threshold)
        elif metric_type == "latency":
            lower_threshold = max(1.0, lower_threshold)
        elif metric_type == "throughput":
            lower_threshold = max(1.0, lower_threshold)
        
        return {
            "upper": upper_threshold,
            "lower": lower_threshold,
            "adaptive_sensitivity": adaptive_sensitivity
        }
    
    def _multi_level_deviation_check(self, current_value: float, 
                                   thresholds: Dict[str, float],
                                   baseline_stats: Statistics) -> Tuple[bool, float]:
        """فحص انحراف متعدد المستويات"""
        
        # Level 1: Basic threshold check
        basic_deviation = (current_value > thresholds["upper"] or 
                          current_value < thresholds["lower"])
        
        if not basic_deviation:
            return False, 0.0
        
        # Level 2: Severity calculation
        if baseline_stats.std_deviation > 0:
            severity = abs(current_value - baseline_stats.mean) / baseline_stats.std_deviation
            normalized_severity = min(1.0, severity / 5.0)
        else:
            normalized_severity = 0.5
        
        # Level 3: Confidence adjustment
        confidence_multiplier = min(1.0, baseline_stats.sample_count / 50.0)
        final_severity = normalized_severity * confidence_multiplier
        
        return True, final_severity
    
    def _predict_metric_value(self, historical_metrics: List[NetworkMetrics], 
                            metric_type: str) -> float:
        """التنبؤ بقيمة المقياس باستخدام التعلم الآلي"""
        
        values = self._extract_metric_values(historical_metrics[-20:], metric_type)
        if len(values) < 5:
            return values[-1] if values else 0.0
        
        # Simple weighted moving average with trend
        weights = np.exp(np.linspace(-1, 0, len(values)))
        weights /= weights.sum()
        
        weighted_avg = np.average(values, weights=weights)
        
        # Add trend component
        if len(values) > 3:
            trend = (values[-1] - values[-3]) / 2
            predicted_value = weighted_avg + trend * 0.3
        else:
            predicted_value = weighted_avg
        
        return max(0.0, predicted_value)
    
    def _calculate_ml_threshold(self, metric_type: str) -> float:
        """حساب عتبة التعلم الآلي"""
        
        base_threshold = 0.2  # 20% prediction error threshold
        accuracy = self.prediction_accuracy.get(metric_type, 0.5)
        
        # Adjust threshold based on prediction accuracy
        if accuracy > 0.8:
            return base_threshold * 0.8  # More strict when accurate
        elif accuracy < 0.3:
            return base_threshold * 1.5  # More lenient when inaccurate
        else:
            return base_threshold
    
    def _update_ml_models(self, current_metrics: NetworkMetrics,
                         historical_metrics: List[NetworkMetrics],
                         detected_deviations: List[Deviation]):
        """تحديث نماذج التعلم الآلي"""
        
        if not ML_PREDICTION_ENABLED:
            return
        
        # Add to learning buffer
        self.learning_buffer.append({
            "metrics": current_metrics,
            "deviations": detected_deviations,
            "timestamp": time.time()
        })
        
        # Update prediction accuracy
        if len(self.learning_buffer) > 10:
            self._update_prediction_accuracy()
        
        # Update prediction weights
        self._update_prediction_weights(detected_deviations)
    
    def _update_prediction_accuracy(self):
        """تحديث دقة التنبؤ"""
        
        if len(self.learning_buffer) < 10:
            return
        
        for metric_type in ["latency", "packet_loss", "throughput"]:
            recent_predictions = []
            actual_values = []
            
            for i in range(5, len(self.learning_buffer)):
                historical = [entry["metrics"] for entry in list(self.learning_buffer)[i-5:i]]
                predicted = self._predict_metric_value(historical, metric_type)
                actual = self._get_current_metric_value(self.learning_buffer[i]["metrics"], metric_type)
                
                recent_predictions.append(predicted)
                actual_values.append(actual)
            
            if recent_predictions and actual_values:
                # Calculate accuracy as 1 - normalized mean absolute error
                mae = np.mean(np.abs(np.array(recent_predictions) - np.array(actual_values)))
                mean_actual = np.mean(actual_values)
                normalized_mae = mae / max(mean_actual, 1.0)
                accuracy = max(0.1, 1.0 - normalized_mae)
                
                # Update with learning rate
                old_accuracy = self.prediction_accuracy[metric_type]
                self.prediction_accuracy[metric_type] = (
                    old_accuracy * (1 - ML_LEARNING_RATE) + accuracy * ML_LEARNING_RATE
                )
    
    def _update_prediction_weights(self, detected_deviations: List[Deviation]):
        """تحديث أوزان التنبؤ"""
        
        for deviation in detected_deviations:
            metric_type = deviation.metric_type
            current_weight = self.prediction_weights[metric_type]
            
            # Increase weight for metrics with detected deviations
            new_weight = min(1.0, current_weight + ML_LEARNING_RATE * 0.1)
            self.prediction_weights[metric_type] = new_weight
    
    def _extract_metric_values(self, metrics_list: List[NetworkMetrics], 
                              metric_type: str) -> List[float]:
        """استخراج قيم المقياس"""
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
    
    def get_advanced_detection_summary(self) -> Dict:
        """الحصول على ملخص الكشف المتقدم"""
        
        base_summary = {
            "total_detections": len(self.detection_history),
            "ml_prediction_accuracy": self.prediction_accuracy,
            "adaptive_thresholds_active": ADAPTIVE_THRESHOLD_ENABLED,
            "ml_enhancement_active": ML_PREDICTION_ENABLED
        }
        
        if self.detection_history:
            by_metric = {}
            total_severity = 0.0
            
            for deviation in self.detection_history:
                metric_type = deviation.metric_type
                by_metric[metric_type] = by_metric.get(metric_type, 0) + 1
                total_severity += deviation.severity
            
            base_summary.update({
                "by_metric": by_metric,
                "average_severity": total_severity / len(self.detection_history),
                "recent_detections": len([d for d in self.detection_history 
                                        if time.time() - d.timestamp < 60])
            })
        
        return base_summary
