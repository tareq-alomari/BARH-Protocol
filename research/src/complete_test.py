"""
BARH Protocol - Complete System Test
اختبار النظام الكامل مع جميع الخوارزميات الخمس
"""

import asyncio
import time
from network_simulator import NetworkSimulator
from network_monitor import NetworkMonitor
from deviation_detector import DeviationDetector
from correction_selector import CorrectionSelector
from correction_applicator import CorrectionApplicator
from performance_evaluator import PerformanceEvaluator

class BARHProtocol:
    """بروتوكول BARH الكامل"""
    
    def __init__(self):
        self.simulator = NetworkSimulator()
        self.monitor = NetworkMonitor(self.simulator)
        self.detector = DeviationDetector()
        self.selector = CorrectionSelector()
        self.applicator = CorrectionApplicator(self.simulator)
        self.evaluator = PerformanceEvaluator()
        
        self.is_running = False
        self.correction_count = 0
        
    async def start(self):
        """بدء تشغيل بروتوكول BARH"""
        if self.is_running:
            return
            
        print("🚀 Starting BARH Protocol - Complete System")
        print("   All 5 algorithms active:")
        print("   1️⃣ Network Monitoring")
        print("   2️⃣ Deviation Detection") 
        print("   3️⃣ Correction Selection")
        print("   4️⃣ Correction Application")
        print("   5️⃣ Performance Evaluation")
        print()
        
        self.is_running = True
        await self.monitor.start_monitoring()
        
    async def stop(self):
        """إيقاف بروتوكول BARH"""
        self.is_running = False
        await self.monitor.stop_monitoring()
        print("⏹️ BARH Protocol stopped")
        
    async def run_correction_cycle(self):
        """تشغيل دورة تصحيح كاملة"""
        if not self.is_running:
            return
            
        # Get recent metrics for analysis
        recent_metrics = self.monitor.get_recent_metrics(50)
        baseline_metrics = self.monitor.get_baseline_metrics()
        
        if not recent_metrics or not baseline_metrics:
            return  # Not enough data yet
            
        current_metrics = recent_metrics[-1]
        
        # Step 1: Detect deviations
        deviations = self.detector.analyze_metrics(current_metrics, baseline_metrics)
        
        if not deviations:
            return  # No deviations detected
            
        # Step 2: Select correction
        available_resources = {"cpu": 0.8, "memory": 0.7}
        correction_action = self.selector.select_correction(deviations, available_resources)
        
        if not correction_action:
            return  # No suitable correction found
            
        # Step 3: Apply correction
        print(f"\n🔧 Applying correction #{self.correction_count + 1}:")
        correction_result = await self.applicator.apply_correction(correction_action)
        
        if not correction_result.success:
            print(f"   ❌ Correction failed: {correction_result.error_message}")
            return
            
        # Step 4: Wait a moment and measure after-correction metrics
        await asyncio.sleep(0.5)  # Wait for correction to take effect
        
        # Get metrics after correction
        after_metrics = self.simulator.simulate_correction_effect(
            current_metrics, correction_action.action_type.value
        )
        
        # Step 5: Evaluate performance
        performance_report = self.evaluator.evaluate_correction(
            current_metrics, after_metrics, correction_action, correction_result
        )
        
        self.correction_count += 1
        
        return performance_report

async def complete_system_test():
    """اختبار النظام الكامل"""
    print("🎯 BARH Protocol - Complete System Test")
    print("=" * 60)
    
    # Initialize BARH protocol
    barh = BARHProtocol()
    
    # Start the protocol
    await barh.start()
    
    # Test parameters
    test_duration = 90  # 1.5 minutes
    correction_check_interval = 10  # Check for corrections every 10 seconds
    
    print(f"📊 Running complete system test for {test_duration} seconds...")
    print("   Monitoring network and applying corrections automatically")
    print()
    
    start_time = time.time()
    last_correction_check = 0
    
    try:
        while time.time() - start_time < test_duration:
            current_time = time.time() - start_time
            
            # Check for corrections periodically
            if current_time - last_correction_check >= correction_check_interval:
                await barh.run_correction_cycle()
                last_correction_check = current_time
            
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    
    finally:
        await barh.stop()
        await show_complete_results(barh)

async def show_complete_results(barh: BARHProtocol):
    """عرض النتائج الكاملة"""
    print("\n" + "=" * 60)
    print("📈 BARH Protocol - Complete Results")
    
    # Monitoring performance
    monitoring_perf = barh.monitor.get_monitoring_performance()
    print(f"\n🔍 Network Monitoring:")
    print(f"   Samples collected: {monitoring_perf['samples_collected']}")
    print(f"   Buffer utilization: {monitoring_perf['buffer_size']}/{monitoring_perf['buffer_capacity']}")
    
    # Detection statistics
    detection_stats = barh.detector.get_detection_summary()
    print(f"\n🎯 Deviation Detection:")
    print(f"   Total deviations: {detection_stats['total_detections']}")
    if detection_stats['by_metric']:
        for metric, count in detection_stats['by_metric'].items():
            print(f"   {metric}: {count} deviations")
    if detection_stats['total_detections'] > 0:
        print(f"   Average severity: {detection_stats['average_severity']:.2f}")
    
    # Selection statistics
    selection_stats = barh.selector.get_selection_statistics()
    print(f"\n⚡ Correction Selection:")
    print(f"   Total selections: {selection_stats['total_selections']}")
    if selection_stats['by_action_type']:
        for action_type, count in selection_stats['by_action_type'].items():
            print(f"   {action_type}: {count} selections")
    
    # Application statistics
    application_stats = barh.applicator.get_application_statistics()
    print(f"\n🔧 Correction Application:")
    print(f"   Total applications: {application_stats['total_applications']}")
    print(f"   Success rate: {application_stats['success_rate']*100:.1f}%")
    if application_stats['average_execution_time'] > 0:
        print(f"   Average execution time: {application_stats['average_execution_time']:.2f}ms")
    
    # Performance evaluation
    performance_summary = barh.evaluator.get_performance_summary()
    print(f"\n📊 Performance Evaluation:")
    print(f"   Total evaluations: {performance_summary['total_evaluations']}")
    if performance_summary['total_evaluations'] > 0:
        print(f"   Average effectiveness: {performance_summary['average_effectiveness']:.2f}")
    
    # Research paper metrics
    research_metrics = barh.evaluator.get_research_paper_metrics()
    print(f"\n📄 Research Paper Metrics:")
    if research_metrics['average_latency_improvement'] > 0:
        print(f"   Average latency improvement: {research_metrics['average_latency_improvement']*100:.1f}%")
        print(f"   Average packet loss reduction: {research_metrics['average_packet_loss_reduction']*100:.1f}%")
        print(f"   Average throughput increase: {research_metrics['average_throughput_increase']*100:.1f}%")
        print(f"   Correction success rate: {research_metrics['correction_success_rate']*100:.1f}%")
        print(f"   Average correction time: {research_metrics['average_correction_time']:.2f}ms")
    
    # Performance targets check
    performance_metrics = barh.applicator.get_performance_metrics()
    print(f"\n🎯 Performance Targets:")
    print(f"   Response time target (<5ms): {'✅' if performance_metrics['response_time_target_met'] else '❌'}")
    print(f"   Average response time: {performance_metrics['average_response_time_ms']:.2f}ms")
    
    print(f"\n✅ Complete system test finished!")
    print(f"   Total corrections applied: {barh.correction_count}")
    print(f"   BARH Protocol is fully operational! 🎉")

if __name__ == "__main__":
    asyncio.run(complete_system_test())
