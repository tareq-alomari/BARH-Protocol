"""
Enhanced BARH Protocol - Phase 1: Stability Filter Integration
Advanced Kalman Filter for Network Stability Optimization
"""

import time
import math
from typing import Dict, List, Tuple, Optional
from collections import deque

class AdvancedKalmanFilter:
    """Advanced Kalman Filter for network stability prediction"""
    
    def __init__(self, dim=3):
        self.dim = dim
        # State vector: [latency, packet_loss, throughput]
        self.x = [0.0] * dim
        
        # Covariance matrix (simplified diagonal)
        self.P = [1.0] * dim
        
        # Process noise (tuned for network stability)
        self.Q = [0.005, 0.01, 0.008]  # Lower noise for stability
        
        # Measurement noise (adaptive)
        self.R = [0.05, 0.08, 0.06]
        
        # State transition (with momentum)
        self.momentum = [0.0] * dim
        self.momentum_factor = 0.7
        
    def predict_with_momentum(self):
        """Predict next state with momentum consideration"""
        for i in range(self.dim):
            # Apply momentum to prediction
            self.x[i] = self.x[i] + self.momentum[i] * self.momentum_factor
            
            # Update covariance with process noise
            self.P[i] += self.Q[i]
    
    def update_adaptive(self, measurement: List[float], confidence: float = 1.0):
        """Update with adaptive noise based on measurement confidence"""
        if len(measurement) != self.dim:
            return
        
        for i in range(self.dim):
            # Adaptive measurement noise based on confidence
            adaptive_R = self.R[i] / (confidence + 0.1)
            
            # Kalman gain
            K = self.P[i] / (self.P[i] + adaptive_R)
            
            # Innovation (prediction error)
            innovation = measurement[i] - self.x[i]
            
            # Update state
            old_x = self.x[i]
            self.x[i] = self.x[i] + K * innovation
            
            # Update momentum
            self.momentum[i] = (self.x[i] - old_x) * 0.3 + self.momentum[i] * 0.7
            
            # Update covariance
            self.P[i] = (1 - K) * self.P[i]
    
    def get_stabilized_prediction(self) -> List[float]:
        """Get stabilized prediction with confidence bounds"""
        return self.x.copy()
    
    def get_prediction_confidence(self) -> List[float]:
        """Get confidence levels for each metric"""
        return [1.0 / (1.0 + p) for p in self.P]

class StabilityFilter:
    """Network stability filter using advanced smoothing"""
    
    def __init__(self, window_size=20):
        self.window_size = window_size
        self.history = deque(maxlen=window_size)
        self.kalman_filter = AdvancedKalmanFilter()
        self.stability_threshold = 0.15  # 15% variation threshold
        
    def add_measurement(self, latency: float, packet_loss: float, throughput: float, confidence: float = 1.0):
        """Add new measurement and update stability filter"""
        measurement = [latency, packet_loss, throughput]
        
        # Update Kalman filter
        self.kalman_filter.predict_with_momentum()
        self.kalman_filter.update_adaptive(measurement, confidence)
        
        # Store in history
        self.history.append({
            'raw': measurement,
            'filtered': self.kalman_filter.get_stabilized_prediction(),
            'confidence': self.kalman_filter.get_prediction_confidence(),
            'timestamp': time.time()
        })
    
    def get_stabilized_metrics(self) -> Dict:
        """Get current stabilized metrics"""
        if not self.history:
            return {'latency': 0.0, 'packet_loss': 0.0, 'throughput': 0.0}
        
        filtered = self.kalman_filter.get_stabilized_prediction()
        confidence = self.kalman_filter.get_prediction_confidence()
        
        return {
            'latency': max(0.1, filtered[0]),
            'packet_loss': max(0.0, min(100.0, filtered[1])),
            'throughput': max(1.0, filtered[2]),
            'confidence': confidence,
            'stability_score': self._calculate_stability_score()
        }
    
    def _calculate_stability_score(self) -> float:
        """Calculate network stability score (0.0 to 1.0)"""
        if len(self.history) < 5:
            return 0.5
        
        # Get recent measurements
        recent = list(self.history)[-10:]
        
        # Calculate coefficient of variation for each metric
        metrics = ['latency', 'packet_loss', 'throughput']
        stability_scores = []
        
        for i, metric in enumerate(metrics):
            values = [h['filtered'][i] for h in recent]
            if len(values) < 2:
                continue
                
            mean_val = sum(values) / len(values)
            if mean_val == 0:
                continue
                
            variance = sum((x - mean_val) ** 2 for x in values) / len(values)
            cv = math.sqrt(variance) / mean_val  # Coefficient of variation
            
            # Convert to stability score (lower CV = higher stability)
            stability = max(0.0, 1.0 - cv / self.stability_threshold)
            stability_scores.append(stability)
        
        return sum(stability_scores) / len(stability_scores) if stability_scores else 0.5
    
    def predict_next_state(self, time_ahead_ms: float = 500.0) -> Dict:
        """Predict network state ahead of time (proactive prediction)"""
        if len(self.history) < 3:
            current = self.get_stabilized_metrics()
            return {
                'predicted_latency': current['latency'],
                'predicted_packet_loss': current['packet_loss'],
                'predicted_throughput': current['throughput'],
                'prediction_confidence': 0.5,
                'time_ahead_ms': time_ahead_ms
            }
        
        # Simple trend analysis for prediction
        recent = list(self.history)[-5:]
        
        # Calculate trends
        trends = [0.0, 0.0, 0.0]  # latency, packet_loss, throughput
        
        if len(recent) >= 2:
            for i in range(3):
                values = [h['filtered'][i] for h in recent]
                # Simple linear trend
                if len(values) >= 2:
                    trend = (values[-1] - values[0]) / len(values)
                    trends[i] = trend
        
        # Project forward
        current = self.kalman_filter.get_stabilized_prediction()
        time_factor = time_ahead_ms / 1000.0  # Convert to seconds
        
        predicted = [
            max(0.1, current[0] + trends[0] * time_factor),
            max(0.0, min(100.0, current[1] + trends[1] * time_factor)),
            max(1.0, current[2] + trends[2] * time_factor)
        ]
        
        return {
            'predicted_latency': predicted[0],
            'predicted_packet_loss': predicted[1],
            'predicted_throughput': predicted[2],
            'prediction_confidence': min(self.kalman_filter.get_prediction_confidence()),
            'time_ahead_ms': time_ahead_ms
        }

class ProactiveDeviationDetector:
    """Enhanced detector with proactive prediction capabilities"""
    
    def __init__(self, window_size=50):
        self.window_size = window_size
        self.stability_filter = StabilityFilter()
        self.adaptive_sensitivity = 0.8  # More sensitive for proactive detection
        self.learning_rate = 0.1
        self.prediction_horizon = 500.0  # 500ms ahead prediction
        
    def process_measurement(self, latency: float, packet_loss: float, throughput: float, 
                          ml_confidence: float = 0.5) -> Dict:
        """Process measurement with stability filtering and proactive detection"""
        
        # Add to stability filter
        self.stability_filter.add_measurement(latency, packet_loss, throughput, ml_confidence)
        
        # Get stabilized current state
        current_state = self.stability_filter.get_stabilized_metrics()
        
        # Get proactive prediction
        future_prediction = self.stability_filter.predict_next_state(self.prediction_horizon)
        
        # Detect current deviations (reactive)
        current_deviation = self._detect_current_deviation(current_state)
        
        # Detect future deviations (proactive)
        future_deviation = self._detect_future_deviation(future_prediction)
        
        # Combined decision
        deviation_detected = current_deviation['detected'] or future_deviation['detected']
        
        # Calculate combined severity
        severity = max(current_deviation['severity'], future_deviation['severity'])
        
        # Enhanced confidence calculation
        stability_bonus = current_state['stability_score'] * 0.3
        prediction_bonus = future_prediction['prediction_confidence'] * 0.2
        enhanced_confidence = ml_confidence + stability_bonus + prediction_bonus
        
        return {
            'deviation_detected': deviation_detected,
            'severity': severity,
            'confidence': min(0.95, enhanced_confidence),
            'current_state': current_state,
            'future_prediction': future_prediction,
            'proactive_mode': future_deviation['detected'] and not current_deviation['detected'],
            'stability_score': current_state['stability_score']
        }
    
    def _detect_current_deviation(self, state: Dict) -> Dict:
        """Detect current state deviations"""
        # Simple threshold-based detection with stability consideration
        latency_threshold = 20.0 * (2.0 - state['stability_score'])  # Adaptive threshold
        loss_threshold = 2.0 * (2.0 - state['stability_score'])
        
        lat_deviation = state['latency'] > latency_threshold
        loss_deviation = state['packet_loss'] > loss_threshold
        
        detected = lat_deviation or loss_deviation
        severity = 0.0
        
        if detected:
            lat_severity = max(0, (state['latency'] - latency_threshold) / latency_threshold)
            loss_severity = max(0, (state['packet_loss'] - loss_threshold) / loss_threshold)
            severity = min(1.0, 0.6 * lat_severity + 0.4 * loss_severity)
        
        return {'detected': detected, 'severity': severity}
    
    def _detect_future_deviation(self, prediction: Dict) -> Dict:
        """Detect predicted future deviations (proactive)"""
        # More aggressive thresholds for proactive detection
        future_lat_threshold = 15.0  # Lower threshold for early detection
        future_loss_threshold = 1.5
        
        lat_deviation = prediction['predicted_latency'] > future_lat_threshold
        loss_deviation = prediction['predicted_packet_loss'] > future_loss_threshold
        
        detected = lat_deviation or loss_deviation
        severity = 0.0
        
        if detected:
            # Weight by prediction confidence
            confidence_factor = prediction['prediction_confidence']
            
            lat_severity = max(0, (prediction['predicted_latency'] - future_lat_threshold) / future_lat_threshold)
            loss_severity = max(0, (prediction['predicted_packet_loss'] - future_loss_threshold) / future_loss_threshold)
            
            severity = min(1.0, confidence_factor * (0.6 * lat_severity + 0.4 * loss_severity))
        
        return {'detected': detected, 'severity': severity}
