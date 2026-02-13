#!/usr/bin/env python3
"""
اختبار سريع للخادم والمحاكي
"""
import subprocess
import time
import requests
import os
import signal

def test_mobile_integration():
    print("📱 اختبار تكامل BARH مع التطبيقات المحمولة")
    print("=" * 60)
    
    # بدء الخادم
    print("🚀 بدء خادم BARH API...")
    
    # تشغيل الخادم في عملية منفصلة
    server_process = subprocess.Popen([
        "python3", "-c", """
from mobile_api_server import app
app.run(host='0.0.0.0', port=5000, debug=False)
"""
    ], cwd="/home/tareq/CS/paper/BARH-Project")
    
    # انتظار بدء الخادم
    print("⏳ انتظار بدء الخادم...")
    time.sleep(3)
    
    try:
        # اختبار الاتصال
        print("🔍 اختبار الاتصال...")
        response = requests.get("http://localhost:5000/api/barh/test", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ الخادم يعمل بنجاح!")
            print(f"🏓 التأخير: {data['current_latency']:.1f}ms")
            print(f"🎯 التوصية: {data['recommendation']}")
            print(f"🎲 الثقة: {data['confidence']:.0%}")
            
            # اختبار إرسال بيانات
            print("\n📤 اختبار إرسال بيانات...")
            test_data = {
                'network_data': [200, 30, 0.7, 1500, 3000, 0.8, 0.2, 400]
            }
            
            response = requests.post(
                "http://localhost:5000/api/barh/analyze", 
                json=test_data, 
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ تحليل البيانات ناجح!")
                print(f"🎯 القرار: {result['barh_decision']['action']}")
                print(f"🎲 الثقة: {result['barh_decision']['confidence']:.0%}")
            else:
                print(f"❌ فشل تحليل البيانات: {response.status_code}")
        
        else:
            print(f"❌ فشل الاتصال: {response.status_code}")
    
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
    
    finally:
        # إيقاف الخادم
        print("\n⏹️  إيقاف الخادم...")
        server_process.terminate()
        server_process.wait()
    
    print("\n✅ انتهى اختبار التكامل")

if __name__ == "__main__":
    test_mobile_integration()
