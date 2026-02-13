"""
API بسيط لـ BARH - بدون مكتبات معقدة
"""
import json
from simple_barh import SimpleBARH

class SimpleAPI:
    def __init__(self):
        self.barh = SimpleBARH()
    
    def predict_json(self, data_str):
        """توقع من JSON"""
        try:
            data = json.loads(data_str)
            network_data = data.get('network_data', [])
            result = self.barh.predict(network_data)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    def demo(self):
        """عرض توضيحي"""
        print("🚀 BARH API Demo")
        print("=" * 30)
        
        # مثال 1: شبكة بطيئة
        slow_network = '{"network_data": [250, 20, 0.9, 1024, 512, 0.6, 0.1, 300]}'
        print("📡 شبكة بطيئة:")
        print(self.predict_json(slow_network))
        
        # مثال 2: شبكة سريعة
        fast_network = '{"network_data": [30, 100, 0.5, 2048, 1024, 0.95, 0.001, 25]}'
        print("\n⚡ شبكة سريعة:")
        print(self.predict_json(fast_network))

if __name__ == "__main__":
    api = SimpleAPI()
    api.demo()
    
    print("\n📋 للاستخدام:")
    print("from simple_api import SimpleAPI")
    print("api = SimpleAPI()")
    print('result = api.predict_json(\'{"network_data": [100,50,0.8,1024,512,0.95,0.01,80]}\')')
