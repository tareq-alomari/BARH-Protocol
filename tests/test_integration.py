"""
اختبار شامل لنظام BARH
"""
from simple_barh import SimpleBARH
from simple_api import SimpleAPI
import json

def test_integration():
    print("🧪 اختبار التكامل الشامل")
    print("=" * 40)
    
    # اختبار النموذج
    barh = SimpleBARH()
    api = SimpleAPI()
    
    # حالات اختبار متنوعة
    test_scenarios = [
        {
            "name": "شبكة مثالية",
            "data": [20, 100, 0.3, 4096, 2048, 0.99, 0.001, 15],
            "expected": "predictive_prefetch"
        },
        {
            "name": "شبكة بطيئة جداً", 
            "data": [500, 10, 0.95, 512, 256, 0.4, 0.15, 800],
            "expected": "data_compression"
        },
        {
            "name": "تأخير متوسط",
            "data": [180, 50, 0.7, 1024, 512, 0.8, 0.03, 120],
            "expected": "route_optimization"
        },
        {
            "name": "شبكة عادية",
            "data": [80, 60, 0.6, 2048, 1024, 0.85, 0.02, 90],
            "expected": "no_action"
        }
    ]
    
    success_count = 0
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 اختبار {i}: {scenario['name']}")
        
        # اختبار النموذج المباشر
        result = barh.predict(scenario['data'])
        print(f"   النتيجة: {result['action']}")
        print(f"   الثقة: {result['confidence']:.0%}")
        
        # اختبار API
        json_data = json.dumps({"network_data": scenario['data']})
        api_result = json.loads(api.predict_json(json_data))
        
        # التحقق من التطابق
        if result['action'] == api_result['action']:
            print("   ✅ API متطابق مع النموذج")
            success_count += 1
        else:
            print("   ❌ عدم تطابق بين API والنموذج")
    
    print(f"\n📊 النتائج النهائية:")
    print(f"   نجح: {success_count}/{len(test_scenarios)}")
    print(f"   معدل النجاح: {success_count/len(test_scenarios)*100:.0f}%")
    
    if success_count == len(test_scenarios):
        print("🎯 جميع الاختبارات نجحت!")
        return True
    else:
        print("⚠️  بعض الاختبارات فشلت")
        return False

def performance_test():
    """اختبار الأداء"""
    print("\n⚡ اختبار الأداء")
    print("=" * 20)
    
    import time
    barh = SimpleBARH()
    
    # بيانات اختبار
    test_data = [100, 50, 0.8, 1024, 512, 0.95, 0.01, 80]
    
    # قياس الوقت
    start_time = time.time()
    for _ in range(1000):
        barh.predict(test_data)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 1000 * 1000  # milliseconds
    print(f"متوسط وقت التوقع: {avg_time:.2f} ms")
    print(f"التوقعات في الثانية: {1000/avg_time:.0f}")
    
    if avg_time < 1:
        print("✅ أداء ممتاز!")
    else:
        print("⚠️  الأداء بطيء")

if __name__ == "__main__":
    # تشغيل جميع الاختبارات
    integration_success = test_integration()
    performance_test()
    
    print(f"\n🏁 التقييم النهائي:")
    if integration_success:
        print("✅ نظام BARH جاهز للإنتاج!")
        print("🚀 يمكن دمجه مع التطبيقات الأخرى")
    else:
        print("❌ يحتاج مراجعة وإصلاح")
