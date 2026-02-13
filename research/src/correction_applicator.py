"""
BARH Protocol - Correction Applicator (Algorithm 4)
خوارزمية تطبيق التصحيح - الخوارزمية الرابعة
"""

import time
import asyncio
from typing import Optional, Dict
from data_structures import CorrectionAction, CorrectionResult, CorrectionType, NetworkMetrics
from network_simulator import NetworkSimulator
from config import *

class CorrectionApplicator:
    """مطبق التصحيحات - ينفذ الخوارزمية الرابعة من BARH"""
    
    def __init__(self, simulator: NetworkSimulator):
        self.simulator = simulator
        self.application_history = []
        self.active_corrections = {}
        self.correction_cooldowns = {}
        
    async def apply_correction(self, action: CorrectionAction) -> CorrectionResult:
        """تطبيق الإجراء التصحيحي"""
        
        # Check cooldown
        if self._is_in_cooldown(action.action_type):
            return CorrectionResult(
                success=False,
                execution_time=0.0,
                error_message=f"Action {action.action_type.value} is in cooldown",
                timestamp=time.time()
            )
        
        # Record start time for performance measurement
        start_time = time.perf_counter()
        
        try:
            # Apply the correction based on type
            success = await self._execute_correction(action)
            
            # Calculate execution time
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Create result
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
            
            # Set cooldown if successful
            if success:
                self.correction_cooldowns[action.action_type] = time.time() + CORRECTION_COOLDOWN
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
    
    async def _execute_correction(self, action: CorrectionAction) -> bool:
        """تنفيذ التصحيح الفعلي"""
        
        # Simulate realistic execution time
        await asyncio.sleep(action.estimated_time / 1000.0)  # Convert ms to seconds
        
        if action.action_type == CorrectionType.BUFFER_OPTIMIZATION:
            return await self._apply_buffer_optimization(action.parameters)
            
        elif action.action_type == CorrectionType.TIMEOUT_ADJUSTMENT:
            return await self._apply_timeout_adjustment(action.parameters)
            
        elif action.action_type == CorrectionType.RETRANSMISSION_CONTROL:
            return await self._apply_retransmission_control(action.parameters)
            
        elif action.action_type == CorrectionType.INTERFACE_SWITCH:
            return await self._apply_interface_switch(action.parameters)
            
        else:
            return False
    
    async def _apply_buffer_optimization(self, parameters: Dict) -> bool:
        """تطبيق تحسين المخزن المؤقت"""
        try:
            buffer_size = parameters.get("buffer_size", 65536)
            optimization_level = parameters.get("optimization_level", "moderate")
            
            # Simulate buffer optimization effect
            print(f"   🔧 Optimizing buffer: size={buffer_size}, level={optimization_level}")
            
            # Store active correction
            self.active_corrections["buffer_optimization"] = {
                "buffer_size": buffer_size,
                "optimization_level": optimization_level,
                "applied_at": time.time()
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Buffer optimization failed: {e}")
            return False
    
    async def _apply_timeout_adjustment(self, parameters: Dict) -> bool:
        """تطبيق تعديل المهلة الزمنية"""
        try:
            timeout_ms = parameters.get("timeout_ms", 5000)
            adjustment_factor = parameters.get("adjustment_factor", 1.0)
            
            # Calculate new timeout
            new_timeout = timeout_ms * adjustment_factor
            
            print(f"   ⏱️ Adjusting timeout: {timeout_ms}ms → {new_timeout:.0f}ms")
            
            # Store active correction
            self.active_corrections["timeout_adjustment"] = {
                "original_timeout": timeout_ms,
                "new_timeout": new_timeout,
                "adjustment_factor": adjustment_factor,
                "applied_at": time.time()
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Timeout adjustment failed: {e}")
            return False
    
    async def _apply_retransmission_control(self, parameters: Dict) -> bool:
        """تطبيق التحكم في إعادة الإرسال"""
        try:
            max_retries = parameters.get("max_retries", 3)
            backoff_factor = parameters.get("backoff_factor", 1.5)
            
            print(f"   🔄 Configuring retransmission: max_retries={max_retries}, backoff={backoff_factor}")
            
            # Store active correction
            self.active_corrections["retransmission_control"] = {
                "max_retries": max_retries,
                "backoff_factor": backoff_factor,
                "applied_at": time.time()
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Retransmission control failed: {e}")
            return False
    
    async def _apply_interface_switch(self, parameters: Dict) -> bool:
        """تطبيق تبديل الواجهة"""
        try:
            target_interface = parameters.get("target_interface", "alternative")
            switch_threshold = parameters.get("switch_threshold", 0.5)
            
            print(f"   🔀 Switching interface: target={target_interface}, threshold={switch_threshold}")
            
            # Store active correction
            self.active_corrections["interface_switch"] = {
                "target_interface": target_interface,
                "switch_threshold": switch_threshold,
                "applied_at": time.time()
            }
            
            return True
            
        except Exception as e:
            print(f"   ❌ Interface switch failed: {e}")
            return False
    
    def _is_in_cooldown(self, action_type: CorrectionType) -> bool:
        """فحص ما إذا كان الإجراء في فترة التهدئة"""
        if action_type not in self.correction_cooldowns:
            return False
        
        cooldown_end = self.correction_cooldowns[action_type]
        return time.time() < cooldown_end
    
    def get_active_corrections(self) -> Dict:
        """الحصول على التصحيحات النشطة"""
        # Remove expired corrections (older than 60 seconds)
        current_time = time.time()
        expired_corrections = []
        
        for correction_type, correction_data in self.active_corrections.items():
            if current_time - correction_data["applied_at"] > 60:
                expired_corrections.append(correction_type)
        
        for correction_type in expired_corrections:
            del self.active_corrections[correction_type]
        
        return self.active_corrections.copy()
    
    def get_application_statistics(self) -> Dict:
        """الحصول على إحصائيات التطبيق"""
        if not self.application_history:
            return {
                "total_applications": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0,
                "by_action_type": {}
            }
        
        total_applications = len(self.application_history)
        successful_applications = sum(1 for entry in self.application_history 
                                    if entry["result"].success)
        
        success_rate = successful_applications / total_applications
        
        # Calculate average execution time for successful applications
        successful_times = [entry["result"].execution_time 
                          for entry in self.application_history 
                          if entry["result"].success]
        
        average_execution_time = (sum(successful_times) / len(successful_times) 
                                if successful_times else 0.0)
        
        # Count by action type
        by_action_type = {}
        for entry in self.application_history:
            action_type = entry["action"].action_type.value
            if action_type not in by_action_type:
                by_action_type[action_type] = {"total": 0, "successful": 0}
            
            by_action_type[action_type]["total"] += 1
            if entry["result"].success:
                by_action_type[action_type]["successful"] += 1
        
        return {
            "total_applications": total_applications,
            "successful_applications": successful_applications,
            "success_rate": success_rate,
            "average_execution_time": average_execution_time,
            "by_action_type": by_action_type,
            "recent_applications": len([entry for entry in self.application_history 
                                      if time.time() - entry["timestamp"] < 60])
        }
    
    def get_performance_metrics(self) -> Dict:
        """الحصول على مقاييس الأداء"""
        stats = self.get_application_statistics()
        
        if stats["total_applications"] == 0:
            return {
                "response_time_target_met": True,  # No applications yet
                "success_rate_percentage": 0.0,
                "average_response_time_ms": 0.0,
                "target_response_time_ms": MAX_CORRECTION_TIME * 1000
            }
        
        target_response_time_ms = MAX_CORRECTION_TIME * 1000  # 5ms
        response_time_target_met = stats["average_execution_time"] <= target_response_time_ms
        
        return {
            "response_time_target_met": response_time_target_met,
            "success_rate_percentage": stats["success_rate"] * 100,
            "average_response_time_ms": stats["average_execution_time"],
            "target_response_time_ms": target_response_time_ms
        }
    
    def clear_history(self):
        """مسح تاريخ التطبيقات"""
        self.application_history.clear()
        self.active_corrections.clear()
        self.correction_cooldowns.clear()
        print("🗑️ Application history cleared")
