"""
BARH Protocol - Enhanced Correction Applicator
مطبق التصحيحات المحسن مع تأثيرات أقوى
"""

import time
import asyncio
from typing import Optional, Dict
from data_structures import CorrectionAction, CorrectionResult, CorrectionType, NetworkMetrics
from enhanced_network_simulator import EnhancedNetworkSimulator
from config import *

class EnhancedCorrectionApplicator:
    """مطبق التصحيحات المحسن مع تأثيرات أقوى وأكثر واقعية"""
    
    def __init__(self, simulator: EnhancedNetworkSimulator):
        self.simulator = simulator
        self.application_history = []
        self.active_corrections = {}
        self.correction_cooldowns = {}
        self.correction_stack = []  # Track multiple corrections
        
    async def apply_correction(self, action: CorrectionAction) -> CorrectionResult:
        """تطبيق الإجراء التصحيحي مع تحسينات"""
        
        # Check cooldown with reduced time for testing
        if self._is_in_cooldown(action.action_type):
            return CorrectionResult(
                success=False,
                execution_time=0.0,
                error_message=f"Action {action.action_type.value} is in cooldown",
                timestamp=time.time()
            )
        
        start_time = time.perf_counter()
        
        try:
            # Apply the correction
            success = await self._execute_enhanced_correction(action)
            
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000
            
            result = CorrectionResult(
                success=success,
                execution_time=execution_time,
                error_message="" if success else f"Failed to apply {action.action_type.value}",
                timestamp=time.time()
            )
            
            # Record in history
            self.application_history.append({
                "action": action,
                "result": result,
                "timestamp": time.time()
            })
            
            if success:
                # Reduced cooldown for more frequent corrections
                self.correction_cooldowns[action.action_type] = time.time() + (CORRECTION_COOLDOWN * 0.5)
                
                # Apply correction effect to simulator
                self.simulator.apply_correction_effect(action.action_type.value, action.parameters)
                
                # Add to correction stack
                self.correction_stack.append({
                    "action": action,
                    "applied_at": time.time()
                })
                
                print(f"✅ Applied {action.action_type.value} in {execution_time:.2f}ms")
            else:
                print(f"❌ Failed to apply {action.action_type.value}")
            
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000
            
            result = CorrectionResult(
                success=False,
                execution_time=execution_time,
                error_message=f"Exception during correction: {str(e)}",
                timestamp=time.time()
            )
            
            print(f"💥 Exception applying {action.action_type.value}: {str(e)}")
            return result
    
    async def _execute_enhanced_correction(self, action: CorrectionAction) -> bool:
        """تنفيذ التصحيح المحسن مع تأثيرات أقوى"""
        
        # Simulate more realistic execution time
        execution_delay = min(action.estimated_time / 1000.0, 0.003)  # Max 3ms
        await asyncio.sleep(execution_delay)
        
        if action.action_type == CorrectionType.BUFFER_OPTIMIZATION:
            return await self._apply_enhanced_buffer_optimization(action.parameters)
            
        elif action.action_type == CorrectionType.TIMEOUT_ADJUSTMENT:
            return await self._apply_enhanced_timeout_adjustment(action.parameters)
            
        elif action.action_type == CorrectionType.RETRANSMISSION_CONTROL:
            return await self._apply_enhanced_retransmission_control(action.parameters)
            
        elif action.action_type == CorrectionType.INTERFACE_SWITCH:
            return await self._apply_enhanced_interface_switch(action.parameters)
            
        else:
            return False
    
    async def _apply_enhanced_buffer_optimization(self, parameters: Dict) -> bool:
        """تطبيق تحسين المخزن المؤقت المحسن"""
        try:
            buffer_size = parameters.get("buffer_size", 65536)
            optimization_level = parameters.get("optimization_level", "moderate")
            
            # Enhanced buffer optimization with better effects
            if optimization_level == "aggressive":
                print(f"   🔧 Aggressive buffer optimization: {buffer_size} bytes")
                # Aggressive optimization has stronger effects
            elif optimization_level == "throughput":
                print(f"   🔧 Throughput-focused buffer optimization: {buffer_size} bytes")
            else:
                print(f"   🔧 Standard buffer optimization: {buffer_size} bytes")
            
            # Store active correction with enhanced tracking
            self.active_corrections["buffer_optimization"] = {
                "buffer_size": buffer_size,
                "optimization_level": optimization_level,
                "applied_at": time.time(),
                "effectiveness_multiplier": 1.5 if optimization_level == "aggressive" else 1.0
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Enhanced buffer optimization failed: {e}")
            return False
    
    async def _apply_enhanced_timeout_adjustment(self, parameters: Dict) -> bool:
        """تطبيق تعديل المهلة الزمنية المحسن"""
        try:
            timeout_ms = parameters.get("timeout_ms", 5000)
            adjustment_factor = parameters.get("adjustment_factor", 1.0)
            
            new_timeout = timeout_ms * adjustment_factor
            
            # Enhanced timeout adjustment with adaptive logic
            if adjustment_factor < 1.0:
                print(f"   ⚡ Aggressive timeout reduction: {timeout_ms}ms → {new_timeout:.0f}ms")
            else:
                print(f"   ⏱️ Conservative timeout increase: {timeout_ms}ms → {new_timeout:.0f}ms")
            
            self.active_corrections["timeout_adjustment"] = {
                "original_timeout": timeout_ms,
                "new_timeout": new_timeout,
                "adjustment_factor": adjustment_factor,
                "applied_at": time.time(),
                "effectiveness_multiplier": 1.3 if adjustment_factor < 1.0 else 1.0
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Enhanced timeout adjustment failed: {e}")
            return False
    
    async def _apply_enhanced_retransmission_control(self, parameters: Dict) -> bool:
        """تطبيق التحكم في إعادة الإرسال المحسن"""
        try:
            max_retries = parameters.get("max_retries", 3)
            backoff_factor = parameters.get("backoff_factor", 1.5)
            
            # Enhanced retransmission with adaptive parameters
            if max_retries >= 5:
                print(f"   🔄 Aggressive retransmission: {max_retries} retries, backoff={backoff_factor}")
            else:
                print(f"   🔄 Standard retransmission: {max_retries} retries, backoff={backoff_factor}")
            
            self.active_corrections["retransmission_control"] = {
                "max_retries": max_retries,
                "backoff_factor": backoff_factor,
                "applied_at": time.time(),
                "effectiveness_multiplier": 1.4 if max_retries >= 5 else 1.0
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Enhanced retransmission control failed: {e}")
            return False
    
    async def _apply_enhanced_interface_switch(self, parameters: Dict) -> bool:
        """تطبيق تبديل الواجهة المحسن"""
        try:
            target_interface = parameters.get("target_interface", "alternative")
            switch_threshold = parameters.get("switch_threshold", 0.5)
            
            # Enhanced interface switching with better targeting
            if target_interface == "high_bandwidth":
                print(f"   🚀 Switching to high-bandwidth interface (threshold: {switch_threshold})")
            elif target_interface == "low_latency":
                print(f"   ⚡ Switching to low-latency interface (threshold: {switch_threshold})")
            else:
                print(f"   🔀 Switching to alternative interface (threshold: {switch_threshold})")
            
            self.active_corrections["interface_switch"] = {
                "target_interface": target_interface,
                "switch_threshold": switch_threshold,
                "applied_at": time.time(),
                "effectiveness_multiplier": 1.6 if target_interface in ["high_bandwidth", "low_latency"] else 1.0
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Enhanced interface switch failed: {e}")
            return False
    
    def _cleanup_expired_corrections(self):
        """تنظيف التصحيحات المنتهية الصلاحية"""
        current_time = time.time()
        expired_corrections = []
        
        # Remove corrections older than 20 seconds
        for correction_type, correction_data in self.active_corrections.items():
            if current_time - correction_data["applied_at"] > 20:
                expired_corrections.append(correction_type)
        
        for correction_type in expired_corrections:
            del self.active_corrections[correction_type]
            self.simulator.remove_correction_effect(correction_type)
        
        # Clean correction stack
        self.correction_stack = [
            correction for correction in self.correction_stack
            if current_time - correction["applied_at"] < 20
        ]
    
    def get_enhanced_statistics(self) -> Dict:
        """الحصول على إحصائيات محسنة"""
        self._cleanup_expired_corrections()
        
        # Calculate base statistics manually since we don't inherit the method
        if not self.application_history:
            base_stats = {
                "total_applications": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0,
                "by_action_type": {}
            }
        else:
            total_applications = len(self.application_history)
            successful_applications = sum(1 for entry in self.application_history 
                                        if entry["result"].success)
            
            success_rate = successful_applications / total_applications
            
            successful_times = [entry["result"].execution_time 
                              for entry in self.application_history 
                              if entry["result"].success]
            
            average_execution_time = (sum(successful_times) / len(successful_times) 
                                    if successful_times else 0.0)
            
            by_action_type = {}
            for entry in self.application_history:
                action_type = entry["action"].action_type.value
                if action_type not in by_action_type:
                    by_action_type[action_type] = {"total": 0, "successful": 0}
                
                by_action_type[action_type]["total"] += 1
                if entry["result"].success:
                    by_action_type[action_type]["successful"] += 1
            
            base_stats = {
                "total_applications": total_applications,
                "successful_applications": successful_applications,
                "success_rate": success_rate,
                "average_execution_time": average_execution_time,
                "by_action_type": by_action_type,
                "recent_applications": len([entry for entry in self.application_history 
                                          if time.time() - entry["timestamp"] < 60])
            }
        
        # Add enhanced metrics
        correction_effectiveness = {}
        for entry in self.application_history:
            action_type = entry["action"].action_type.value
            if action_type not in correction_effectiveness:
                correction_effectiveness[action_type] = []
            
            # Calculate effectiveness based on execution time and success
            if entry["result"].success:
                effectiveness = min(1.0, 5.0 / entry["result"].execution_time)  # Faster = more effective
                correction_effectiveness[action_type].append(effectiveness)
        
        # Calculate average effectiveness per action type
        avg_effectiveness = {}
        for action_type, effectiveness_list in correction_effectiveness.items():
            if effectiveness_list:
                avg_effectiveness[action_type] = sum(effectiveness_list) / len(effectiveness_list)
        
        enhanced_stats = base_stats.copy()
        enhanced_stats.update({
            "active_corrections_count": len(self.active_corrections),
            "correction_stack_depth": len(self.correction_stack),
            "average_effectiveness_by_type": avg_effectiveness,
            "expired_corrections_cleaned": len([c for c in self.application_history 
                                              if time.time() - c["timestamp"] > 20])
        })
        
        return enhanced_stats
    
    def _is_in_cooldown(self, action_type: CorrectionType) -> bool:
        """فحص فترة التهدئة مع تقليل الوقت"""
        if action_type not in self.correction_cooldowns:
            return False
        
        cooldown_end = self.correction_cooldowns[action_type]
        return time.time() < cooldown_end
