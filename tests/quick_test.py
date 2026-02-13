#!/usr/bin/env python3
from advanced_network_test import AdvancedNetworkTester

print("🔍 اختبار سريع للأداة المتقدمة...")

tester = AdvancedNetworkTester()
network_data, additional_info = tester.get_comprehensive_network_stats()

print(f"🏓 متوسط Ping: {network_data[0]:.1f}ms")
print(f"🌐 عرض النطاق: {network_data[1]:.1f} KB/s")
print(f"🖥️  المعالج: {network_data[2]:.1%}")
print(f"💾 الذاكرة: {network_data[3]:.0f}MB")

print(f"\n📡 واجهات نشطة: {len(additional_info['network_interfaces'])}")
for name, info in additional_info['network_interfaces'].items():
    print(f"   {name}: {info['ip']}")

print(f"\n🎯 تفاصيل Ping:")
for host, result in additional_info['ping_results'].items():
    if result['success']:
        print(f"   {host}: {result['avg_time']:.1f}ms")
    else:
        print(f"   {host}: فشل")

print("\n✅ الاختبار السريع مكتمل!")
