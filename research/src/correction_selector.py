"""
BARH Protocol - Correction Selector (Algorithm 3)
خوارزمية اختيار التصحيح - الخوارزمية الثالثة
"""

import time
from typing import List, Optional, Dict
from data_structures import Deviation, CorrectionAction, CorrectionType
from config import *

class CorrectionSelector:
    """محدد التصحيحات - ينفذ الخوارزمية الثالثة من BARH"""
    
    def __init__(self):
        self.action_database = self._initialize_action_database()
        self.selection_history = []
        
    def select_correction(self, deviations: List[Deviation], 
                         available_resources: Dict[str, float]) -> Optional[CorrectionAction]:
        """اختيار أفضل إجراء تصحيحي بناءً على الانحرافات والموارد المتاحة"""
        
        if not deviations:
            return None
        
        # Get possible actions for the detected deviations
        possible_actions = self._get_possible_actions(deviations)
        
        if not possible_actions:
            return None
        
        # Calculate priorities for each action
        prioritized_actions = []
        for action in possible_actions:
            priority = self._calculate_priority(action, deviations, available_resources)
            if priority > 0:  # Only consider viable actions
                prioritized_actions.append((action, priority))
        
        if not prioritized_actions:
            return None
        
        # Sort by priority (highest first)
        prioritized_actions.sort(key=lambda x: x[1], reverse=True)
        
        # Select the highest priority action
        selected_action = prioritized_actions[0][0]
        
        # Record selection
        self.selection_history.append({
            "action": selected_action,
            "deviations": deviations,
            "priority": prioritized_actions[0][1],
            "timestamp": time.time()
        })
        
        return selected_action
    
    def _initialize_action_database(self) -> Dict[str, List[CorrectionAction]]:
        """تهيئة قاعدة بيانات الإجراءات التصحيحية"""
        
        database = {
            "latency": [
                CorrectionAction(
                    action_type=CorrectionType.BUFFER_OPTIMIZATION,
                    parameters={"buffer_size": 65536, "optimization_level": "aggressive"},
                    priority=0.8,
                    estimated_time=2.0,  # 2ms
                    resource_cost=0.3
                ),
                CorrectionAction(
                    action_type=CorrectionType.TIMEOUT_ADJUSTMENT,
                    parameters={"timeout_ms": 5000, "adjustment_factor": 0.8},
                    priority=0.6,
                    estimated_time=1.0,  # 1ms
                    resource_cost=0.1
                ),
                CorrectionAction(
                    action_type=CorrectionType.INTERFACE_SWITCH,
                    parameters={"target_interface": "alternative", "switch_threshold": 0.7},
                    priority=0.9,
                    estimated_time=3.0,  # 3ms
                    resource_cost=0.5
                )
            ],
            
            "packet_loss": [
                CorrectionAction(
                    action_type=CorrectionType.RETRANSMISSION_CONTROL,
                    parameters={"max_retries": 5, "backoff_factor": 1.5},
                    priority=0.9,
                    estimated_time=1.5,  # 1.5ms
                    resource_cost=0.4
                ),
                CorrectionAction(
                    action_type=CorrectionType.BUFFER_OPTIMIZATION,
                    parameters={"buffer_size": 131072, "optimization_level": "moderate"},
                    priority=0.7,
                    estimated_time=2.0,  # 2ms
                    resource_cost=0.3
                ),
                CorrectionAction(
                    action_type=CorrectionType.INTERFACE_SWITCH,
                    parameters={"target_interface": "alternative", "switch_threshold": 0.5},
                    priority=0.8,
                    estimated_time=3.0,  # 3ms
                    resource_cost=0.5
                )
            ],
            
            "throughput": [
                CorrectionAction(
                    action_type=CorrectionType.BUFFER_OPTIMIZATION,
                    parameters={"buffer_size": 262144, "optimization_level": "throughput"},
                    priority=0.8,
                    estimated_time=2.5,  # 2.5ms
                    resource_cost=0.4
                ),
                CorrectionAction(
                    action_type=CorrectionType.INTERFACE_SWITCH,
                    parameters={"target_interface": "high_bandwidth", "switch_threshold": 0.6},
                    priority=0.9,
                    estimated_time=3.0,  # 3ms
                    resource_cost=0.5
                ),
                CorrectionAction(
                    action_type=CorrectionType.TIMEOUT_ADJUSTMENT,
                    parameters={"timeout_ms": 10000, "adjustment_factor": 1.2},
                    priority=0.5,
                    estimated_time=1.0,  # 1ms
                    resource_cost=0.1
                )
            ]
        }
        
        return database
    
    def _get_possible_actions(self, deviations: List[Deviation]) -> List[CorrectionAction]:
        """الحصول على الإجراءات الممكنة للانحرافات المكتشفة"""
        possible_actions = []
        
        for deviation in deviations:
            if deviation.metric_type in self.action_database:
                actions = self.action_database[deviation.metric_type]
                possible_actions.extend(actions)
        
        # Remove duplicates based on action type
        unique_actions = {}
        for action in possible_actions:
            key = action.action_type.value
            if key not in unique_actions or action.priority > unique_actions[key].priority:
                unique_actions[key] = action
        
        return list(unique_actions.values())
    
    def _calculate_priority(self, action: CorrectionAction, deviations: List[Deviation],
                          available_resources: Dict[str, float]) -> float:
        """حساب أولوية الإجراء التصحيحي"""
        
        # Base priority from action definition
        base_priority = action.priority
        
        # Effectiveness score based on deviation severity
        effectiveness_score = self._calculate_effectiveness_score(action, deviations)
        
        # Resource availability score
        resource_score = self._calculate_resource_score(action, available_resources)
        
        # Time constraint score (prefer faster actions)
        time_score = self._calculate_time_score(action)
        
        # Weighted combination
        weights = {
            "effectiveness": 0.4,
            "resource": 0.3,
            "time": 0.2,
            "base": 0.1
        }
        
        total_priority = (
            weights["effectiveness"] * effectiveness_score +
            weights["resource"] * resource_score +
            weights["time"] * time_score +
            weights["base"] * base_priority
        )
        
        return max(0.0, min(1.0, total_priority))  # Clamp to [0, 1]
    
    def _calculate_effectiveness_score(self, action: CorrectionAction, 
                                     deviations: List[Deviation]) -> float:
        """حساب نقاط الفعالية بناءً على شدة الانحراف"""
        
        # Find the most severe deviation that this action can address
        max_severity = 0.0
        
        for deviation in deviations:
            if self._action_addresses_deviation(action, deviation):
                max_severity = max(max_severity, deviation.severity)
        
        # Higher severity = higher effectiveness score
        return max_severity
    
    def _action_addresses_deviation(self, action: CorrectionAction, deviation: Deviation) -> bool:
        """فحص ما إذا كان الإجراء يعالج نوع الانحراف"""
        
        action_effectiveness = {
            CorrectionType.BUFFER_OPTIMIZATION: ["latency", "packet_loss", "throughput"],
            CorrectionType.TIMEOUT_ADJUSTMENT: ["latency", "throughput"],
            CorrectionType.RETRANSMISSION_CONTROL: ["packet_loss"],
            CorrectionType.INTERFACE_SWITCH: ["latency", "packet_loss", "throughput"]
        }
        
        return deviation.metric_type in action_effectiveness.get(action.action_type, [])
    
    def _calculate_resource_score(self, action: CorrectionAction, 
                                available_resources: Dict[str, float]) -> float:
        """حساب نقاط الموارد المتاحة"""
        
        # Default resource availability if not specified
        cpu_available = available_resources.get("cpu", 0.8)
        memory_available = available_resources.get("memory", 0.8)
        
        # Check if we have enough resources
        if action.resource_cost > min(cpu_available, memory_available):
            return 0.0  # Not enough resources
        
        # Higher available resources = higher score
        resource_margin = min(cpu_available, memory_available) - action.resource_cost
        return resource_margin
    
    def _calculate_time_score(self, action: CorrectionAction) -> float:
        """حساب نقاط الوقت (تفضيل الإجراءات الأسرع)"""
        
        # Prefer actions that complete within our time constraint
        if action.estimated_time > MAX_CORRECTION_TIME * 1000:  # Convert to ms
            return 0.0  # Too slow
        
        # Normalize time score (faster = higher score)
        max_acceptable_time = MAX_CORRECTION_TIME * 1000
        time_score = 1.0 - (action.estimated_time / max_acceptable_time)
        
        return max(0.0, time_score)
    
    def get_selection_statistics(self) -> Dict:
        """الحصول على إحصائيات الاختيار"""
        
        if not self.selection_history:
            return {"total_selections": 0, "by_action_type": {}, "average_priority": 0.0}
        
        by_action_type = {}
        total_priority = 0.0
        
        for selection in self.selection_history:
            action_type = selection["action"].action_type.value
            by_action_type[action_type] = by_action_type.get(action_type, 0) + 1
            total_priority += selection["priority"]
        
        return {
            "total_selections": len(self.selection_history),
            "by_action_type": by_action_type,
            "average_priority": total_priority / len(self.selection_history),
            "recent_selections": len([s for s in self.selection_history 
                                    if time.time() - s["timestamp"] < 60])
        }
    
    def clear_history(self):
        """مسح تاريخ الاختيارات"""
        self.selection_history.clear()
        print("🗑️ Selection history cleared")
