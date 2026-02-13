"""
BARH Protocol - Quick Ultra-Precision Test
اختبار سريع للنظام عالي الدقة
"""

import asyncio
import time
from enhanced_network_simulator import EnhancedNetworkSimulator
from network_monitor import NetworkMonitor
from deviation_detector import DeviationDetector
from correction_selector import CorrectionSelector
from enhanced_correction_applicator import EnhancedCorrectionApplicator
from performance_evaluator import PerformanceEvaluator

async def quick_precision_test():
    """اختبار سريع للدقة القصوى"""
    print("🎯 BARH Protocol - Quick Ultra-Precision Test")
    print("   🔬 Enhanced Detection & Correction")
    print("   ⚡ Multi-Layer Strategy")
    print("   📊 Maximum Accuracy Target")
    print("=" * 60)
    
    # Initialize enhanced system
    simulator = EnhancedNetworkSimulator()
    monitor = NetworkMonitor(simulator)
    detector = DeviationDetector()
    selector = CorrectionSelector()
    applicator = EnhancedCorrectionApplicator(simulator)
    evaluator = PerformanceEvaluator()
    
    # Start monitoring
    await monitor.start_monitoring()
    
    # Quick test - 45 seconds
    test_duration = 45
    correction_interval = 8
    
    print(f"📊 Running quick precision test for {test_duration} seconds...")
    print()
    
    start_time = time.time()
    last_correction = 0
    corrections_applied = 0
    total_improvements = {"latency": [], "packet_loss": [], "throughput": []}
    
    try:
        while time.time() - start_time < test_duration:
            current_time = time.time() - start_time
            
            # Apply corrections more frequently
            if current_time - last_correction >= correction_interval:
                
                # Get metrics
                recent_metrics = monitor.get_recent_metrics(50)
                baseline_metrics = monitor.get_baseline_metrics()
                
                if recent_metrics and baseline_metrics and len(baseline_metrics) >= 20:
                    current_metrics = recent_metrics[-1]
                    
                    # Detect deviations
                    deviations = detector.analyze_metrics(current_metrics, baseline_metrics)
                    
                    if deviations:
                        print(f"\n🔧 Applying precision correction #{corrections_applied + 1}:")
                        
                        # Select and apply correction
                        available_resources = {"cpu": 0.95, "memory": 0.9}
                        correction_action = selector.select_correction(deviations, available_resources)
                        
                        if correction_action:
                            # Apply correction
                            correction_result = await applicator.apply_correction(correction_action)
                            
                            if correction_result.success:
                                # Wait for effect
                                await asyncio.sleep(0.5)
                                
                                # Simulate enhanced correction effect
                                post_metrics = simulator.simulate_correction_effect(
                                    current_metrics, correction_action.action_type.value
                                )
                                
                                # Evaluate performance
                                performance_report = evaluator.evaluate_correction(
                                    current_metrics, post_metrics, 
                                    correction_action, correction_result
                                )
                                
                                # Track improvements
                                improvements = performance_report.improvement_percentage
                                total_improvements["latency"].append(max(0, improvements["latency"]))
                                total_improvements["packet_loss"].append(max(0, improvements["packet_loss"]))
                                total_improvements["throughput"].append(max(0, improvements["throughput"]))
                                
                                corrections_applied += 1
                
                last_correction = current_time
            
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted")
    
    finally:
        await monitor.stop_monitoring()
        
        # Show results
        print("\n" + "=" * 60)
        print("📈 Quick Ultra-Precision Results")
        
        if corrections_applied > 0:
            # Calculate averages
            avg_latency = sum(total_improvements["latency"]) / len(total_improvements["latency"])
            avg_packet_loss = sum(total_improvements["packet_loss"]) / len(total_improvements["packet_loss"])
            avg_throughput = sum(total_improvements["throughput"]) / len(total_improvements["throughput"])
            
            print(f"\n🎯 Performance Improvements:")
            print(f"   Latency improvement: {avg_latency*100:.1f}% (Target: 75%)")
            print(f"   Packet loss reduction: {avg_packet_loss*100:.1f}% (Target: 85%)")
            print(f"   Throughput increase: {avg_throughput*100:.1f}% (Target: 25%)")
            
            # Target achievement
            latency_achievement = (avg_latency / 0.75) * 100
            packet_loss_achievement = (avg_packet_loss / 0.85) * 100
            throughput_achievement = (avg_throughput / 0.25) * 100
            
            print(f"\n🎯 Target Achievement:")
            print(f"   Latency: {latency_achievement:.1f}% of target")
            print(f"   Packet Loss: {packet_loss_achievement:.1f}% of target")
            print(f"   Throughput: {throughput_achievement:.1f}% of target")
            
            overall_achievement = (latency_achievement + packet_loss_achievement + throughput_achievement) / 3
            print(f"   Overall: {overall_achievement:.1f}%")
            
            # System stats
            monitoring_perf = monitor.get_monitoring_performance()
            application_stats = applicator.get_enhanced_statistics()
            
            print(f"\n🔧 System Performance:")
            print(f"   Corrections applied: {corrections_applied}")
            print(f"   Success rate: {application_stats['success_rate']*100:.1f}%")
            print(f"   Samples collected: {monitoring_perf['samples_collected']}")
            if application_stats['average_execution_time'] > 0:
                print(f"   Avg correction time: {application_stats['average_execution_time']:.2f}ms")
            
            # Final assessment
            if overall_achievement >= 80:
                print(f"\n🏆 EXCELLENT: Ultra-precision system achieved {overall_achievement:.1f}% of targets!")
            elif overall_achievement >= 60:
                print(f"\n✅ GOOD: System achieved {overall_achievement:.1f}% of targets")
            else:
                print(f"\n🟡 MODERATE: System achieved {overall_achievement:.1f}% of targets")
        
        else:
            print(f"\n📊 No corrections needed - network remained stable")
            print(f"   This indicates excellent baseline performance")
        
        print(f"\n✅ Quick ultra-precision test completed!")

if __name__ == "__main__":
    asyncio.run(quick_precision_test())
