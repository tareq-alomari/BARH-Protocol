#!/usr/bin/env python3
"""
اختبار BARH المتقدم للشبكة - تشمل اختبارات متنوعة
Advanced BARH Network Testing Suite
"""
import subprocess
import time
import json
import psutil
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from simple_barh import SimpleBARH

class AdvancedNetworkTester:
    def __init__(self):
        self.barh = SimpleBARH()
        self.test_hosts = [
            "8.8.8.8",      # Google DNS
            "1.1.1.1",      # Cloudflare DNS  
            "208.67.222.222", # OpenDNS
            "google.com",   # Google
            "github.com"    # GitHub
        ]
        
    def ping_multiple_hosts(self):
        """اختبار ping لعدة مضيفين"""
        results = {}
        
        def ping_host(host):
            try:
                result = subprocess.run(
                    ["ping", "-c", "3", host],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    times = []
                    for line in lines:
                        if "time=" in line:
                            time_part = line.split("time=")[1].split()[0]
                            times.append(float(time_part))
                    
                    if times:
                        return {
                            'host': host,
                            'avg_time': sum(times) / len(times),
                            'min_time': min(times),
                            'max_time': max(times),
                            'success': True
                        }
                
                return {'host': host, 'success': False, 'avg_time': 999.0}
                
            except Exception:
                return {'host': host, 'success': False, 'avg_time': 999.0}
        
        # اختبار متوازي للمضيفين
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(ping_host, host) for host in self.test_hosts]
            for future in futures:
                result = future.result()
                results[result['host']] = result
        
        return results
    
    def test_dns_resolution(self):
        """اختبار حل أسماء النطاقات"""
        dns_results = {}
        test_domains = ["google.com", "github.com", "stackoverflow.com"]
        
        for domain in test_domains:
            try:
                start_time = time.time()
                socket.gethostbyname(domain)
                end_time = time.time()
                
                dns_results[domain] = {
                    'success': True,
                    'resolution_time': (end_time - start_time) * 1000
                }
            except Exception:
                dns_results[domain] = {
                    'success': False,
                    'resolution_time': 999.0
                }
        
        return dns_results
    
    def test_bandwidth_simple(self):
        """اختبار عرض النطاق البسيط"""
        try:
            # محاولة تحميل بيانات صغيرة
            start_time = time.time()
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("httpbin.org", 80))
            
            request = b"GET /bytes/1024 HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
            sock.send(request)
            
            data = b""
            while len(data) < 1024:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                data += chunk
            
            sock.close()
            end_time = time.time()
            
            if len(data) > 0:
                duration = end_time - start_time
                speed = len(data) / duration / 1024  # KB/s
                return {'success': True, 'speed_kbps': speed}
            
        except Exception:
            pass
        
        return {'success': False, 'speed_kbps': 0}
    
    def get_comprehensive_network_stats(self):
        """إحصائيات شبكة شاملة"""
        # الإحصائيات الأساسية
        net_io = psutil.net_io_counters()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # اختبارات متقدمة
        ping_results = self.ping_multiple_hosts()
        dns_results = self.test_dns_resolution()
        bandwidth_result = self.test_bandwidth_simple()
        
        # حساب متوسط التأخير
        successful_pings = [r['avg_time'] for r in ping_results.values() if r['success']]
        avg_latency = sum(successful_pings) / len(successful_pings) if successful_pings else 999.0
        
        # حساب متوسط حل DNS
        successful_dns = [r['resolution_time'] for r in dns_results.values() if r['success']]
        avg_dns_time = sum(successful_dns) / len(successful_dns) if successful_dns else 999.0
        
        # معدل الخطأ
        error_rate = (net_io.errin + net_io.errout) / max(net_io.packets_sent + net_io.packets_recv, 1)
        
        # إرجاع البيانات بتنسيق BARH
        network_data = [
            avg_latency,                           # latency
            bandwidth_result['speed_kbps'],        # bandwidth
            cpu_percent / 100,                     # cpu usage
            memory.used / 1024 / 1024,             # memory MB
            net_io.packets_sent,                   # packets
            1 - error_rate,                        # quality
            error_rate,                            # error_rate
            avg_latency + avg_dns_time             # response_time
        ]
        
        # معلومات إضافية للتقرير
        additional_info = {
            'ping_results': ping_results,
            'dns_results': dns_results,
            'bandwidth_test': bandwidth_result,
            'network_interfaces': self.get_active_interfaces()
        }
        
        return network_data, additional_info
    
    def get_active_interfaces(self):
        """الحصول على الواجهات النشطة"""
        interfaces = {}
        try:
            net_if_stats = psutil.net_if_stats()
            net_if_addrs = psutil.net_if_addrs()
            
            for interface, stats in net_if_stats.items():
                if stats.isup and interface != 'lo':  # تجاهل loopback
                    if interface in net_if_addrs:
                        addresses = [addr.address for addr in net_if_addrs[interface] 
                                   if addr.family == socket.AF_INET]
                        if addresses:
                            interfaces[interface] = {
                                'ip': addresses[0],
                                'speed': stats.speed if stats.speed > 0 else 'Unknown',
                                'mtu': stats.mtu
                            }
        except Exception:
            pass
        
        return interfaces
    
    def run_comprehensive_test(self, duration=60, interval=5):
        """تشغيل اختبار شامل"""
        print("🌐 اختبار BARH الشامل للشبكة")
        print("=" * 70)
        
        # معلومات أولية
        interfaces = self.get_active_interfaces()
        print(f"📡 الواجهات النشطة:")
        for name, info in interfaces.items():
            print(f"   {name}: {info['ip']} (MTU: {info['mtu']})")
        
        print(f"\n⏱️  مدة الاختبار: {duration} ثانية")
        print(f"🔄 فترة القياس: {interval} ثانية")
        print("=" * 70)
        
        start_time = time.time()
        cycle = 1
        results = []
        
        while time.time() - start_time < duration:
            print(f"\n📊 دورة {cycle} - {time.strftime('%H:%M:%S')}")
            print("-" * 50)
            
            # جمع الإحصائيات الشاملة
            network_data, additional_info = self.get_comprehensive_network_stats()
            
            # عرض النتائج التفصيلية
            print(f"🏓 متوسط Ping: {network_data[0]:.1f}ms")
            print(f"🌐 عرض النطاق: {network_data[1]:.1f} KB/s")
            print(f"🖥️  المعالج: {network_data[2]:.1%}")
            print(f"💾 الذاكرة: {network_data[3]:.0f}MB")
            print(f"📦 الحزم المرسلة: {network_data[4]}")
            print(f"✅ جودة الاتصال: {network_data[5]:.3f}")
            print(f"❌ معدل الخطأ: {network_data[6]:.4f}")
            
            # عرض تفاصيل Ping
            print(f"\n🎯 تفاصيل Ping:")
            for host, result in additional_info['ping_results'].items():
                if result['success']:
                    print(f"   {host}: {result['avg_time']:.1f}ms")
                else:
                    print(f"   {host}: فشل")
            
            # عرض تفاصيل DNS
            print(f"\n🔍 تفاصيل DNS:")
            for domain, result in additional_info['dns_results'].items():
                if result['success']:
                    print(f"   {domain}: {result['resolution_time']:.1f}ms")
                else:
                    print(f"   {domain}: فشل")
            
            # قرار BARH
            decision = self.barh.predict(network_data)
            print(f"\n🎯 قرار BARH: {decision['action']}")
            print(f"🎲 مستوى الثقة: {decision['confidence']:.0%}")
            
            # حفظ النتائج
            result = {
                'cycle': cycle,
                'timestamp': time.time(),
                'network_data': network_data,
                'additional_info': additional_info,
                'decision': decision
            }
            results.append(result)
            
            # تطبيق الإجراء
            self.apply_advanced_action(decision['action'], additional_info)
            
            cycle += 1
            time.sleep(interval)
        
        # تلخيص شامل
        self.generate_comprehensive_report(results)
        
        return results
    
    def apply_advanced_action(self, action, network_info):
        """تطبيق إجراء متقدم بناءً على معلومات الشبكة"""
        actions = {
            "no_action": "✅ الشبكة تعمل بكفاءة",
            "route_optimization": "🔄 تحسين مسارات التوجيه",
            "data_compression": "📦 تفعيل ضغط البيانات", 
            "predictive_prefetch": "⚡ تفعيل الجلب التنبؤي"
        }
        
        print(f"🔧 الإجراء: {actions.get(action, action)}")
        
        # اقتراحات إضافية بناءً على حالة الشبكة
        if action == "route_optimization":
            # البحث عن أفضل مضيف
            ping_results = network_info['ping_results']
            best_host = min(ping_results.items(), 
                          key=lambda x: x[1]['avg_time'] if x[1]['success'] else 999)
            print(f"   💡 اقتراح: استخدام {best_host[0]} كمضيف أساسي")
        
        elif action == "data_compression":
            bandwidth = network_info['bandwidth_test']
            if bandwidth['success'] and bandwidth['speed_kbps'] < 100:
                print(f"   💡 اقتراح: تفعيل ضغط قوي بسبب بطء الاتصال")
    
    def generate_comprehensive_report(self, results):
        """إنشاء تقرير شامل"""
        print("\n" + "=" * 70)
        print("📈 التقرير الشامل لاختبار BARH")
        print("=" * 70)
        
        if not results:
            print("❌ لا توجد نتائج")
            return
        
        # إحصائيات الأداء
        latencies = [r['network_data'][0] for r in results]
        bandwidths = [r['network_data'][1] for r in results]
        cpu_usage = [r['network_data'][2] for r in results]
        
        print(f"🏓 إحصائيات التأخير:")
        print(f"   متوسط: {sum(latencies)/len(latencies):.1f}ms")
        print(f"   أدنى: {min(latencies):.1f}ms")
        print(f"   أعلى: {max(latencies):.1f}ms")
        
        print(f"\n🌐 إحصائيات عرض النطاق:")
        print(f"   متوسط: {sum(bandwidths)/len(bandwidths):.1f} KB/s")
        print(f"   أدنى: {min(bandwidths):.1f} KB/s")
        print(f"   أعلى: {max(bandwidths):.1f} KB/s")
        
        print(f"\n🖥️  متوسط استخدام المعالج: {sum(cpu_usage)/len(cpu_usage):.1%}")
        
        # توزيع القرارات
        actions = [r['decision']['action'] for r in results]
        action_counts = {}
        for action in actions:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        print(f"\n🎯 توزيع قرارات BARH:")
        for action, count in action_counts.items():
            percentage = count / len(actions) * 100
            print(f"   {action}: {count} مرة ({percentage:.1f}%)")
        
        # حفظ التقرير
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"barh_comprehensive_test_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 تم حفظ التقرير الشامل في: {filename}")
        
        # تقييم الأداء العام
        avg_latency = sum(latencies) / len(latencies)
        avg_confidence = sum(r['decision']['confidence'] for r in results) / len(results)
        
        print(f"\n🏆 تقييم الأداء العام:")
        if avg_latency < 100:
            print("   🟢 ممتاز: زمن استجابة سريع")
        elif avg_latency < 300:
            print("   🟡 جيد: زمن استجابة مقبول")
        else:
            print("   🔴 يحتاج تحسين: زمن استجابة بطيء")
        
        print(f"   🎲 متوسط ثقة BARH: {avg_confidence:.0%}")

def main():
    """الدالة الرئيسية للاختبار الشامل"""
    print("🚀 اختبار BARH الشامل للشبكة")
    print("=" * 70)
    
    tester = AdvancedNetworkTester()
    
    try:
        # اختبار أولي سريع
        print("🔍 اختبار الاتصال الأولي...")
        network_data, additional_info = tester.get_comprehensive_network_stats()
        
        print(f"🏓 متوسط Ping: {network_data[0]:.1f}ms")
        print(f"🌐 عرض النطاق: {network_data[1]:.1f} KB/s")
        
        if network_data[0] > 1000:
            print("⚠️  تحذير: الاتصال بطيء جداً")
            return
        
        # تشغيل الاختبار الشامل
        print("\n" + "="*70)
        results = tester.run_comprehensive_test(duration=60, interval=5)
        
        print("\n✅ تم الانتهاء من الاختبار الشامل بنجاح!")
        
    except KeyboardInterrupt:
        print("\n⏹️  تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ أثناء الاختبار: {e}")

if __name__ == "__main__":
    main()
