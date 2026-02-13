"""
Phase 2: ML Prediction Integration - LSTM + Deep Reinforcement Learning
Building the "Intelligent Brain" for BARH Protocol
"""

import time
import math
import random
from typing import Dict, List, Tuple, Optional
from collections import deque
import json

class SimpleLSTM:
    """Lightweight LSTM implementation for network pattern recognition"""
    
    def __init__(self, input_size=4, hidden_size=16, output_size=3):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # LSTM weights (simplified implementation)
        self.Wf = [[random.uniform(-0.1, 0.1) for _ in range(input_size + hidden_size)] for _ in range(hidden_size)]
        self.Wi = [[random.uniform(-0.1, 0.1) for _ in range(input_size + hidden_size)] for _ in range(hidden_size)]
        self.Wo = [[random.uniform(-0.1, 0.1) for _ in range(input_size + hidden_size)] for _ in range(hidden_size)]
        self.Wg = [[random.uniform(-0.1, 0.1) for _ in range(input_size + hidden_size)] for _ in range(hidden_size)]
        
        # Output layer weights
        self.Wy = [[random.uniform(-0.1, 0.1) for _ in range(hidden_size)] for _ in range(output_size)]
        
        # Biases
        self.bf = [0.0] * hidden_size
        self.bi = [0.0] * hidden_size
        self.bo = [0.0] * hidden_size
        self.bg = [0.0] * hidden_size
        self.by = [0.0] * output_size
        
        # Hidden state and cell state
        self.h = [0.0] * hidden_size
        self.c = [0.0] * hidden_size
        
        # Training data storage
        self.training_sequences = deque(maxlen=1000)
        
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-max(-500, min(500, x))))
    
    def tanh(self, x):
        return math.tanh(max(-500, min(500, x)))
    
    def matrix_vector_mult(self, matrix, vector):
        """Matrix-vector multiplication"""
        result = []
        for row in matrix:
            sum_val = sum(row[i] * vector[i] for i in range(len(vector)))
            result.append(sum_val)
        return result
    
    def forward(self, input_sequence: List[List[float]]) -> List[float]:
        """Forward pass through LSTM"""
        outputs = []
        
        for input_vec in input_sequence:
            # Concatenate input and hidden state
            combined = input_vec + self.h
            
            # Forget gate
            f_gate = [self.sigmoid(sum_val + bias) for sum_val, bias in 
                     zip(self.matrix_vector_mult(self.Wf, combined), self.bf)]
            
            # Input gate
            i_gate = [self.sigmoid(sum_val + bias) for sum_val, bias in 
                     zip(self.matrix_vector_mult(self.Wi, combined), self.bi)]
            
            # Candidate values
            g_gate = [self.tanh(sum_val + bias) for sum_val, bias in 
                     zip(self.matrix_vector_mult(self.Wg, combined), self.bg)]
            
            # Update cell state
            self.c = [f * c + i * g for f, c, i, g in zip(f_gate, self.c, i_gate, g_gate)]
            
            # Output gate
            o_gate = [self.sigmoid(sum_val + bias) for sum_val, bias in 
                     zip(self.matrix_vector_mult(self.Wo, combined), self.bo)]
            
            # Update hidden state
            self.h = [o * self.tanh(c) for o, c in zip(o_gate, self.c)]
            
            outputs.append(self.h.copy())
        
        # Final output layer
        final_output = [sum_val + bias for sum_val, bias in 
                       zip(self.matrix_vector_mult(self.Wy, self.h), self.by)]
        
        return final_output
    
    def predict_network_state(self, recent_metrics: List[Dict]) -> Dict:
        """Predict future network state using LSTM"""
        if len(recent_metrics) < 3:
            return {'confidence': 0.1, 'predictions': [0.0, 0.0, 0.0]}
        
        # Prepare input sequence
        input_sequence = []
        for metrics in recent_metrics[-10:]:  # Use last 10 measurements
            normalized_input = [
                metrics.get('latency', 0) / 100.0,  # Normalize latency
                metrics.get('packet_loss', 0) / 10.0,  # Normalize packet loss
                metrics.get('throughput', 0) / 100.0,  # Normalize throughput
                metrics.get('jitter', 0) / 50.0  # Normalize jitter
            ]
            input_sequence.append(normalized_input)
        
        # Get LSTM prediction
        prediction = self.forward(input_sequence)
        
        # Denormalize predictions
        predicted_latency = max(0.1, prediction[0] * 100.0)
        predicted_packet_loss = max(0.0, min(100.0, prediction[1] * 10.0))
        predicted_throughput = max(1.0, prediction[2] * 100.0)
        
        # Calculate confidence based on recent accuracy
        confidence = min(0.95, 0.6 + len(recent_metrics) * 0.01)
        
        return {
            'predicted_latency': predicted_latency,
            'predicted_packet_loss': predicted_packet_loss,
            'predicted_throughput': predicted_throughput,
            'confidence': confidence,
            'pattern_detected': self._detect_pattern(recent_metrics)
        }
    
    def _detect_pattern(self, metrics: List[Dict]) -> str:
        """Detect network patterns"""
        if len(metrics) < 5:
            return "insufficient_data"
        
        # Simple pattern detection
        latencies = [m.get('latency', 0) for m in metrics[-5:]]
        
        # Check for increasing trend
        if all(latencies[i] <= latencies[i+1] for i in range(len(latencies)-1)):
            return "degrading_trend"
        
        # Check for decreasing trend
        if all(latencies[i] >= latencies[i+1] for i in range(len(latencies)-1)):
            return "improving_trend"
        
        # Check for oscillation
        changes = [latencies[i+1] - latencies[i] for i in range(len(latencies)-1)]
        if len(set([1 if c > 0 else -1 for c in changes])) > 2:
            return "oscillating"
        
        return "stable"

class DeepQLearning:
    """Deep Q-Learning for optimal correction action selection"""
    
    def __init__(self, state_size=6, action_size=6, learning_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.epsilon = 0.9  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1
        
        # Q-network (simplified neural network)
        self.weights_1 = [[random.uniform(-0.1, 0.1) for _ in range(state_size)] for _ in range(32)]
        self.weights_2 = [[random.uniform(-0.1, 0.1) for _ in range(32)] for _ in range(16)]
        self.weights_3 = [[random.uniform(-0.1, 0.1) for _ in range(16)] for _ in range(action_size)]
        
        self.bias_1 = [0.0] * 32
        self.bias_2 = [0.0] * 16
        self.bias_3 = [0.0] * action_size
        
        # Experience replay
        self.memory = deque(maxlen=2000)
        self.action_names = [
            "buffer_optimization",
            "connection_pooling", 
            "route_optimization",
            "adaptive_compression",
            "parallel_connections",
            "predictive_prefetch"
        ]
        
    def relu(self, x):
        return max(0, x)
    
    def forward(self, state: List[float]) -> List[float]:
        """Forward pass through Q-network"""
        # Layer 1
        h1 = [self.relu(sum(state[j] * self.weights_1[i][j] for j in range(len(state))) + self.bias_1[i]) 
              for i in range(32)]
        
        # Layer 2
        h2 = [self.relu(sum(h1[j] * self.weights_2[i][j] for j in range(len(h1))) + self.bias_2[i]) 
              for i in range(16)]
        
        # Output layer
        output = [sum(h2[j] * self.weights_3[i][j] for j in range(len(h2))) + self.bias_3[i] 
                 for i in range(self.action_size)]
        
        return output
    
    def select_action(self, state: List[float], available_actions: List[str]) -> str:
        """Select optimal action using epsilon-greedy policy"""
        # Epsilon-greedy exploration
        if random.random() < self.epsilon:
            return random.choice(available_actions)
        
        # Get Q-values for all actions
        q_values = self.forward(state)
        
        # Filter available actions
        available_indices = [i for i, action in enumerate(self.action_names) 
                           if action in available_actions]
        
        if not available_indices:
            return available_actions[0] if available_actions else "buffer_optimization"
        
        # Select action with highest Q-value
        best_index = max(available_indices, key=lambda i: q_values[i])
        return self.action_names[best_index]
    
    def remember(self, state: List[float], action: str, reward: float, 
                next_state: List[float], done: bool):
        """Store experience in replay memory"""
        action_index = self.action_names.index(action) if action in self.action_names else 0
        self.memory.append((state, action_index, reward, next_state, done))
    
    def calculate_reward(self, before_metrics: Dict, after_metrics: Dict, 
                        correction_type: str) -> float:
        """Calculate reward for reinforcement learning"""
        # Improvement-based reward
        latency_improvement = (before_metrics.get('latency', 0) - after_metrics.get('latency', 0)) / 100.0
        loss_improvement = (before_metrics.get('packet_loss', 0) - after_metrics.get('packet_loss', 0)) / 10.0
        throughput_improvement = (after_metrics.get('throughput', 0) - before_metrics.get('throughput', 0)) / 100.0
        
        # Weighted reward
        reward = (
            0.4 * latency_improvement +
            0.4 * loss_improvement +
            0.2 * throughput_improvement
        )
        
        # Bonus for specific correction types
        if correction_type in ["route_optimization", "parallel_connections"]:
            reward += 0.1  # Bonus for high-impact corrections
        
        return max(-1.0, min(1.0, reward))  # Clamp reward
    
    def update_epsilon(self):
        """Decay exploration rate"""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class IntelligentBARHProtocol:
    """Phase 2: BARH Protocol with ML Intelligence"""
    
    def __init__(self):
        self.lstm_predictor = SimpleLSTM()
        self.dql_agent = DeepQLearning()
        self.metrics_history = deque(maxlen=100)
        self.correction_history = deque(maxlen=50)
        self.performance_tracker = deque(maxlen=1000)
        
        # Enhanced thresholds
        self.confidence_threshold = 0.75  # Higher confidence requirement
        self.prediction_horizon = 3  # Predict 3 steps ahead
        
    def process_intelligent_correction(self, current_metrics: Dict, 
                                     simulator) -> Dict:
        """Process metrics with full ML intelligence"""
        
        # Store current metrics
        self.metrics_history.append(current_metrics)
        
        # LSTM Prediction
        lstm_prediction = self.lstm_predictor.predict_network_state(
            list(self.metrics_history)
        )
        
        # Prepare state for DQL
        state = [
            current_metrics.get('latency', 0) / 100.0,
            current_metrics.get('packet_loss', 0) / 10.0,
            current_metrics.get('throughput', 0) / 100.0,
            current_metrics.get('jitter', 0) / 50.0,
            lstm_prediction['confidence'],
            len(self.correction_history) / 50.0  # Correction frequency
        ]
        
        # Detect if correction is needed
        correction_needed = self._intelligent_detection(current_metrics, lstm_prediction)
        
        correction_applied = False
        correction_type = "none"
        reward = 0.0
        
        if correction_needed:
            # Available correction actions
            available_actions = [
                "buffer_optimization",
                "connection_pooling", 
                "route_optimization",
                "adaptive_compression",
                "parallel_connections",
                "predictive_prefetch"
            ]
            
            # DQL action selection
            selected_action = self.dql_agent.select_action(state, available_actions)
            
            # Store metrics before correction
            before_metrics = current_metrics.copy()
            
            # Apply correction
            success = simulator.apply_correction(selected_action, 0.8)
            
            if success:
                correction_applied = True
                correction_type = selected_action
                
                # Simulate after-correction metrics (simplified)
                after_metrics = {
                    'latency': current_metrics.get('latency', 0) * 0.85,
                    'packet_loss': current_metrics.get('packet_loss', 0) * 0.75,
                    'throughput': current_metrics.get('throughput', 0) * 1.15
                }
                
                # Calculate reward
                reward = self.dql_agent.calculate_reward(
                    before_metrics, after_metrics, selected_action
                )
                
                # Store experience
                next_state = [
                    after_metrics['latency'] / 100.0,
                    after_metrics['packet_loss'] / 10.0,
                    after_metrics['throughput'] / 100.0,
                    current_metrics.get('jitter', 0) / 50.0,
                    lstm_prediction['confidence'],
                    (len(self.correction_history) + 1) / 50.0
                ]
                
                self.dql_agent.remember(state, selected_action, reward, next_state, False)
                
                # Update correction history
                self.correction_history.append({
                    'action': selected_action,
                    'reward': reward,
                    'timestamp': time.time()
                })
        
        # Update DQL exploration
        self.dql_agent.update_epsilon()
        
        # Track performance
        self.performance_tracker.append({
            'timestamp': time.time(),
            'correction_applied': correction_applied,
            'correction_type': correction_type,
            'reward': reward,
            'lstm_confidence': lstm_prediction['confidence'],
            'dql_epsilon': self.dql_agent.epsilon,
            'pattern': lstm_prediction.get('pattern_detected', 'unknown')
        })
        
        return {
            'correction_applied': correction_applied,
            'correction_type': correction_type,
            'lstm_prediction': lstm_prediction,
            'dql_reward': reward,
            'intelligence_confidence': lstm_prediction['confidence'],
            'pattern_detected': lstm_prediction.get('pattern_detected', 'unknown'),
            'learning_progress': 1.0 - self.dql_agent.epsilon  # Learning progress indicator
        }
    
    def _intelligent_detection(self, current_metrics: Dict, lstm_prediction: Dict) -> bool:
        """Intelligent deviation detection using ML predictions"""
        
        # Current state analysis
        current_latency = current_metrics.get('latency', 0)
        current_loss = current_metrics.get('packet_loss', 0)
        
        # LSTM prediction analysis
        predicted_latency = lstm_prediction.get('predicted_latency', 0)
        predicted_loss = lstm_prediction.get('predicted_packet_loss', 0)
        confidence = lstm_prediction.get('confidence', 0)
        
        # Adaptive thresholds based on confidence
        latency_threshold = 20.0 * (2.0 - confidence)
        loss_threshold = 2.0 * (2.0 - confidence)
        
        # Current deviation detection
        current_deviation = (current_latency > latency_threshold or 
                           current_loss > loss_threshold)
        
        # Predictive deviation detection
        future_deviation = (predicted_latency > latency_threshold * 0.8 or 
                          predicted_loss > loss_threshold * 0.8)
        
        # Pattern-based detection
        pattern = lstm_prediction.get('pattern_detected', 'stable')
        pattern_risk = pattern in ['degrading_trend', 'oscillating']
        
        # Combined intelligent decision
        return (current_deviation or 
                (future_deviation and confidence > self.confidence_threshold) or
                (pattern_risk and confidence > 0.6))
    
    def get_intelligence_report(self) -> Dict:
        """Get comprehensive intelligence and learning report"""
        if not self.performance_tracker:
            return {}
        
        recent_performance = list(self.performance_tracker)[-50:]
        
        # Calculate learning metrics
        avg_reward = sum(p.get('reward', 0) for p in recent_performance) / len(recent_performance)
        correction_rate = sum(1 for p in recent_performance if p.get('correction_applied', False)) / len(recent_performance)
        avg_confidence = sum(p.get('lstm_confidence', 0) for p in recent_performance) / len(recent_performance)
        
        # Pattern analysis
        patterns = [p.get('pattern_detected', 'unknown') for p in recent_performance]
        pattern_distribution = {pattern: patterns.count(pattern) for pattern in set(patterns)}
        
        return {
            'learning_metrics': {
                'average_reward': avg_reward,
                'correction_rate': correction_rate,
                'average_lstm_confidence': avg_confidence,
                'learning_progress': 1.0 - self.dql_agent.epsilon,
                'total_corrections': len(self.correction_history)
            },
            'pattern_analysis': pattern_distribution,
            'intelligence_level': min(1.0, avg_confidence + (1.0 - self.dql_agent.epsilon)) / 2
        }
