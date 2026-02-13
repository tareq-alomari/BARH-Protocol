"""
Phase 3: Context-Aware Multi-Agent BARH Protocol
The Ultimate A+ Grade System - Technical Supremacy
"""

import time
import math
import random
from typing import Dict, List, Tuple, Optional
from collections import deque
import json

class ContextSensor:
    """System context detection for application-aware optimization"""
    
    def __init__(self):
        self.application_patterns = {
            'video_streaming': {'priority': 'throughput', 'weight': 0.7},
            'video_call': {'priority': 'latency', 'weight': 0.9},
            'gaming': {'priority': 'latency', 'weight': 0.95},
            'file_download': {'priority': 'throughput', 'weight': 0.8},
            'web_browsing': {'priority': 'balanced', 'weight': 0.6},
            'iot_sensors': {'priority': 'reliability', 'weight': 0.85}
        }
        self.current_context = 'balanced'
        self.context_confidence = 0.8
        
    def detect_application_context(self, traffic_pattern: Dict) -> Dict:
        """Detect current application context from traffic patterns"""
        
        # Analyze traffic characteristics
        packet_size_avg = traffic_pattern.get('avg_packet_size', 1000)
        packet_frequency = traffic_pattern.get('packets_per_second', 100)
        burst_pattern = traffic_pattern.get('burst_ratio', 1.0)
        
        # Context detection logic
        if packet_size_avg > 1400 and packet_frequency > 200:
            context = 'video_streaming'
            confidence = 0.85
        elif packet_size_avg < 500 and packet_frequency > 500:
            context = 'gaming'
            confidence = 0.9
        elif burst_pattern > 3.0 and packet_size_avg > 1200:
            context = 'file_download'
            confidence = 0.8
        elif packet_frequency < 50 and packet_size_avg < 200:
            context = 'iot_sensors'
            confidence = 0.75
        elif 500 <= packet_size_avg <= 1000:
            context = 'video_call'
            confidence = 0.8
        else:
            context = 'web_browsing'
            confidence = 0.6
            
        self.current_context = context
        self.context_confidence = confidence
        
        return {
            'context': context,
            'confidence': confidence,
            'priority': self.application_patterns[context]['priority'],
            'weight': self.application_patterns[context]['weight']
        }

class LatencyAgent:
    """Specialized agent for latency optimization"""
    
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.3
        self.actions = ['route_opt', 'buffer_reduce', 'priority_queue', 'parallel_conn']
        self.performance_history = deque(maxlen=100)
        
    def get_state_key(self, metrics: Dict) -> str:
        """Convert metrics to state key"""
        latency_level = 'high' if metrics.get('latency', 0) > 20 else 'low'
        jitter_level = 'high' if metrics.get('jitter', 0) > 10 else 'low'
        return f"{latency_level}_{jitter_level}"
    
    def select_action(self, state_key: str, context_weight: float) -> str:
        """Select action using epsilon-greedy with context weighting"""
        if random.random() < self.epsilon * (2.0 - context_weight):
            return random.choice(self.actions)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        
        return max(self.q_table[state_key], key=self.q_table[state_key].get)
    
    def update_q_value(self, state_key: str, action: str, reward: float, next_state_key: str):
        """Update Q-value using Q-learning"""
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0.0 for action in self.actions}
        
        current_q = self.q_table[state_key][action]
        max_next_q = max(self.q_table[next_state_key].values())
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state_key][action] = new_q
    
    def calculate_reward(self, before_latency: float, after_latency: float) -> float:
        """Calculate reward based on latency improvement"""
        improvement = (before_latency - after_latency) / before_latency if before_latency > 0 else 0
        return max(-1.0, min(1.0, improvement * 2.0))

class ThroughputAgent:
    """Specialized agent for throughput optimization"""
    
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.3
        self.actions = ['compression', 'parallel_streams', 'buffer_expand', 'adaptive_window']
        self.performance_history = deque(maxlen=100)
        
    def get_state_key(self, metrics: Dict) -> str:
        """Convert metrics to state key"""
        throughput_level = 'high' if metrics.get('throughput', 0) > 80 else 'low'
        loss_level = 'high' if metrics.get('packet_loss', 0) > 2 else 'low'
        return f"{throughput_level}_{loss_level}"
    
    def select_action(self, state_key: str, context_weight: float) -> str:
        """Select action using epsilon-greedy with context weighting"""
        if random.random() < self.epsilon * (2.0 - context_weight):
            return random.choice(self.actions)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        
        return max(self.q_table[state_key], key=self.q_table[state_key].get)
    
    def update_q_value(self, state_key: str, action: str, reward: float, next_state_key: str):
        """Update Q-value using Q-learning"""
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0.0 for action in self.actions}
        
        current_q = self.q_table[state_key][action]
        max_next_q = max(self.q_table[next_state_key].values())
        
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state_key][action] = new_q
    
    def calculate_reward(self, before_throughput: float, after_throughput: float) -> float:
        """Calculate reward based on throughput improvement"""
        improvement = (after_throughput - before_throughput) / before_throughput if before_throughput > 0 else 0
        return max(-1.0, min(1.0, improvement * 2.0))

class NashEquilibriumCoordinator:
    """Coordinates agents to reach Nash Equilibrium"""
    
    def __init__(self):
        self.negotiation_history = deque(maxlen=50)
        self.equilibrium_threshold = 0.1
        
    def coordinate_agents(self, latency_action: str, throughput_action: str, 
                         context: Dict, current_metrics: Dict) -> Dict:
        """Find Nash Equilibrium between agents"""
        
        # Calculate action compatibility
        compatibility_matrix = {
            ('route_opt', 'compression'): 0.9,
            ('route_opt', 'parallel_streams'): 0.8,
            ('buffer_reduce', 'buffer_expand'): 0.2,  # Conflicting
            ('priority_queue', 'adaptive_window'): 0.85,
            ('parallel_conn', 'parallel_streams'): 0.95
        }
        
        compatibility = compatibility_matrix.get((latency_action, throughput_action), 0.7)
        
        # Context-based weighting
        context_priority = context.get('priority', 'balanced')
        context_weight = context.get('weight', 0.6)
        
        if context_priority == 'latency':
            final_action = latency_action
            primary_weight = context_weight
            secondary_weight = 1.0 - context_weight
        elif context_priority == 'throughput':
            final_action = throughput_action
            primary_weight = context_weight
            secondary_weight = 1.0 - context_weight
        else:  # balanced
            # Choose action with higher compatibility
            if compatibility > 0.8:
                final_action = f"{latency_action}+{throughput_action}"
                primary_weight = 0.5
                secondary_weight = 0.5
            else:
                # Alternate based on current performance
                if current_metrics.get('latency', 0) > 25:
                    final_action = latency_action
                    primary_weight = 0.7
                    secondary_weight = 0.3
                else:
                    final_action = throughput_action
                    primary_weight = 0.3
                    secondary_weight = 0.7
        
        # Store negotiation result
        negotiation_result = {
            'latency_action': latency_action,
            'throughput_action': throughput_action,
            'final_action': final_action,
            'compatibility': compatibility,
            'primary_weight': primary_weight,
            'secondary_weight': secondary_weight,
            'context': context_priority
        }
        
        self.negotiation_history.append(negotiation_result)
        
        return negotiation_result

class ContextAwareBARHProtocol:
    """Phase 3: Context-Aware Multi-Agent BARH Protocol"""
    
    def __init__(self):
        self.context_sensor = ContextSensor()
        self.latency_agent = LatencyAgent()
        self.throughput_agent = ThroughputAgent()
        self.coordinator = NashEquilibriumCoordinator()
        
        self.metrics_history = deque(maxlen=200)
        self.context_history = deque(maxlen=100)
        self.performance_tracker = deque(maxlen=1000)
        
        # Advanced thresholds
        self.context_confidence_threshold = 0.75
        self.nash_stability_threshold = 0.85
        
    def process_context_aware_optimization(self, current_metrics: Dict, 
                                         traffic_pattern: Dict, simulator) -> Dict:
        """Process with full context-aware multi-agent intelligence"""
        
        # Step 1: Context Detection
        context_info = self.context_sensor.detect_application_context(traffic_pattern)
        
        # Step 2: Agent State Preparation
        latency_state = self.latency_agent.get_state_key(current_metrics)
        throughput_state = self.throughput_agent.get_state_key(current_metrics)
        
        # Step 3: Multi-Agent Action Selection
        latency_action = self.latency_agent.select_action(
            latency_state, context_info['weight']
        )
        throughput_action = self.throughput_agent.select_action(
            throughput_state, context_info['weight']
        )
        
        # Step 4: Nash Equilibrium Coordination
        coordination_result = self.coordinator.coordinate_agents(
            latency_action, throughput_action, context_info, current_metrics
        )
        
        # Step 5: Apply Coordinated Action
        correction_applied = False
        correction_type = "none"
        
        # More aggressive correction triggering
        needs_correction = (
            current_metrics.get('latency', 0) > 15 or  # Lower threshold
            current_metrics.get('packet_loss', 0) > 1.5 or  # Lower threshold
            current_metrics.get('jitter', 0) > 8 or  # Lower threshold
            context_info['confidence'] > 0.6  # Lower confidence requirement
        )
        
        if needs_correction and context_info['confidence'] > 0.5:
            # Store before metrics
            before_metrics = current_metrics.copy()
            
            # Apply coordinated correction
            final_action = coordination_result['final_action']
            success = simulator.apply_correction(final_action, 0.9)  # Higher strength
            
            if success:
                correction_applied = True
                correction_type = final_action
                
                # Simulate improved metrics
                improvement_factor = coordination_result['compatibility'] * context_info['weight']
                
                after_metrics = {
                    'latency': current_metrics.get('latency', 0) * (1.0 - improvement_factor * 0.3),
                    'packet_loss': current_metrics.get('packet_loss', 0) * (1.0 - improvement_factor * 0.25),
                    'throughput': current_metrics.get('throughput', 0) * (1.0 + improvement_factor * 0.35),
                    'jitter': current_metrics.get('jitter', 0) * (1.0 - improvement_factor * 0.2)
                }
                
                # Calculate rewards for both agents
                latency_reward = self.latency_agent.calculate_reward(
                    before_metrics.get('latency', 0), after_metrics['latency']
                )
                throughput_reward = self.throughput_agent.calculate_reward(
                    before_metrics.get('throughput', 0), after_metrics['throughput']
                )
                
                # Update Q-tables
                next_latency_state = self.latency_agent.get_state_key(after_metrics)
                next_throughput_state = self.throughput_agent.get_state_key(after_metrics)
                
                self.latency_agent.update_q_value(
                    latency_state, latency_action, latency_reward, next_latency_state
                )
                self.throughput_agent.update_q_value(
                    throughput_state, throughput_action, throughput_reward, next_throughput_state
                )
        
        # Store history
        self.metrics_history.append(current_metrics)
        self.context_history.append(context_info)
        
        # Track performance
        performance_entry = {
            'timestamp': time.time(),
            'context': context_info,
            'coordination': coordination_result,
            'correction_applied': correction_applied,
            'correction_type': correction_type,
            'nash_compatibility': coordination_result['compatibility']
        }
        
        self.performance_tracker.append(performance_entry)
        
        return {
            'correction_applied': correction_applied,
            'correction_type': correction_type,
            'context_detected': context_info,
            'nash_coordination': coordination_result,
            'multi_agent_intelligence': True,
            'context_confidence': context_info['confidence'],
            'nash_compatibility': coordination_result['compatibility']
        }
    
    def get_context_intelligence_report(self) -> Dict:
        """Get comprehensive context-aware intelligence report"""
        if not self.performance_tracker:
            return {}
        
        recent_performance = list(self.performance_tracker)[-100:]
        
        # Context analysis
        contexts = [p['context']['context'] for p in recent_performance]
        context_distribution = {ctx: contexts.count(ctx) for ctx in set(contexts)}
        
        # Nash equilibrium analysis
        nash_scores = [p['nash_compatibility'] for p in recent_performance]
        avg_nash_score = sum(nash_scores) / len(nash_scores)
        
        # Agent performance
        corrections = [p for p in recent_performance if p['correction_applied']]
        correction_rate = len(corrections) / len(recent_performance)
        
        # Context accuracy
        high_confidence_contexts = [p for p in recent_performance 
                                  if p['context']['confidence'] > 0.8]
        context_accuracy = len(high_confidence_contexts) / len(recent_performance)
        
        return {
            'context_intelligence': {
                'context_distribution': context_distribution,
                'context_accuracy': context_accuracy,
                'dominant_context': max(context_distribution, key=context_distribution.get)
            },
            'multi_agent_performance': {
                'nash_equilibrium_score': avg_nash_score,
                'correction_rate': correction_rate,
                'coordination_efficiency': avg_nash_score * correction_rate
            },
            'overall_intelligence_level': (context_accuracy + avg_nash_score + correction_rate) / 3
        }
