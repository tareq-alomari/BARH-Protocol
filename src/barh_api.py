"""
BARH Protocol API - واجهة برمجية لبروتوكول BARH
"""

from flask import Flask, request, jsonify
from barh_model_loader import BARHModelLoader
import numpy as np

app = Flask(__name__)

# تحميل النموذج عند بدء التشغيل
model_loader = BARHModelLoader()
model_loaded = model_loader.load_model()

@app.route('/health', methods=['GET'])
def health_check():
    """فحص حالة الخدمة"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded,
        "service": "BARH Protocol API"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """توقع الإجراء المطلوب للشبكة"""
    if not model_loaded:
        return jsonify({"error": "النموذج غير محمل"}), 500
    
    try:
        # استقبال البيانات
        data = request.json
        network_data = data.get('network_data', [])
        
        if len(network_data) != 8:
            return jsonify({"error": "يجب أن تحتوي البيانات على 8 قيم"}), 400
        
        # التوقع
        result = model_loader.predict_network_action(network_data)
        
        if result:
            return jsonify({
                "success": True,
                "prediction": result
            })
        else:
            return jsonify({"error": "فشل في التوقع"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """معلومات النموذج"""
    if not model_loaded:
        return jsonify({"error": "النموذج غير محمل"}), 500
    
    info = model_loader.get_model_info()
    return jsonify(info)

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """توقع متعدد للشبكات"""
    if not model_loaded:
        return jsonify({"error": "النموذج غير محمل"}), 500
    
    try:
        data = request.json
        batch_data = data.get('batch_data', [])
        
        results = []
        for network_data in batch_data:
            if len(network_data) == 8:
                result = model_loader.predict_network_action(network_data)
                results.append(result)
            else:
                results.append({"error": "بيانات غير صحيحة"})
        
        return jsonify({
            "success": True,
            "predictions": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if model_loaded:
        print("🚀 تشغيل BARH Protocol API...")
        print("📡 الخدمة متاحة على: http://localhost:5000")
        print("🔗 نقاط النهاية:")
        print("   - GET  /health")
        print("   - POST /predict")
        print("   - GET  /model-info")
        print("   - POST /batch-predict")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ لا يمكن تشغيل الخدمة - النموذج غير محمل")
        print("▶️  تشغيل: python download_model.py")
