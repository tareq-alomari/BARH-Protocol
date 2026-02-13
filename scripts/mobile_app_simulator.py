#!/usr/bin/env python3
"""
محاكي تطبيق الموبايل لاختبار BARH
Mobile App Simulator for BARH Testing
"""
import requests
import time
import json
import threading
from datetime import datetime

class MobileAppSimulator:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.running = False
        
    def test_connection(self):
        """اختبار الاتصال بخادم BARH"""
        try:
            response = requests.get(f"{self.server_url}/api/barh/test", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'latency': data.get('current_latency', 0),
                    'recommendation': data.get('recommendation', 'unknown'),
                    'confidence': data.get('confidence', 0)
                }
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_network_data(self, network_data):
        """إرسال بيانات الشبكة للتحليل"""
        try:
            payload = {'network_data': network_data}
            response = requests.post(
                f"{self.server_url}/api/barh/analyze", 
                json=payload, 
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def simulate_mobile_usage(self, duration=60):
        """محاكاة استخدام التطبيق المحمول"""
        print("📱 بدء محاكاة تطبيق الموبايل")
        print("=" * 50)
        
        self.running = True
        start_time = time.time()
        cycle = 1
        
        while self.running and (time.time() - start_time) < duration:
            print(f"\n📊 دورة {cycle} - {datetime.now().strftime('%H:%M:%S')}")
            
            # اختبار الاتصال
            result = self.test_connection()
            
            if result['success']:
                print(f"✅ متصل بـ BARH")
                print(f"🏓 التأخير: {result['latency']:.1f}ms")
                print(f"🎯 التوصية: {self.get_arabic_action(result['recommendation'])}")
                print(f"🎲 الثقة: {result['confidence']:.0%}")
                
                # محاكاة تطبيق التوصية
                self.simulate_action_application(result['recommendation'])
                
            else:
                print(f"❌ فشل الاتصال: {result['error']}")
            
            cycle += 1
            time.sleep(5)  # انتظار 5 ثوان
        
        print(f"\n🏁 انتهت المحاكاة بعد {cycle-1} دورات")
    
    def get_arabic_action(self, action):
        """ترجمة الإجراءات للعربية"""
        actions = {
            "no_action": "لا حاجة لإجراء",
            "route_optimization": "تحسين المسار",
            "data_compression": "ضغط البيانات",
            "predictive_prefetch": "جلب تنبؤي"
        }
        return actions.get(action, action)
    
    def simulate_action_application(self, action):
        """محاكاة تطبيق الإجراء في التطبيق"""
        if action == "route_optimization":
            print("   🔄 تطبيق تحسين المسار...")
        elif action == "data_compression":
            print("   📦 تفعيل ضغط البيانات...")
        elif action == "predictive_prefetch":
            print("   ⚡ بدء الجلب التنبؤي...")
        else:
            print("   ✅ لا إجراء مطلوب")
    
    def stop(self):
        """إيقاف المحاكاة"""
        self.running = False

class MobileTestSuite:
    def __init__(self):
        self.simulator = MobileAppSimulator()
    
    def run_comprehensive_mobile_test(self):
        """اختبار شامل للتطبيق المحمول"""
        print("🚀 اختبار BARH للتطبيقات المحمولة")
        print("=" * 60)
        
        # اختبار الاتصال الأولي
        print("🔍 اختبار الاتصال الأولي...")
        result = self.simulator.test_connection()
        
        if not result['success']:
            print(f"❌ فشل الاتصال: {result['error']}")
            print("💡 تأكد من تشغيل الخادم: python3 mobile_api_server.py")
            return
        
        print("✅ الاتصال ناجح!")
        print(f"🏓 التأخير الحالي: {result['latency']:.1f}ms")
        
        # اختبار إرسال بيانات مخصصة
        print("\n📤 اختبار إرسال بيانات مخصصة...")
        test_data = [150, 25, 0.6, 2048, 5000, 0.85, 0.15, 300]
        
        analysis_result = self.simulator.send_network_data(test_data)
        if analysis_result['success']:
            decision = analysis_result['barh_decision']
            print(f"✅ تحليل ناجح")
            print(f"🎯 القرار: {self.simulator.get_arabic_action(decision['action'])}")
            print(f"🎲 الثقة: {decision['confidence']:.0%}")
        else:
            print(f"❌ فشل التحليل: {analysis_result['error']}")
        
        # محاكاة الاستخدام المستمر
        print("\n🔄 بدء المحاكاة المستمرة...")
        try:
            self.simulator.simulate_mobile_usage(duration=30)
        except KeyboardInterrupt:
            print("\n⏹️  تم إيقاف المحاكاة")
            self.simulator.stop()

def main():
    """الدالة الرئيسية"""
    print("📱 مرحباً بك في اختبار BARH للموبايل")
    print("=" * 50)
    
    test_suite = MobileTestSuite()
    
    try:
        test_suite.run_comprehensive_mobile_test()
        print("\n✅ انتهى الاختبار بنجاح!")
        
    except Exception as e:
        print(f"\n❌ خطأ: {e}")

if __name__ == "__main__":
    main()
