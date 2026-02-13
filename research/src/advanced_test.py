"""
BARH Protocol - Advanced Test
اختبار متقدم لبروتوكول BARH مع اكتشاف الانحراف واختيار التصحيح
"""

import asyncio
import time
from network_simulator import NetworkSimulator
from network_monitor import NetworkMonitor
from deviation_detector import DeviationDetector
from correction_selector import CorrectionSelector

async def advanced_test():
    """اختبار متقدم للنظام مع الخوارزميات الثلاث الأولى"""
    print("🚀 Starting BARH Protocol Advanced Test")
    print("   Testing: Monitoring + Deviation Detection + Correction Selection")
    print("=" * 70)
    
    # Initialize components
    simulator = NetworkSimulator()
    monitor = NetworkMonitor(simulator)
    detector = DeviationDetector()
    selector = CorrectionSelector()
    
    # Start monitoring
    await monitor.start_monitoring()
    
    # Test parameters
    test_duration = 60  # 1 minute test
    analysis_interval = 5  # Analyze every 5 seconds
    
    print(f"📊 Running advanced test for {test_duration} seconds...")
    print("   🔍 Monitoring network metrics")
    print("   🎯 Detecting deviations")
    print("   ⚡ Selecting corrections")
    print()
    
    start_time = time.time()
    last_analysis = 0
    
    try:
        while time.time() - start_time < test_duration:
            current_time = time.time() - start_time
            
            # Perform analysis every interval
            if current_time - last_analysis >= analysis_interval:
                await perform_analysis(monitor, detector, selector)
                last_analysis = current_time
            
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    
    finally:
        await monitor.stop_monitoring()
        await show_final_analysis(monitor, detector, selector)

async def perform_analysis(monitor: NetworkMonitor, detector: DeviationDetector, 
                          selector: CorrectionSelector):
    """تنفيذ تحليل شامل للنظام"""
    
    # Get recent metrics for analysis
    recent_metrics = monitor.get_recent_metrics(50)  # Last 50 samples
    baseline_metrics = monitor.get_baseline_metrics()
    
    if not recent_metrics or not baseline_metrics:
        print("⏳ Collecting baseline data...")
        return
    
    # Get current metrics
    current_metrics = recent_metrics[-1]
    
    # Detect deviations
    deviations = detector.analyze_metrics(current_metrics, baseline_metrics)
    
    # Show current status
    network_status = monitor.simulator.get_network_status()
    status_icon = "🟢" if network_status["stable"] else "🔴"
    
    print(f"\n{status_icon} Current Status:")
    print(f"   Latency: {current_metrics.latency:.1f}ms | "
          f"Loss: {current_metrics.packet_loss:.1f}% | "
          f"Throughput: {current_metrics.throughput:.1f}Mbps")
    
    if deviations:
        print(f"   🚨 {len(deviations)} deviation(s) detected:")
        for deviation in deviations:
            severity_icon = "🔥" if deviation.severity > 0.7 else "⚠️" if deviation.severity > 0.3 else "📊"
            print(f"      {severity_icon} {deviation.metric_type}: {deviation.current_value:.1f} "
                  f"(baseline: {deviation.baseline_value:.1f}, severity: {deviation.severity:.2f})")
        
        # Select correction
        available_resources = {"cpu": 0.8, "memory": 0.7}  # Simulated resource availability
        correction = selector.select_correction(deviations, available_resources)
        
        if correction:
            print(f"   ⚡ Selected correction: {correction.action_type.value}")
            print(f"      Priority: {correction.priority:.2f}, "
                  f"Est. time: {correction.estimated_time:.1f}ms, "
                  f"Resource cost: {correction.resource_cost:.2f}")
        else:
            print("   ❌ No suitable correction found")
    else:
        print("   ✅ No deviations detected - network stable")
    
    # Show baselines
    baselines = detector.get_current_baselines()
    if baselines:
        print("   📊 Current baselines:")
        for metric_type, baseline in baselines.items():
            print(f"      {metric_type}: {baseline['mean']:.1f}±{baseline['std_deviation']:.1f}")

async def show_final_analysis(monitor: NetworkMonitor, detector: DeviationDetector, 
                             selector: CorrectionSelector):
    """عرض التحليل النهائي"""
    
    print("\n" + "=" * 70)
    print("📈 Final Analysis Results:")
    
    # Monitoring performance
    monitoring_perf = monitor.get_monitoring_performance()
    print(f"\n🔍 Monitoring Performance:")
    print(f"   Total samples collected: {monitoring_perf['samples_collected']}")
    print(f"   Buffer utilization: {monitoring_perf['buffer_size']}/{monitoring_perf['buffer_capacity']}")
    
    # Detection statistics
    detection_stats = detector.get_detection_summary()
    print(f"\n🎯 Deviation Detection:")
    print(f"   Total deviations detected: {detection_stats['total_detections']}")
    if detection_stats['by_metric']:
        print("   Deviations by metric:")
        for metric, count in detection_stats['by_metric'].items():
            print(f"      {metric}: {count}")
    if detection_stats['total_detections'] > 0:
        print(f"   Average severity: {detection_stats['average_severity']:.2f}")
        print(f"   Recent detections (last minute): {detection_stats['recent_detections']}")
    
    # Selection statistics
    selection_stats = selector.get_selection_statistics()
    print(f"\n⚡ Correction Selection:")
    print(f"   Total corrections selected: {selection_stats['total_selections']}")
    if selection_stats['by_action_type']:
        print("   Selections by action type:")
        for action_type, count in selection_stats['by_action_type'].items():
            print(f"      {action_type}: {count}")
    if selection_stats['total_selections'] > 0:
        print(f"   Average priority: {selection_stats['average_priority']:.2f}")
    
    # Final network statistics
    print(f"\n📊 Final Network Statistics:")
    for metric_type in ["latency", "packet_loss", "throughput"]:
        stats = monitor.calculate_statistics(metric_type)
        if stats:
            unit = "ms" if metric_type == "latency" else "%" if metric_type == "packet_loss" else "Mbps"
            print(f"   {metric_type.title()}: {stats.mean:.2f}±{stats.std_deviation:.2f} {unit}")
    
    print("\n✅ Advanced test completed successfully!")
    print("   Next step: Implement correction application and performance evaluation")

if __name__ == "__main__":
    asyncio.run(advanced_test())
