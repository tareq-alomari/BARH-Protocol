"""
محاكي بسيط لنموذج BARH - بدون tensorflow
"""
import pickle
import random
import numpy as np

class SimpleBARH:
    def __init__(self):
        self.actions = {
            0: "no_action",
            1: "route_optimization", 
            2: "data_compression",
            3: "predictive_prefetch"
        }
        self.scaler = None
        self.load_scaler()
    
    def load_scaler(self):
        """تحميل المعالج فقط"""
        try:
            with open("models/scaler.pkl", 'rb') as f:
                self.scaler = pickle.load(f)
            print("✅ تم تحميل معالج البيانات")
            return True
        except:
            print("❌ لم يتم العثور على المعالج")
            return False
    
    def predict(self, network_data):
        """توقع بسيط بناءً على قواعد"""
        if len(network_data) != 8:
            return None
        
        # قواعد بسيطة للتوقع
        latency, bandwidth, cpu, memory, packets, quality, error_rate, response_time = network_data
        
        # قرار بناءً على القيم
        if error_rate > 0.05:  # خطأ عالي
            action = 2  # ضغط البيانات
            confidence = 0.95
        elif latency > 150:  # تأخير عالي
            action = 1  # تحسين المسار
            confidence = 0.90
        elif quality > 0.9 and response_time < 100:  # أداء ممتاز
            action = 3  # جلب تنبؤي
            confidence = 0.85
        else:
            action = 0  # لا يوجد إجراء
            confidence = 0.80
        
        return {
            "action": self.actions[action],
            "confidence": confidence,
            "reasoning": f"القرار بناءً على: latency={latency}, error_rate={error_rate}"
        }

# اختبار سريع
if __name__ == "__main__":
    print("🤖 محاكي BARH البسيط")
    
    barh = SimpleBARH()
    
    # بيانات اختبار
    test_cases = [
        [100, 50, 0.8, 1024, 512, 0.95, 0.01, 80],   # حالة عادية
        [200, 30, 0.9, 2048, 1024, 0.7, 0.08, 150],  # تأخير + خطأ
        [50, 100, 0.6, 512, 256, 0.98, 0.001, 40],   # أداء ممتاز
    ]
    
    for i, data in enumerate(test_cases, 1):
        result = barh.predict(data)
        print(f"\n🔮 اختبار {i}:")
        print(f"   الإجراء: {result['action']}")
        print(f"   الثقة: {result['confidence']:.0%}")
        print(f"   السبب: {result['reasoning']}")
    
    print("\n✅ النموذج البسيط يعمل!")
