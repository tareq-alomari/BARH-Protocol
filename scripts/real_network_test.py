#!/usr/bin/env python3
"""
اختبار BARH على الشبكة الحقيقية
Real Network Testing for BARH Protocol
"""
import subprocess
import time
import json
import psutil
import socket
from simple_barh import SimpleBARH

class RealNetworkTester:
    def __init__(self):
        self.barh = SimpleBARH()
        
    def get_real_network_stats(self):
        """قراءة إحصائيات الشبكة الحقيقية من النظام"""
        try:
            # معلومات الشبكة
            net_io = psutil.net_io_counters()
            
            # معلومات النظام
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # اختبار ping لقياس التأخير
            latency = self.ping_test("8.8.8.8")
            
            # حساب معدل الخطأ (تقريبي)
            error_rate = (net_io.errin + net_io.errout) / max(net_io.packets_sent + net_io.packets_recv, 1)
            
            return [
                latency,                           # latency (ms)
                net_io.bytes_sent / 1024 / 1024,   # bandwidth out (MB)
                cpu_percent / 100,                 # cpu usage (0-1)
                memory.used / 1024 / 1024,         # memory used (MB)
                net_io.packets_sent,               # packets sent
                1 - error_rate,                    # quality (1 - error_rate)
                error_rate,                        # error_rate
                latency * 2                        # response_time (approx)
            ]
        except Exception as e:
            print(f"خطأ في قراءة إحصائيات الشبكة: {e}")
            return [100, 50, 0.5, 1024, 1000, 0.9, 0.01, 200]
    
    def ping_test(self, host="8.8.8.8", count=1):
        """اختبار ping لقياس التأخير"""
        try:
            result = subprocess.run(
                ["ping", "-c", str(count), host],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                # استخراج وقت الاستجابة من النتيجة
                lines = result.stdout.split('\n')
                for line in lines:
                    if "time=" in line:
                        time_part = line.split("time=")[1].split()[0]
                        return float(time_part)
            
            return 999.0  # timeout
            
        except Exception:
            return 999.0
    
    def test_internet_speed(self):
        """اختبار سرعة الإنترنت البسيط"""
        try:
            start_time = time.time()
            
            # محاولة الاتصال بموقع سريع
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(("8.8.8.8", 53))
            sock.close()
            
            end_time = time.time()
            connection_time = (end_time - start_time) * 1000
            
            return connection_time if result == 0 else 999.0
            
        except Exception:
            return 999.0
    
    def get_network_interfaces(self):
        """الحصول على معلومات واجهات الشبكة"""
        interfaces = {}
        try:
            net_if_stats = psutil.net_if_stats()
            net_if_addrs = psutil.net_if_addrs()
            
            for interface, stats in net_if_stats.items():
                if stats.isup and interface in net_if_addrs:
                    interfaces[interface] = {
                        'is_up': stats.isup,
                        'speed': stats.speed,
                        'mtu': stats.mtu,
                        'addresses': [addr.address for addr in net_if_addrs[interface]]
                    }
        except Exception as e:
            print(f"خطأ في قراءة واجهات الشبكة: {e}")
        
        return interfaces
    
    def run_real_test(self, duration=30, interval=3):
        """تشغيل اختبار حقيقي على الشبكة"""
        print("🌐 بدء اختبار BARH على الشبكة الحقيقية")
        print("=" * 60)
        
        # عرض معلومات الشبكة
        interfaces = self.get_network_interfaces()
        print(f"📡 واجهات الشبكة النشطة: {len(interfaces)}")
        for name, info in interfaces.items():
            print(f"   {name}: {info['addresses'][0] if info['addresses'] else 'N/A'}")
        
        print(f"\n⏱️  مدة الاختبار: {duration} ثانية")
        print(f"🔄 فترة القياس: {interval} ثانية")
        print("=" * 60)
        
        start_time = time.time()
        cycle = 1
        results = []
        
        while time.time() - start_time < duration:
            print(f"\n📊 دورة {cycle} - {time.strftime('%H:%M:%S')}")
            
            # قراءة الإحصائيات الحقيقية
            network_data = self.get_real_network_stats()
            
            # عرض المعلومات
            print(f"   🏓 Ping: {network_data[0]:.1f}ms")
            print(f"   💾 الذاكرة: {network_data[3]:.0f}MB")
            print(f"   🖥️  المعالج: {network_data[2]:.1%}")
            print(f"   📦 الحزم: {network_data[4]}")
            print(f"   ❌ معدل الخطأ: {network_data[6]:.4f}")
            
            # اتخاذ القرار باستخدام BARH
            decision = self.barh.predict(network_data)
            
            print(f"   🎯 قرار BARH: {decision['action']}")
            print(f"   🎲 مستوى الثقة: {decision['confidence']:.0%}")
            
            # حفظ النتائج
            result = {
                'cycle': cycle,
                'timestamp': time.time(),
                'network_data': network_data,
                'decision': decision
            }
            results.append(result)
            
            # تطبيق الإجراء (محاكاة)
            self.simulate_action(decision['action'])
            
            cycle += 1
            time.sleep(interval)
        
        # تلخيص النتائج
        self.summarize_results(results)
        
        return results
    
    def simulate_action(self, action):
        """محاكاة تطبيق الإجراء"""
        actions = {
            "no_action": "✅ لا حاجة لإجراء",
            "route_optimization": "🔄 تحسين المسار",
            "data_compression": "📦 ضغط البيانات", 
            "predictive_prefetch": "⚡ جلب تنبؤي"
        }
        
        print(f"   🔧 الإجراء: {actions.get(action, action)}")
    
    def summarize_results(self, results):
        """تلخيص نتائج الاختبار"""
        print("\n" + "=" * 60)
        print("📈 ملخص نتائج الاختبار")
        print("=" * 60)
        
        if not results:
            print("❌ لا توجد نتائج للعرض")
            return
        
        # إحصائيات الشبكة
        latencies = [r['network_data'][0] for r in results]
        cpu_usage = [r['network_data'][2] for r in results]
        error_rates = [r['network_data'][6] for r in results]
        
        print(f"🏓 متوسط التأخير: {sum(latencies)/len(latencies):.1f}ms")
        print(f"🖥️  متوسط استخدام المعالج: {sum(cpu_usage)/len(cpu_usage):.1%}")
        print(f"❌ متوسط معدل الخطأ: {sum(error_rates)/len(error_rates):.4f}")
        
        # إحصائيات القرارات
        actions = [r['decision']['action'] for r in results]
        action_counts = {}
        for action in actions:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        print(f"\n🎯 توزيع القرارات:")
        for action, count in action_counts.items():
            percentage = count / len(actions) * 100
            print(f"   {action}: {count} مرة ({percentage:.1f}%)")
        
        # متوسط الثقة
        confidences = [r['decision']['confidence'] for r in results]
        avg_confidence = sum(confidences) / len(confidences)
        print(f"\n🎲 متوسط مستوى الثقة: {avg_confidence:.0%}")
        
        # حفظ النتائج في ملف
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"barh_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 تم حفظ النتائج في: {filename}")

def main():
    """الدالة الرئيسية"""
    print("🚀 مرحباً بك في اختبار BARH للشبكة الحقيقية")
    print("=" * 60)
    
    tester = RealNetworkTester()
    
    try:
        # اختبار سريع أولاً
        print("🔍 اختبار الاتصال...")
        ping_result = tester.ping_test()
        print(f"🏓 نتيجة Ping: {ping_result}ms")
        
        if ping_result > 500:
            print("⚠️  تحذير: الاتصال بطيء، قد تكون النتائج غير دقيقة")
        
        # تشغيل الاختبار الكامل
        print("\n" + "="*60)
        results = tester.run_real_test(duration=30, interval=3)
        
        print("\n✅ تم الانتهاء من الاختبار بنجاح!")
        
    except KeyboardInterrupt:
        print("\n⏹️  تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ أثناء الاختبار: {e}")

if __name__ == "__main__":
    main()
