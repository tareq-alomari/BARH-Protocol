"""
BARH Protocol - Performance Evaluator (Algorithm 5)
خوارزمية تقييم الأداء - الخوارزمية الخامسة والأخيرة
"""

import time
from typing import Dict, List, Optional
from data_structures import NetworkMetrics, CorrectionAction, CorrectionResult, PerformanceReport
from config import *

class PerformanceEvaluator:
    """مقيم الأداء - ينفذ الخوارزمية الخامسة من BARH"""
    
    def __init__(self):
        self.evaluation_history = []
        self.performance_trends = {
            "latency": [],
            "packet_loss": [],
            "throughput": []
        }
        
    def evaluate_correction(self, before_metrics: NetworkMetrics, 
                          after_metrics: NetworkMetrics,
                          correction_action: CorrectionAction,
                          correction_result: CorrectionResult) -> PerformanceReport:
        """تقييم فعالية التصحيح"""
        
        # Calculate improvements for each metric
        improvements = self._calculate_improvements(before_metrics, after_metrics)
        
        # Calculate overall effectiveness
        overall_effectiveness = self._calculate_overall_effectiveness(improvements)
        
        # Create performance report
        report = PerformanceReport(
            before_metrics=before_metrics,
            after_metrics=after_metrics,
            correction_action=correction_action,
            correction_result=correction_result,
            improvement_percentage=improvements,
            overall_effectiveness=overall_effectiveness
        )
        
        # Store in history
        self.evaluation_history.append({
            "report": report,
            "timestamp": time.time()
        })
        
        # Update performance trends
        self._update_performance_trends(improvements)
        
        # Log evaluation results
        self._log_evaluation_results(report)
        
        return report
    
    def _calculate_improvements(self, before: NetworkMetrics, after: NetworkMetrics) -> Dict[str, float]:
        """حساب التحسينات لكل مقياس"""
        improvements = {}
        
        # Latency improvement (lower is better)
        if before.latency > 0:
            latency_improvement = (before.latency - after.latency) / before.latency
            improvements["latency"] = max(-1.0, min(1.0, latency_improvement))  # Clamp to [-1, 1]
        else:
            improvements["latency"] = 0.0
        
        # Packet loss improvement (lower is better)
        if before.packet_loss > 0:
            packet_loss_improvement = (before.packet_loss - after.packet_loss) / before.packet_loss
            improvements["packet_loss"] = max(-1.0, min(1.0, packet_loss_improvement))
        else:
            improvements["packet_loss"] = 0.0
        
        # Throughput improvement (higher is better)
        if before.throughput > 0:
            throughput_improvement = (after.throughput - before.throughput) / before.throughput
            improvements["throughput"] = max(-1.0, min(1.0, throughput_improvement))
        else:
            improvements["throughput"] = 0.0
        
        return improvements
    
    def _calculate_overall_effectiveness(self, improvements: Dict[str, float]) -> float:
        """حساب الفعالية الإجمالية"""
        
        # Weighted average of improvements
        weights = {
            "latency": 0.4,      # Latency is most important
            "packet_loss": 0.4,  # Packet loss is also critical
            "throughput": 0.2    # Throughput is important but less critical
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric, improvement in improvements.items():
            if metric in weights:
                # Only count positive improvements in overall effectiveness
                positive_improvement = max(0.0, improvement)
                weighted_sum += weights[metric] * positive_improvement
                total_weight += weights[metric]
        
        if total_weight > 0:
            overall_effectiveness = weighted_sum / total_weight
        else:
            overall_effectiveness = 0.0
        
        return overall_effectiveness
    
    def _update_performance_trends(self, improvements: Dict[str, float]):
        """تحديث اتجاهات الأداء"""
        for metric, improvement in improvements.items():
            if metric in self.performance_trends:
                self.performance_trends[metric].append(improvement)
                
                # Keep only last 100 measurements
                if len(self.performance_trends[metric]) > 100:
                    self.performance_trends[metric] = self.performance_trends[metric][-100:]
    
    def _log_evaluation_results(self, report: PerformanceReport):
        """تسجيل نتائج التقييم"""
        action_type = report.correction_action.action_type.value
        effectiveness = report.overall_effectiveness
        
        # Choose appropriate icon based on effectiveness
        if effectiveness >= 0.7:
            icon = "🎯"  # Excellent
        elif effectiveness >= 0.4:
            icon = "✅"  # Good
        elif effectiveness >= 0.1:
            icon = "📊"  # Moderate
        else:
            icon = "⚠️"  # Poor
        
        print(f"   {icon} Correction effectiveness: {effectiveness:.2f}")
        print(f"      Action: {action_type}")
        print(f"      Execution time: {report.correction_result.execution_time:.2f}ms")
        
        # Show individual improvements
        improvements = report.improvement_percentage
        if improvements["latency"] != 0:
            sign = "↓" if improvements["latency"] > 0 else "↑"
            print(f"      Latency: {sign}{abs(improvements['latency']*100):.1f}%")
        
        if improvements["packet_loss"] != 0:
            sign = "↓" if improvements["packet_loss"] > 0 else "↑"
            print(f"      Packet Loss: {sign}{abs(improvements['packet_loss']*100):.1f}%")
        
        if improvements["throughput"] != 0:
            sign = "↑" if improvements["throughput"] > 0 else "↓"
            print(f"      Throughput: {sign}{abs(improvements['throughput']*100):.1f}%")
    
    def get_performance_summary(self) -> Dict:
        """الحصول على ملخص الأداء"""
        if not self.evaluation_history:
            return {
                "total_evaluations": 0,
                "average_effectiveness": 0.0,
                "target_achievements": {},
                "trend_analysis": {}
            }
        
        # Calculate average effectiveness
        total_effectiveness = sum(entry["report"].overall_effectiveness 
                                for entry in self.evaluation_history)
        average_effectiveness = total_effectiveness / len(self.evaluation_history)
        
        # Check target achievements
        target_achievements = self._analyze_target_achievements()
        
        # Analyze trends
        trend_analysis = self._analyze_performance_trends()
        
        return {
            "total_evaluations": len(self.evaluation_history),
            "average_effectiveness": average_effectiveness,
            "target_achievements": target_achievements,
            "trend_analysis": trend_analysis,
            "recent_evaluations": len([entry for entry in self.evaluation_history 
                                     if time.time() - entry["timestamp"] < 60])
        }
    
    def _analyze_target_achievements(self) -> Dict:
        """تحليل تحقيق الأهداف"""
        if not self.evaluation_history:
            return {}
        
        # Count how many corrections achieved the research paper targets
        latency_target_achieved = 0
        packet_loss_target_achieved = 0
        throughput_target_achieved = 0
        
        for entry in self.evaluation_history:
            improvements = entry["report"].improvement_percentage
            
            # Check if improvements meet or exceed targets from research paper
            if improvements["latency"] >= TARGET_LATENCY_IMPROVEMENT:
                latency_target_achieved += 1
            
            if improvements["packet_loss"] >= TARGET_PACKET_LOSS_REDUCTION:
                packet_loss_target_achieved += 1
            
            if improvements["throughput"] >= TARGET_THROUGHPUT_INCREASE:
                throughput_target_achieved += 1
        
        total_evaluations = len(self.evaluation_history)
        
        return {
            "latency_target_achievement_rate": latency_target_achieved / total_evaluations,
            "packet_loss_target_achievement_rate": packet_loss_target_achieved / total_evaluations,
            "throughput_target_achievement_rate": throughput_target_achieved / total_evaluations,
            "overall_target_achievement_rate": (latency_target_achieved + packet_loss_target_achieved + throughput_target_achieved) / (total_evaluations * 3)
        }
    
    def _analyze_performance_trends(self) -> Dict:
        """تحليل اتجاهات الأداء"""
        trends = {}
        
        for metric, improvements in self.performance_trends.items():
            if len(improvements) < 2:
                trends[metric] = "insufficient_data"
                continue
            
            # Calculate trend direction
            recent_improvements = improvements[-10:]  # Last 10 measurements
            early_improvements = improvements[:10] if len(improvements) >= 20 else improvements[:len(improvements)//2]
            
            if recent_improvements and early_improvements:
                recent_avg = sum(recent_improvements) / len(recent_improvements)
                early_avg = sum(early_improvements) / len(early_improvements)
                
                if recent_avg > early_avg + 0.05:  # 5% threshold
                    trends[metric] = "improving"
                elif recent_avg < early_avg - 0.05:
                    trends[metric] = "declining"
                else:
                    trends[metric] = "stable"
            else:
                trends[metric] = "stable"
        
        return trends
    
    def get_research_paper_metrics(self) -> Dict:
        """الحصول على المقاييس للورقة البحثية"""
        if not self.evaluation_history:
            return {
                "average_latency_improvement": 0.0,
                "average_packet_loss_reduction": 0.0,
                "average_throughput_increase": 0.0,
                "correction_success_rate": 0.0,
                "average_correction_time": 0.0
            }
        
        # Calculate averages for research paper
        total_latency_improvement = 0.0
        total_packet_loss_reduction = 0.0
        total_throughput_increase = 0.0
        successful_corrections = 0
        total_correction_time = 0.0
        
        for entry in self.evaluation_history:
            report = entry["report"]
            improvements = report.improvement_percentage
            
            # Only count positive improvements
            total_latency_improvement += max(0.0, improvements["latency"])
            total_packet_loss_reduction += max(0.0, improvements["packet_loss"])
            total_throughput_increase += max(0.0, improvements["throughput"])
            
            if report.correction_result.success:
                successful_corrections += 1
                total_correction_time += report.correction_result.execution_time
        
        total_evaluations = len(self.evaluation_history)
        
        return {
            "average_latency_improvement": total_latency_improvement / total_evaluations,
            "average_packet_loss_reduction": total_packet_loss_reduction / total_evaluations,
            "average_throughput_increase": total_throughput_increase / total_evaluations,
            "correction_success_rate": successful_corrections / total_evaluations,
            "average_correction_time": total_correction_time / successful_corrections if successful_corrections > 0 else 0.0
        }
    
    def clear_history(self):
        """مسح تاريخ التقييمات"""
        self.evaluation_history.clear()
        for metric in self.performance_trends:
            self.performance_trends[metric].clear()
        print("🗑️ Evaluation history cleared")
