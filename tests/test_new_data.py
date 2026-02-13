"""
اختبار BARH على بيانات جديدة ومتنوعة
"""
from simple_barh import SimpleBARH
import random

def generate_new_test_data():
    """توليد بيانات اختبار جديدة ومتنوعة"""
    scenarios = [
        # حالات شبكة حقيقية متنوعة
        {
            "name": "شبكة مكتب صباحاً",
            "data": [45, 80, 0.4, 2048, 800, 0.92, 0.005, 60]
        },
        {
            "name": "شبكة مزدحمة مساءً", 
            "data": [180, 25, 0.85, 1024, 1500, 0.65, 0.08, 220]
        },
        {
            "name": "شبكة ألعاب عالية الأداء",
            "data": [15, 200, 0.6, 8192, 3000, 0.98, 0.001, 12]
        },
        {
            "name": "شبكة محمولة ضعيفة",
            "data": [400, 5, 0.9, 256, 100, 0.3, 0.2, 500]
        },
        {
            "name": "شبكة خادم تحت الضغط",
            "data": [120, 100, 0.95, 4096, 5000, 0.8, 0.06, 180]
        },
        {
            "name": "شبكة WiFi منزلية",
            "data": [80, 50, 0.5, 1024, 400, 0.88, 0.02, 95]
        },
        {
            "name": "شبكة 5G مثالية",
            "data": [8, 500, 0.3, 16384, 8000, 0.99, 0.0001, 5]
        },
        {
            "name": "شبكة قديمة بطيئة",
            "data": [600, 2, 0.8, 128, 50, 0.2, 0.3, 800]
        }
    ]
    
    # إضافة بيانات عشوائية
    for i in range(5):
        scenarios.append({
            "name": f"شبكة عشوائية {i+1}",
            "data": [
                random.uniform(10, 500),    # latency
                random.uniform(1, 1000),    # bandwidth
                random.uniform(0.2, 0.99),  # cpu
                random.randint(128, 16384), # memory
                random.randint(50, 10000),  # packets
                random.uniform(0.1, 0.99),  # quality
                random.uniform(0.0001, 0.5), # error_rate
                random.uniform(5, 1000)     # response_time
            ]
        })
    
    return scenarios

def test_new_data():
    """اختبار البيانات الجديدة"""
    print("🧪 اختبار BARH على بيانات جديدة ومتنوعة")
    print("=" * 60)
    
    barh = SimpleBARH()
    test_data = generate_new_test_data()
    
    results = {
        "no_action": 0,
        "route_optimization": 0,
        "data_compression": 0,
        "predictive_prefetch": 0
    }
    
    high_confidence = 0
    
    for i, scenario in enumerate(test_data, 1):
        print(f"\n🔍 اختبار {i}: {scenario['name']}")
        
        # عرض البيانات الأساسية
        data = scenario['data']
        print(f"   📊 التأخير: {data[0]:.1f}ms | النطاق: {data[1]:.1f}Mbps")
        print(f"   💾 المعالج: {data[2]:.1%} | الذاكرة: {data[3]}MB")
        print(f"   📈 الجودة: {data[5]:.1%} | الخطأ: {data[6]:.3f}")
        
        # التوقع
        result = barh.predict(data)
        action = result['action']
        confidence = result['confidence']
        
        print(f"   🎯 القرار: {action}")
        print(f"   📈 الثقة: {confidence:.0%}")
        
        # إحصائيات
        results[action] += 1
        if confidence >= 0.9:
            high_confidence += 1
        
        # تقييم منطقية القرار
        if data[0] > 200 and action == "route_optimization":
            print("   ✅ قرار منطقي - تأخير عالي")
        elif data[6] > 0.05 and action == "data_compression":
            print("   ✅ قرار منطقي - خطأ عالي")
        elif data[5] > 0.95 and data[0] < 50 and action == "predictive_prefetch":
            print("   ✅ قرار منطقي - أداء ممتاز")
        elif action == "no_action":
            print("   ✅ قرار منطقي - حالة عادية")
        else:
            print("   ⚠️  قرار يحتاج مراجعة")
    
    # تقرير الإحصائيات
    print(f"\n📊 إحصائيات النتائج:")
    print("=" * 30)
    total_tests = len(test_data)
    
    for action, count in results.items():
        percentage = (count / total_tests) * 100
        print(f"   {action}: {count} ({percentage:.1f}%)")
    
    print(f"\n📈 الثقة العالية (≥90%): {high_confidence}/{total_tests} ({high_confidence/total_tests*100:.1f}%)")
    
    # تقييم الأداء العام
    print(f"\n🏆 التقييم العام:")
    if high_confidence / total_tests >= 0.7:
        print("   ✅ أداء ممتاز - ثقة عالية في معظم القرارات")
    elif high_confidence / total_tests >= 0.5:
        print("   ⚠️  أداء جيد - ثقة متوسطة")
    else:
        print("   ❌ أداء يحتاج تحسين")
    
    return results

if __name__ == "__main__":
    test_new_data()
