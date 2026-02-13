"""
Simplified Enhanced Testing Suite for BARH Protocol
No external dependencies - pure Python implementation
"""

import time
import json
import math
import random
from typing import Dict, List, Tuple
from enhanced_barh_protocol import EnhancedBARHProtocol, NetworkMetrics
from enhanced_network_simulator import EnhancedNetworkSimulator
from collections import defaultdict

class SimpleStatisticalAnalyzer:
    """Simple statistical analysis without external dependencies"""
    
    @staticmethod
    def mean(data: List[float]) -> float:
        return sum(data) / len(data) if data else 0.0
    
    @staticmethod
    def variance(data: List[float]) -> float:
        if len(data) < 2:
            return 0.0
        mean_val = SimpleStatisticalAnalyzer.mean(data)
        return sum((x - mean_val) ** 2 for x in data) / (len(data) - 1)
    
    @staticmethod
    def std_dev(data: List[float]) -> float:
        return math.sqrt(SimpleStatisticalAnalyzer.variance(data))
    
    @staticmethod
    def percentile(data: List[float], p: float) -> float:
        if not data:
            return 0.0
        sorted_data = sorted(data)
        k = (len(sorted_data) - 1) * p / 100
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_data[int(k)]
        return sorted_data[int(f)] * (c - k) + sorted_data[int(c)] * (k - f)
    
    @staticmethod
    def calculate_effect_size(before: List[float], after: List[float]) -> float:
        """Calculate Cohen's d effect size"""
        if len(before) < 2 or len(after) < 2:
            return 0.0
        
        mean_before = SimpleStatisticalAnalyzer.mean(before)
        mean_after = SimpleStatisticalAnalyzer.mean(after)
        
        # Pooled standard deviation
        var_before = SimpleStatisticalAnalyzer.variance(before)
        var_after = SimpleStatisticalAnalyzer.variance(after)
        pooled_var = ((len(before) - 1) * var_before + (len(after) - 1) * var_after) / (len(before) + len(after) - 2)
        pooled_std = math.sqrt(pooled_var)
        
        if pooled_std == 0:
            return 0.0
        
        return (mean_after - mean_before) / pooled_std

def run_quick_enhanced_test():
    """Quick comprehensive test of enhanced BARH protocol"""
    print("🚀 Enhanced BARH Protocol - Quick Comprehensive Test")
    print("=" * 55)
    
    # Initialize components
    protocol = EnhancedBARHProtocol()
    simulator = EnhancedNetworkSimulator()
    analyzer = SimpleStatisticalAnalyzer()
    
    # Test scenarios
    scenarios = [
        ("stable_baseline", 15.0),
        ("sudden_congestion", 20.0),
        ("intermittent_loss", 18.0),
        ("6g_simulation", 12.0),
        ("extreme_conditions", 25.0)
    ]
    
    all_results = {}
    
    for scenario_name, duration in scenarios:
        print(f"\n🔬 Testing Scenario: {scenario_name} ({duration}s)")
        print("-" * 45)
        
        # Reset and configure scenario
        simulator.reset_events()
        simulator.simulate_scenario(scenario_name, duration)
        
        # Baseline test (without BARH)
        print("📊 Running baseline test...")
        baseline_metrics = []
        start_time = time.time()
        
        while time.time() - start_time < duration / 3:  # Shorter for quick test
            metrics = simulator.get_current_metrics()
            baseline_metrics.append({
                'latency': metrics.latency,
                'packet_loss': metrics.packet_loss,
                'throughput': metrics.throughput,
                'jitter': metrics.jitter
            })
            time.sleep(0.02)  # 20ms sampling for quick test
        
        # Enhanced test (with BARH)
        print("🚀 Running enhanced BARH test...")
        protocol.start()
        enhanced_metrics = []
        corrections_applied = 0
        processing_times = []
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration / 3:  # Shorter for quick test
                metrics = simulator.get_current_metrics()
                
                # Process with BARH
                result = protocol.process_metrics(metrics)
                
                enhanced_metrics.append({
                    'latency': metrics.latency,
                    'packet_loss': metrics.packet_loss,
                    'throughput': metrics.throughput,
                    'jitter': metrics.jitter
                })
                
                if result['correction_applied']:
                    corrections_applied += 1
                
                processing_times.append(result['processing_time'])
                time.sleep(0.02)  # 20ms sampling
                
        finally:
            protocol.stop()
        
        # Calculate results
        baseline_latencies = [m['latency'] for m in baseline_metrics]
        enhanced_latencies = [m['latency'] for m in enhanced_metrics]
        baseline_losses = [m['packet_loss'] for m in baseline_metrics]
        enhanced_losses = [m['packet_loss'] for m in enhanced_metrics]
        baseline_throughputs = [m['throughput'] for m in baseline_metrics]
        enhanced_throughputs = [m['throughput'] for m in enhanced_metrics]
        
        # Calculate improvements
        latency_improvement = ((analyzer.mean(baseline_latencies) - analyzer.mean(enhanced_latencies)) / 
                              analyzer.mean(baseline_latencies)) * 100 if baseline_latencies else 0
        
        loss_improvement = ((analyzer.mean(baseline_losses) - analyzer.mean(enhanced_losses)) / 
                           analyzer.mean(baseline_losses)) * 100 if baseline_losses else 0
        
        throughput_improvement = ((analyzer.mean(enhanced_throughputs) - analyzer.mean(baseline_throughputs)) / 
                                 analyzer.mean(baseline_throughputs)) * 100 if baseline_throughputs else 0
        
        # Effect size
        effect_size = analyzer.calculate_effect_size(baseline_latencies, enhanced_latencies)
        
        # Store results
        results = {
            'scenario': scenario_name,
            'duration': duration / 3,
            'baseline': {
                'latency_mean': analyzer.mean(baseline_latencies),
                'latency_std': analyzer.std_dev(baseline_latencies),
                'latency_p99': analyzer.percentile(baseline_latencies, 99),
                'packet_loss_mean': analyzer.mean(baseline_losses),
                'throughput_mean': analyzer.mean(baseline_throughputs)
            },
            'enhanced': {
                'latency_mean': analyzer.mean(enhanced_latencies),
                'latency_std': analyzer.std_dev(enhanced_latencies),
                'latency_p99': analyzer.percentile(enhanced_latencies, 99),
                'packet_loss_mean': analyzer.mean(enhanced_losses),
                'throughput_mean': analyzer.mean(enhanced_throughputs),
                'corrections_applied': corrections_applied,
                'avg_processing_time': analyzer.mean(processing_times),
                'max_processing_time': max(processing_times) if processing_times else 0
            },
            'improvements': {
                'latency_percent': latency_improvement,
                'packet_loss_percent': loss_improvement,
                'throughput_percent': throughput_improvement,
                'effect_size': effect_size
            }
        }
        
        all_results[scenario_name] = results
        
        # Print scenario results
        print(f"✅ Results for {scenario_name}:")
        print(f"   📈 Latency improvement: {latency_improvement:.1f}%")
        print(f"   📉 Packet loss improvement: {loss_improvement:.1f}%")
        print(f"   🚀 Throughput improvement: {throughput_improvement:.1f}%")
        print(f"   🔧 Corrections applied: {corrections_applied}")
        print(f"   ⚡ Avg processing time: {analyzer.mean(processing_times)*1000:.2f}ms")
        
        time.sleep(1)  # Brief pause between scenarios
    
    # Calculate overall summary
    all_latency_improvements = [r['improvements']['latency_percent'] for r in all_results.values()]
    all_loss_improvements = [r['improvements']['packet_loss_percent'] for r in all_results.values()]
    all_throughput_improvements = [r['improvements']['throughput_percent'] for r in all_results.values()]
    
    summary = {
        'total_scenarios': len(scenarios),
        'average_improvements': {
            'latency': analyzer.mean(all_latency_improvements),
            'packet_loss': analyzer.mean(all_loss_improvements),
            'throughput': analyzer.mean(all_throughput_improvements)
        },
        'best_improvements': {
            'latency': max(all_latency_improvements),
            'packet_loss': max(all_loss_improvements),
            'throughput': max(all_throughput_improvements)
        }
    }
    
    # Final results
    final_results = {
        'test_summary': summary,
        'detailed_results': all_results,
        'timestamp': time.time()
    }
    
    print("\n" + "=" * 55)
    print("🎉 ENHANCED BARH PROTOCOL TEST COMPLETED")
    print("=" * 55)
    print(f"📊 OVERALL AVERAGE IMPROVEMENTS:")
    print(f"   🔥 Latency: {summary['average_improvements']['latency']:.1f}%")
    print(f"   🔥 Packet Loss: {summary['average_improvements']['packet_loss']:.1f}%")
    print(f"   🔥 Throughput: {summary['average_improvements']['throughput']:.1f}%")
    print(f"\n🏆 BEST SCENARIO IMPROVEMENTS:")
    print(f"   🥇 Latency: {summary['best_improvements']['latency']:.1f}%")
    print(f"   🥇 Packet Loss: {summary['best_improvements']['packet_loss']:.1f}%")
    print(f"   🥇 Throughput: {summary['best_improvements']['throughput']:.1f}%")
    
    # Save results
    timestamp = int(time.time())
    filename = f"enhanced_barh_results_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(final_results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving results: {str(e)}")
    
    return final_results

if __name__ == "__main__":
    run_quick_enhanced_test()
