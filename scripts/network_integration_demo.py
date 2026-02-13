"""
مثال دمج BARH مع تطبيق شبكة حقيقي
"""
import time
import random
from simple_barh import SimpleBARH

class NetworkMonitor:
    """محاكي مراقب الشبكة"""
    
    def __init__(self):
        self.barh = SimpleBARH()
        self.running = False
    
    def get_network_stats(self):
        """محاكاة قراءة إحصائيات الشبكة الحقيقية"""
        # في التطبيق الحقيقي، هذه ستأتي من النظام
        return [
            random.uniform(20, 300),    # latency
            random.uniform(10, 100),    # bandwidth  
            random.uniform(0.3, 0.9),   # cpu
            random.randint(512, 4096),  # memory
            random.randint(100, 2000),  # packets
            random.uniform(0.7, 0.99),  # quality
            random.uniform(0.001, 0.1), # error_rate
            random.uniform(10, 200)     # response_time
        ]
    
    def apply_action(self, action):
        """تطبيق الإجراء المقترح"""
        actions_map = {
            "no_action": "✅ الشبكة تعمل بشكل طبيعي",
            "route_optimization": "🔄 تحسين مسار البيانات...",
            "data_compression": "📦 تفعيل ضغط البيانات...", 
            "predictive_prefetch": "⚡ تفعيل الجلب التنبؤي..."
        }
        
        print(f"🎯 {actions_map.get(action, 'إجراء غير معروف')}")
        
        # محاكاة تطبيق الإجراء
        time.sleep(0.1)
        return True
    
    def monitor_loop(self, duration=10):
        """حلقة المراقبة الرئيسية"""
        print(f"🔍 بدء مراقبة الشبكة لمدة {duration} ثانية...")
        print("=" * 50)
        
        start_time = time.time()
        cycle = 1
        
        while time.time() - start_time < duration:
            print(f"\n📊 دورة {cycle}:")
            
            # قراءة حالة الشبكة
            network_data = self.get_network_stats()
            print(f"   التأخير: {network_data[0]:.1f}ms")
            print(f"   معدل الخطأ: {network_data[6]:.3f}")
            
            # اتخاذ القرار
            decision = self.barh.predict(network_data)
            print(f"   القرار: {decision['action']}")
            print(f"   الثقة: {decision['confidence']:.0%}")
            
            # تطبيق الإجراء
            self.apply_action(decision['action'])
            
            cycle += 1
            time.sleep(2)  # انتظار ثانيتين بين الدورات
        
        print(f"\n🏁 انتهت المراقبة بعد {cycle-1} دورات")

def demo_real_integration():
    """عرض توضيحي للدمج الحقيقي"""
    print("🌐 عرض توضيحي: دمج BARH مع مراقب الشبكة")
    print("=" * 60)
    
    monitor = NetworkMonitor()
    
    # تشغيل المراقبة لمدة 10 ثوان
    monitor.monitor_loop(duration=10)
    
    print("\n✅ تم الانتهاء من العرض التوضيحي")
    print("🔧 في التطبيق الحقيقي:")
    print("   - استبدل get_network_stats() بقراءة حقيقية")
    print("   - استبدل apply_action() بتنفيذ حقيقي")
    print("   - أضف logging ومعالجة الأخطاء")

if __name__ == "__main__":
    demo_real_integration()
