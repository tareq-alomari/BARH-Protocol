"""
BARH Protocol - Ultimate Hybrid System
Combining Best of All Phases for A+ Achievement
"""

import time
import math
import random
from typing import Dict, List, Tuple, Optional
from collections import deque
import json

class HybridBARHProtocol:
    """Ultimate BARH combining Phase 1 stability + Phase 2 ML + Phase 3 context"""
    
    def __init__(self):
        # Phase 1: Stability components
        self.stability_threshold = 0.15
        self.momentum_factor = 0.3
        
        # Phase 2: ML components  
        self.ml_confidence_threshold = 0.7
        self.learning_rate = 0.1
        self.q_values = {}
        
        # Phase 3: Context awareness
        self.context_patterns = {
            'video_streaming': {'latency_weight': 0.3, 'throughput_weight': 0.7},
            'gaming': {'latency_weight': 0.9, 'throughput_weight': 0.1},
            'video_call': {'latency_weight': 0.8, 'throughput_weight': 0.2},
            'file_download': {'latency_weight': 0.2, 'throughput_weight': 0.8},
            'balanced': {'latency_weight': 0.5, 'throughput_weight': 0.5}
        }
        
        # Unified tracking
        self.metrics_history = deque(maxlen=100)
        self.correction_history = deque(maxlen=50)
        self.performance_tracker = deque(maxlen=1000)
        
        # Hybrid correction actions
        self.correction_actions = [
            'stability_filter',      # Phase 1
            'kalman_prediction',     # Phase 1  
            'ml_optimization',       # Phase 2
            'context_adaptation',    # Phase 3
            'hybrid_correction'      # Combined
        ]
        
    def detect_context(self, traffic_pattern: Dict) -> str:
        """Simple but effective context detection"""
        packet_size = traffic_pattern.get('avg_packet_size', 1000)
        frequency = traffic_pattern.get('packets_per_second', 100)
        
        if packet_size > 1400 and frequency > 200:
            return 'video_streaming'
        elif packet_size < 500 and frequency > 400:
            return 'gaming'
        elif 500 <= packet_size <= 1000 and frequency > 150:
            return 'video_call'
        elif packet_size > 1200:
            return 'file_download'
        else:
            return 'balanced'
    
    def calculate_stability_score(self, recent_metrics: List[Dict]) -> float:
        """Phase 1: Calculate network stability"""
        if len(recent_metrics) < 3:
            return 0.5
        
        latencies = [m.get('latency', 0) for m in recent_metrics[-5:]]
        if not latencies:
            return 0.5
            
        mean_latency = sum(latencies) / len(latencies)
        variance = sum((l - mean_latency) ** 2 for l in latencies) / len(latencies)
        coefficient_of_variation = math.sqrt(variance) / mean_latency if mean_latency > 0 else 1.0
        
        stability_score = max(0.0, 1.0 - coefficient_of_variation)
        return min(1.0, stability_score)
    
    def predict_future_state(self, recent_metrics: List[Dict]) -> Dict:
        """Phase 2: ML-based prediction"""
        if len(recent_metrics) < 3:
            return {'confidence': 0.3, 'predicted_latency': 20.0}
        
        # Simple trend analysis
        latencies = [m.get('latency', 0) for m in recent_metrics[-3:]]
        trend = (latencies[-1] - latencies[0]) / len(latencies)
        
        predicted_latency = latencies[-1] + trend
        confidence = min(0.9, 0.5 + len(recent_metrics) * 0.01)
        
        return {
            'predicted_latency': max(1.0, predicted_latency),
            'confidence': confidence,
            'trend': 'increasing' if trend > 0 else 'decreasing'
        }
    
    def select_hybrid_action(self, current_metrics: Dict, context: str, 
                           stability_score: float, ml_prediction: Dict) -> str:
        """Select best action combining all phases"""
        
        # Context weights
        context_weights = self.context_patterns.get(context, self.context_patterns['balanced'])
        
        # Current state analysis
        current_latency = current_metrics.get('latency', 0)
        current_loss = current_metrics.get('packet_loss', 0)
        
        # Decision logic combining all phases
        if stability_score < 0.3:
            # Phase 1: Stability critical
            return 'stability_filter'
        elif ml_prediction['confidence'] > 0.8 and ml_prediction['predicted_latency'] > 25:
            # Phase 2: ML prediction critical
            return 'ml_optimization'
        elif context in ['gaming', 'video_call'] and current_latency > 20:
            # Phase 3: Context critical
            return 'context_adaptation'
        elif current_latency > 30 or current_loss > 5:
            # Emergency: Hybrid approach
            return 'hybrid_correction'
        else:
            # Proactive: Kalman prediction
            return 'kalman_prediction'
    
    def apply_hybrid_correction(self, action: str, current_metrics: Dict, 
                              context: str, simulator) -> Dict:
        """Apply correction with hybrid intelligence"""
        
        correction_strength = 0.8  # Base strength
        
        # Adjust strength based on action type
        strength_multipliers = {
            'stability_filter': 0.7,
            'kalman_prediction': 0.6,
            'ml_optimization': 0.9,
            'context_adaptation': 0.8,
            'hybrid_correction': 1.0
        }
        
        final_strength = correction_strength * strength_multipliers.get(action, 0.8)
        
        # Apply correction
        success = simulator.apply_correction(action, final_strength)
        
        if success:
            # Calculate expected improvement based on action type
            improvement_factors = {
                'stability_filter': {'latency': 0.25, 'loss': 0.20, 'throughput': 0.15},
                'kalman_prediction': {'latency': 0.30, 'loss': 0.15, 'throughput': 0.20},
                'ml_optimization': {'latency': 0.35, 'loss': 0.25, 'throughput': 0.30},
                'context_adaptation': {'latency': 0.40, 'loss': 0.20, 'throughput': 0.35},
                'hybrid_correction': {'latency': 0.45, 'loss': 0.30, 'throughput': 0.40}
            }
            
            factors = improvement_factors.get(action, improvement_factors['stability_filter'])
            
            # Context-based adjustment
            context_weights = self.context_patterns.get(context, self.context_patterns['balanced'])
            
            if context_weights['latency_weight'] > 0.7:
                factors['latency'] *= 1.2  # Boost latency improvement for latency-critical contexts
            if context_weights['throughput_weight'] > 0.7:
                factors['throughput'] *= 1.2  # Boost throughput for throughput-critical contexts
            
            return {
                'success': True,
                'expected_improvements': factors,
                'action_type': action,
                'context_optimized': context
            }
        
        return {'success': False, 'action_type': action}
    
    def process_hybrid_optimization(self, current_metrics: Dict, 
                                  traffic_pattern: Dict, simulator) -> Dict:
        """Main hybrid processing function"""
        
        # Store metrics
        self.metrics_history.append(current_metrics)
        
        # Phase 1: Stability analysis
        stability_score = self.calculate_stability_score(list(self.metrics_history))
        
        # Phase 2: ML prediction
        ml_prediction = self.predict_future_state(list(self.metrics_history))
        
        # Phase 3: Context detection
        context = self.detect_context(traffic_pattern)
        
        # Hybrid decision making
        needs_correction = (
            current_metrics.get('latency', 0) > 18 or
            current_metrics.get('packet_loss', 0) > 2.0 or
            stability_score < 0.4 or
            (ml_prediction['confidence'] > 0.7 and ml_prediction['predicted_latency'] > 22)
        )
        
        correction_applied = False
        correction_result = {}
        
        if needs_correction:
            # Select hybrid action
            selected_action = self.select_hybrid_action(
                current_metrics, context, stability_score, ml_prediction
            )
            
            # Apply correction
            correction_result = self.apply_hybrid_correction(
                selected_action, current_metrics, context, simulator
            )
            
            correction_applied = correction_result.get('success', False)
            
            if correction_applied:
                self.correction_history.append({
                    'action': selected_action,
                    'context': context,
                    'stability_score': stability_score,
                    'ml_confidence': ml_prediction['confidence'],
                    'timestamp': time.time()
                })
        
        # Track performance
        performance_entry = {
            'timestamp': time.time(),
            'correction_applied': correction_applied,
            'action_type': correction_result.get('action_type', 'none'),
            'context': context,
            'stability_score': stability_score,
            'ml_confidence': ml_prediction['confidence'],
            'hybrid_intelligence': True
        }
        
        self.performance_tracker.append(performance_entry)
        
        return {
            'correction_applied': correction_applied,
            'correction_type': correction_result.get('action_type', 'none'),
            'context_detected': context,
            'stability_score': stability_score,
            'ml_prediction': ml_prediction,
            'hybrid_intelligence_active': True,
            'expected_improvements': correction_result.get('expected_improvements', {}),
            'phase_integration': 'All phases active'
        }
    
    def get_hybrid_performance_report(self) -> Dict:
        """Get comprehensive hybrid performance report"""
        if not self.performance_tracker:
            return {}
        
        recent_performance = list(self.performance_tracker)[-100:]
        
        # Calculate metrics
        corrections = [p for p in recent_performance if p['correction_applied']]
        correction_rate = len(corrections) / len(recent_performance)
        
        # Action distribution
        actions = [p['action_type'] for p in corrections]
        action_distribution = {action: actions.count(action) for action in set(actions)}
        
        # Context distribution
        contexts = [p['context'] for p in recent_performance]
        context_distribution = {ctx: contexts.count(ctx) for ctx in set(contexts)}
        
        # Average scores
        avg_stability = sum(p['stability_score'] for p in recent_performance) / len(recent_performance)
        avg_ml_confidence = sum(p['ml_confidence'] for p in recent_performance) / len(recent_performance)
        
        return {
            'hybrid_performance': {
                'correction_rate': correction_rate,
                'total_corrections': len(self.correction_history),
                'average_stability_score': avg_stability,
                'average_ml_confidence': avg_ml_confidence
            },
            'action_distribution': action_distribution,
            'context_distribution': context_distribution,
            'hybrid_intelligence_level': (avg_stability + avg_ml_confidence + correction_rate) / 3
        }
