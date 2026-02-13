#!/usr/bin/env python3
"""
خادم BARH API للتطبيقات المحمولة
BARH API Server for Mobile Applications
"""
from flask import Flask, request, jsonify
import psutil
import subprocess
import time
from simple_barh import SimpleBARH

app = Flask(__name__)
barh = SimpleBARH()

def get_mobile_network_stats():
    """إحصائيات الشبكة للموبايل"""
    try:
        net_io = psutil.net_io_counters()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # ping test
        try:
            result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if "time=" in line:
                        latency = float(line.split("time=")[1].split()[0])
                        break
                else:
                    latency = 999.0
            else:
                latency = 999.0
        except:
            latency = 999.0
        
        error_rate = (net_io.errin + net_io.errout) / max(net_io.packets_sent + net_io.packets_recv, 1)
        
        return [
            latency,
            net_io.bytes_sent / 1024 / 1024,
            cpu_percent / 100,
            memory.used / 1024 / 1024,
            net_io.packets_sent,
            1 - error_rate,
            error_rate,
            latency * 2
        ]
    except:
        return [100, 50, 0.5, 1024, 1000, 0.9, 0.01, 200]

@app.route('/api/barh/analyze', methods=['POST'])
def analyze_network():
    """تحليل الشبكة وإرجاع قرار BARH"""
    try:
        # الحصول على بيانات من الموبايل أو النظام
        if request.json and 'network_data' in request.json:
            network_data = request.json['network_data']
        else:
            network_data = get_mobile_network_stats()
        
        # تحليل BARH
        decision = barh.predict(network_data)
        
        return jsonify({
            'success': True,
            'network_stats': {
                'latency': network_data[0],
                'bandwidth': network_data[1],
                'cpu_usage': network_data[2],
                'memory_usage': network_data[3],
                'packets': network_data[4],
                'quality': network_data[5],
                'error_rate': network_data[6]
            },
            'barh_decision': decision,
            'timestamp': time.time()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/barh/status', methods=['GET'])
def get_status():
    """حالة الخادم"""
    return jsonify({
        'success': True,
        'server': 'BARH Mobile API',
        'version': '1.0',
        'status': 'running'
    })

@app.route('/api/barh/test', methods=['GET'])
def test_connection():
    """اختبار الاتصال"""
    network_data = get_mobile_network_stats()
    decision = barh.predict(network_data)
    
    return jsonify({
        'success': True,
        'message': 'اختبار الاتصال ناجح',
        'current_latency': network_data[0],
        'recommendation': decision['action'],
        'confidence': decision['confidence']
    })

if __name__ == '__main__':
    print("🚀 بدء خادم BARH API للموبايل")
    print("📱 الرابط: http://localhost:5000")
    print("🔗 اختبار: http://localhost:5000/api/barh/test")
    app.run(host='0.0.0.0', port=5000, debug=True)
