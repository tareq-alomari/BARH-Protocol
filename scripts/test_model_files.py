"""
اختبار سريع لوجود ملفات النموذج
"""
import os
import pickle

def check_model_files():
    """فحص ملفات النموذج"""
    files = {
        "النموذج الرئيسي": "models/best_model.h5",
        "الأوزان": "models/best_weights.weights.h5", 
        "معالج البيانات": "models/scaler.pkl"
    }
    
    print("🔍 فحص ملفات النموذج:")
    print("=" * 40)
    
    all_exist = True
    for name, path in files.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {name}: {path} ({size:,} bytes)")
        else:
            print(f"❌ {name}: {path} - غير موجود")
            all_exist = False
    
    return all_exist

def test_scaler():
    """اختبار معالج البيانات"""
    try:
        with open("models/scaler.pkl", 'rb') as f:
            scaler = pickle.load(f)
        print(f"\n📊 معالج البيانات:")
        print(f"   النوع: {type(scaler).__name__}")
        return True
    except Exception as e:
        print(f"❌ خطأ في تحميل المعالج: {e}")
        return False

if __name__ == "__main__":
    print("🤖 فحص نموذج BARH")
    
    if check_model_files():
        print("\n🎯 جميع الملفات موجودة!")
        
        if test_scaler():
            print("✅ المعالج يعمل بشكل صحيح")
        
        print("\n📋 للاستخدام الكامل:")
        print("1. pip install tensorflow flask numpy pandas scikit-learn")
        print("2. python3 barh_model_loader.py")
        print("3. python3 barh_api.py")
        
    else:
        print("\n❌ بعض الملفات مفقودة")
