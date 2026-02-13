"""
BARH Protocol Model Loader and Integration
تحميل ودمج نموذج بروتوكول BARH
"""

import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd

class BARHModelLoader:
    def __init__(self, model_path="models/best_model.h5", scaler_path="models/scaler.pkl"):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.is_loaded = False
    
    def load_model(self):
        """تحميل النموذج المدرب والمعالج"""
        try:
            # تحميل النموذج
            if os.path.exists(self.model_path):
                self.model = load_model(self.model_path)
                print(f"✅ تم تحميل النموذج من: {self.model_path}")
            else:
                print(f"❌ النموذج غير موجود في: {self.model_path}")
                return False
            
            # تحميل المعالج
            if os.path.exists(self.scaler_path):
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print(f"✅ تم تحميل المعالج من: {self.scaler_path}")
            else:
                print(f"❌ المعالج غير موجود في: {self.scaler_path}")
                return False
            
            self.is_loaded = True
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تحميل النموذج: {e}")
            return False
    
    def predict_network_action(self, network_data):
        """توقع الإجراء المطلوب للشبكة"""
        if not self.is_loaded:
            print("❌ يجب تحميل النموذج أولاً")
            return None
        
        try:
            # معالجة البيانات
            processed_data = self.scaler.transform([network_data])
            processed_data = processed_data.reshape(1, 1, -1)  # LSTM format
            
            # التوقع
            prediction = self.model.predict(processed_data, verbose=0)
            predicted_class = np.argmax(prediction[0])
            confidence = np.max(prediction[0])
            
            # تحويل الرقم إلى اسم الإجراء
            actions = {
                0: "no_action",
                1: "route_optimization", 
                2: "data_compression",
                3: "predictive_prefetch"
            }
            
            return {
                "action": actions.get(predicted_class, "unknown"),
                "confidence": float(confidence),
                "raw_prediction": prediction[0].tolist()
            }
            
        except Exception as e:
            print(f"❌ خطأ في التوقع: {e}")
            return None
    
    def get_model_info(self):
        """معلومات النموذج"""
        if not self.is_loaded:
            return "النموذج غير محمل"
        
        return {
            "model_params": self.model.count_params(),
            "input_shape": self.model.input_shape,
            "output_shape": self.model.output_shape,
            "layers": len(self.model.layers)
        }

# مثال للاستخدام
if __name__ == "__main__":
    # إنشاء محمل النموذج
    loader = BARHModelLoader()
    
    # تحميل النموذج
    if loader.load_model():
        print("🎯 النموذج جاهز للاستخدام!")
        print("📊 معلومات النموذج:", loader.get_model_info())
        
        # مثال على بيانات شبكة
        sample_data = [100.5, 50.2, 0.8, 1024, 512, 0.95, 0.1, 200]
        
        # توقع الإجراء
        result = loader.predict_network_action(sample_data)
        if result:
            print(f"🔮 التوقع: {result['action']}")
            print(f"📈 الثقة: {result['confidence']:.2%}")
    else:
        print("❌ فشل في تحميل النموذج")
