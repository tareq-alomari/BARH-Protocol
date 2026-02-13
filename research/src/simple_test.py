"""
BARH Protocol - Simple Test
اختبار بسيط لبروتوكول BARH
"""

import asyncio
import time
from network_simulator import NetworkSimulator
from network_monitor import NetworkMonitor

async def simple_test():
    """اختبار بسيط للنظام"""
    print("🚀 Starting BARH Protocol Simple Test")
    print("=" * 50)
    
    # Initialize components
    simulator = NetworkSimulator()
    monitor = NetworkMonitor(simulator)
    
    # Start monitoring
    await monitor.start_monitoring()
    
    # Run test for 30 seconds
    test_duration = 30
    print(f"📊 Running test for {test_duration} seconds...")
    print("   Watching for network instabilities and monitoring performance")
    print()
    
    start_time = time.time()
    
    try:
        # Let it run and collect data
        while time.time() - start_time < test_duration:
            await asyncio.sleep(1)
            
            # Show statistics every 10 seconds
            if int(time.time() - start_time) % 10 == 0:
                await show_statistics(monitor)
    
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    
    finally:
        # Stop monitoring
        await monitor.stop_monitoring()
        
        # Show final results
        print("\n" + "=" * 50)
        print("📈 Final Test Results:")
        await show_final_results(monitor)

async def show_statistics(monitor: NetworkMonitor):
    """عرض الإحصائيات الحالية"""
    print("\n📊 Current Statistics:")
    
    for metric_type in ["latency", "packet_loss", "throughput"]:
        stats = monitor.calculate_statistics(metric_type)
        if stats:
            unit = "ms" if metric_type == "latency" else "%" if metric_type == "packet_loss" else "Mbps"
            print(f"   {metric_type.title()}: {stats.mean:.2f}±{stats.std_deviation:.2f} {unit} "
                  f"(min: {stats.min_value:.1f}, max: {stats.max_value:.1f})")
    
    performance = monitor.get_monitoring_performance()
    print(f"   Samples collected: {performance['samples_collected']}")
    print()

async def show_final_results(monitor: NetworkMonitor):
    """عرض النتائج النهائية"""
    
    # Get final statistics
    latency_stats = monitor.calculate_statistics("latency")
    packet_loss_stats = monitor.calculate_statistics("packet_loss")
    throughput_stats = monitor.calculate_statistics("throughput")
    
    if latency_stats and packet_loss_stats and throughput_stats:
        print(f"   Average Latency: {latency_stats.mean:.2f} ms")
        print(f"   Average Packet Loss: {packet_loss_stats.mean:.2f} %")
        print(f"   Average Throughput: {throughput_stats.mean:.2f} Mbps")
        print()
        print(f"   Total samples: {latency_stats.sample_count}")
        print(f"   Latency variation: {latency_stats.std_deviation:.2f} ms")
        print(f"   Packet loss variation: {packet_loss_stats.std_deviation:.2f} %")
        print(f"   Throughput variation: {throughput_stats.std_deviation:.2f} Mbps")
    
    print("\n✅ Test completed successfully!")
    print("   Next step: Implement deviation detection algorithm")

if __name__ == "__main__":
    asyncio.run(simple_test())
