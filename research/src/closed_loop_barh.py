"""
Enhanced BARH Protocol with Realistic Feedback Integration
Closed-Loop Control System Implementation
"""

import time
import math
import random
from typing import Dict, List, Tuple, Optional
from collections import deque
from realistic_feedback_simulator import RealisticFeedbackSimulator, NetworkMetrics

class AdaptiveDeviationDetector:
    """Adaptive deviation detector with dynamic thresholds"""
    
    def __init__(self, window_size=50):
        self.window_size = window_size
        self.metrics_history = deque(maxlen=window_size)
        self.adaptive_sensitivity = 0.9  # Ultra-sensitive for early detection
        self.learning_rate = 0.08
        self.false_positive_count = 0
        self.true_positive_count = 0
        
    def update_sensitivity(self, correction_was_effective: bool):
        """Update sensitivity based on correction effectiveness"""
        if correction_was_effective:
            self.true_positive_count += 1
        else:
            self.false_positive_count += 1
            
        # Adjust sensitivity every 10 detections
        total_detections = self.true_positive_count + self.false_positive_count
        if total_detections > 0 and total_detections % 10 == 0:
            false_positive_rate = self.false_positive_count / total_detections
            
            if false_positive_rate > 0.25:  # Reduced threshold
                self.adaptive_sensitivity *= (1 - self.learning_rate)
            elif false_positive_rate < 0.05:  # More aggressive detection
                self.adaptive_sensitivity *= (1 + self.learning_rate)
                
            # Optimized sensitivity bounds
            self.adaptive_sensitivity = max(0.6, min(2.5, self.adaptive_sensitivity))
    
    def detect_deviation(self, metrics: NetworkMetrics) -> Dict:
        """Enhanced deviation detection with adaptive thresholds"""
        self.metrics_history.append(metrics)
        
        if len(self.metrics_history) < 10:
            return {'deviation_detected': False, 'severity': 0.0, 'confidence': 0.0}
        
        # Calculate dynamic thresholds based on recent history
        recent_latencies = [m.latency for m in list(self.metrics_history)[-20:]]
        recent_losses = [m.packet_loss for m in list(self.metrics_history)[-20:]]
        
        # Statistical measures
        lat_mean = sum(recent_latencies) / len(recent_latencies)
        lat_std = math.sqrt(sum((x - lat_mean) ** 2 for x in recent_latencies) / len(recent_latencies))
        
        loss_mean = sum(recent_losses) / len(recent_losses)
        loss_std = math.sqrt(sum((x - loss_mean) ** 2 for x in recent_losses) / len(recent_losses))
        
        # Adaptive thresholds
        lat_threshold = lat_mean + self.adaptive_sensitivity * lat_std
        loss_threshold = loss_mean + self.adaptive_sensitivity * loss_std
        
        # Deviation detection
        lat_deviation = metrics.latency > lat_threshold
        loss_deviation = metrics.packet_loss > loss_threshold
        jitter_deviation = metrics.jitter > lat_mean * 0.3  # Jitter > 30% of mean latency
        
        # Combined decision with weighted severity
        deviation_detected = lat_deviation or loss_deviation or jitter_deviation
        
        if deviation_detected:
            # Calculate severity (0.0 to 1.0)
            lat_severity = max(0, (metrics.latency - lat_threshold) / (lat_std + 1e-6))
            loss_severity = max(0, (metrics.packet_loss - loss_threshold) / (loss_std + 1e-6))
            jitter_severity = max(0, (metrics.jitter - lat_mean * 0.3) / (lat_mean * 0.1 + 1e-6))
            
            severity = min(1.0, 0.4 * lat_severity + 0.4 * loss_severity + 0.2 * jitter_severity)
            confidence = min(0.95, 0.6 + 0.3 * severity)  # Higher severity = higher confidence
        else:
            severity = 0.0
            confidence = 0.1
        
        return {
            'deviation_detected': deviation_detected,
            'severity': severity,
            'confidence': confidence,
            'thresholds': {
                'latency': lat_threshold,
                'packet_loss': loss_threshold,
                'adaptive_sensitivity': self.adaptive_sensitivity
            }
        }

class FeedbackCorrectionEngine:
    """Correction engine with feedback integration"""
    
    def __init__(self, simulator: RealisticFeedbackSimulator):
        self.simulator = simulator
        self.correction_strategies = [
            {'type': 'buffer_optimization', 'effectiveness': 0.8, 'cost': 0.1, 'time': 0.0008},
            {'type': 'connection_pooling', 'effectiveness': 0.9, 'cost': 0.2, 'time': 0.0012},
            {'type': 'route_optimization', 'effectiveness': 1.0, 'cost': 0.3, 'time': 0.0015},
            {'type': 'adaptive_compression', 'effectiveness': 0.7, 'cost': 0.15, 'time': 0.0005},
            {'type': 'parallel_connections', 'effectiveness': 1.1, 'cost': 0.4, 'time': 0.0018},
            {'type': 'predictive_prefetch', 'effectiveness': 0.8, 'cost': 0.25, 'time': 0.0010}
        ]
        self.correction_history = deque(maxlen=100)
        
    def select_optimal_correction(self, deviation_info: Dict, system_resources: Dict) -> Optional[Dict]:
        """Select optimal correction based on current conditions"""
        if not deviation_info.get('deviation_detected', False):
            return None
            
        severity = deviation_info.get('severity', 0.0)
        available_cpu = system_resources.get('cpu_available', 0.7)
        
        # Filter viable corrections
        viable_corrections = []
        for strategy in self.correction_strategies:
            if strategy['cost'] <= available_cpu and strategy['time'] <= 0.002:
                # Latency-focused utility calculation
                if 'latency' in self.simulator.correction_effects.get(strategy['type'], {}):
                    # Prioritize latency improvements heavily
                    latency_bonus = 0.5
                    effectiveness = (strategy['effectiveness'] + latency_bonus) * severity
                else:
                    effectiveness = strategy['effectiveness'] * severity
                    
                efficiency = 1.0 / (strategy['cost'] + 0.1)
                speed = 1.0 / (strategy['time'] + 0.0001)
                
                # Weighted utility with latency priority
                utility = 0.7 * effectiveness + 0.2 * efficiency + 0.1 * speed
                
                viable_corrections.append({
                    'strategy': strategy,
                    'utility': utility,
                    'expected_improvement': effectiveness
                })
        
        if not viable_corrections:
            return None
            
        # Select best correction
        best_correction = max(viable_corrections, key=lambda x: x['utility'])
        return best_correction
    
    def apply_correction(self, correction_info: Dict) -> bool:
        """Apply correction with realistic feedback"""
        strategy = correction_info['strategy']
        expected_improvement = correction_info['expected_improvement']
        
        start_time = time.time()
        
        try:
            # Simulate correction execution time
            time.sleep(strategy['time'])
            
            # Apply correction to simulator (FEEDBACK LOOP!)
            success = self.simulator.apply_correction(
                strategy['type'], 
                expected_improvement
            )
            
            execution_time = time.time() - start_time
            
            # Record correction
            self.correction_history.append({
                'type': strategy['type'],
                'expected_improvement': expected_improvement,
                'execution_time': execution_time,
                'success': success,
                'timestamp': time.time()
            })
            
            return success
            
        except Exception as e:
            return False
    
    def get_correction_effectiveness(self) -> float:
        """Calculate recent correction effectiveness"""
        if len(self.correction_history) < 5:
            return 0.5
            
        recent_corrections = list(self.correction_history)[-10:]
        success_rate = sum(1 for c in recent_corrections if c['success']) / len(recent_corrections)
        return success_rate

class ClosedLoopBARHProtocol:
    """Enhanced BARH Protocol with Closed-Loop Control"""
    
    def __init__(self):
        self.simulator = RealisticFeedbackSimulator()
        self.detector = AdaptiveDeviationDetector()
        self.correction_engine = FeedbackCorrectionEngine(self.simulator)
        self.performance_monitor = deque(maxlen=1000)
        self.last_correction_time = 0
        self.min_correction_interval = 0.001  # 1ms - ultra-fast response
        
    def process_metrics_with_feedback(self, scenario_name: str = None) -> Dict:
        """Process metrics with realistic feedback loop"""
        # Set scenario if provided
        if scenario_name:
            self.simulator.simulate_scenario(scenario_name)
        
        # Get current metrics (with any active correction effects)
        metrics = self.simulator.get_current_metrics()
        
        start_time = time.time()
        
        # Detect deviations
        deviation_info = self.detector.detect_deviation(metrics)
        
        correction_applied = False
        correction_type = None
        correction_effectiveness = 0.0
        
        # Apply correction if needed with aggressive detection
        current_time = time.time()
        if (deviation_info.get('deviation_detected', False) and 
            current_time - self.last_correction_time >= self.min_correction_interval):
            
            # System resources (optimized for performance)
            system_resources = {'cpu_available': 0.9, 'memory_available': 0.8}
            
            # Select correction
            correction_info = self.correction_engine.select_optimal_correction(
                deviation_info, system_resources
            )
            
            # Apply multiple corrections for severe deviations
            if correction_info and deviation_info.get('severity', 0.0) > 0.6:
                # Apply primary correction
                success = self.correction_engine.apply_correction(correction_info)
                
                if success:
                    correction_applied = True
                    correction_type = correction_info['strategy']['type']
                    correction_effectiveness = correction_info['expected_improvement']
                    self.last_correction_time = current_time
                    
                    # Apply secondary correction for severe cases
                    time.sleep(0.0005)  # Brief delay
                    secondary_correction = self.correction_engine.select_optimal_correction(
                        deviation_info, system_resources
                    )
                    if secondary_correction and secondary_correction['strategy']['type'] != correction_type:
                        self.correction_engine.apply_correction(secondary_correction)
                    
                    self.detector.update_sensitivity(True)
                else:
                    self.detector.update_sensitivity(False)
            elif correction_info:
                # Single correction for moderate deviations
                success = self.correction_engine.apply_correction(correction_info)
                
                if success:
                    correction_applied = True
                    correction_type = correction_info['strategy']['type']
                    correction_effectiveness = correction_info['expected_improvement']
                    self.last_correction_time = current_time
                    self.detector.update_sensitivity(True)
                else:
                    self.detector.update_sensitivity(False)
        
        processing_time = time.time() - start_time
        
        # Record performance
        self.performance_monitor.append({
            'timestamp': metrics.timestamp,
            'latency': metrics.latency,
            'packet_loss': metrics.packet_loss,
            'throughput': metrics.throughput,
            'jitter': metrics.jitter,
            'correction_applied': correction_applied,
            'correction_type': correction_type,
            'processing_time': processing_time,
            'deviation_severity': deviation_info.get('severity', 0.0),
            'detection_confidence': deviation_info.get('confidence', 0.0)
        })
        
        return {
            'metrics': metrics,
            'deviation_info': deviation_info,
            'correction_applied': correction_applied,
            'correction_type': correction_type,
            'correction_effectiveness': correction_effectiveness,
            'processing_time': processing_time,
            'active_corrections': self.simulator.get_active_corrections_info()
        }
    
    def get_performance_summary(self) -> Dict:
        """Get comprehensive performance summary"""
        if len(self.performance_monitor) < 10:
            return {}
        
        data = list(self.performance_monitor)
        
        # Extract metrics
        latencies = [d['latency'] for d in data]
        packet_losses = [d['packet_loss'] for d in data]
        throughputs = [d['throughput'] for d in data]
        processing_times = [d['processing_time'] for d in data]
        
        # Calculate statistics
        def mean(lst): return sum(lst) / len(lst)
        def std_dev(lst): 
            m = mean(lst)
            return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
        def percentile(lst, p):
            sorted_lst = sorted(lst)
            k = (len(sorted_lst) - 1) * p / 100
            f, c = int(k), int(k) + 1
            if c >= len(sorted_lst): return sorted_lst[-1]
            return sorted_lst[f] + (k - f) * (sorted_lst[c] - sorted_lst[f])
        
        corrections_applied = sum(1 for d in data if d['correction_applied'])
        avg_confidence = mean([d['detection_confidence'] for d in data])
        correction_effectiveness = self.correction_engine.get_correction_effectiveness()
        
        return {
            'samples': len(data),
            'latency': {
                'mean': mean(latencies),
                'std': std_dev(latencies),
                'p99': percentile(latencies, 99)
            },
            'packet_loss': {
                'mean': mean(packet_losses),
                'std': std_dev(packet_losses)
            },
            'throughput': {
                'mean': mean(throughputs),
                'std': std_dev(throughputs)
            },
            'protocol_performance': {
                'corrections_applied': corrections_applied,
                'correction_rate': corrections_applied / len(data),
                'avg_processing_time': mean(processing_times),
                'avg_detection_confidence': avg_confidence,
                'correction_effectiveness': correction_effectiveness,
                'adaptive_sensitivity': self.detector.adaptive_sensitivity
            }
        }
    
    def reset_protocol(self):
        """Reset protocol state"""
        self.simulator.reset_corrections()
        self.performance_monitor.clear()
        self.detector = AdaptiveDeviationDetector()
        self.last_correction_time = 0
