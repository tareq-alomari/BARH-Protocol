import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import random

def create_network_intrusion_dataset(n_samples=25000):
    """إنشاء dataset شبكات إضافي للدمج"""
    
    print(f"🔄 إنشاء {n_samples:,} عينة إضافية...")
    
    # إنشاء بيانات أساسية
    X, y = make_classification(
        n_samples=n_samples,
        n_features=10,
        n_informative=8,
        n_redundant=2,
        n_classes=2,
        random_state=42
    )
    
    # تحويل إلى معاملات شبكة واقعية
    data = []
    
    for i in range(n_samples):
        # معاملات الشبكة الأساسية
        sample = {
            'download_speed': max(1, X[i][0] * 50 + 100),  # 1-300 Mbps
            'upload_speed': max(0.5, X[i][1] * 25 + 50),   # 0.5-150 Mbps
            'latency': max(1, abs(X[i][2]) * 100 + 20),     # 1-200 ms
            'packet_loss': max(0, abs(X[i][3]) * 5),        # 0-10%
            'jitter': max(0.1, abs(X[i][4]) * 20 + 5),      # 0.1-50 ms
            'bandwidth_utilization': max(10, min(100, abs(X[i][5]) * 40 + 50)),  # 10-100%
            'connected_devices': max(1, int(abs(X[i][6]) * 5 + 3)),  # 1-15
            'concurrent_connections': max(1, int(abs(X[i][7]) * 10 + 5)),  # 1-25
            'time_of_day': i % 24,
            'network_type_encoded': random.randint(0, 4),
            'location_encoded': random.randint(0, 3),
            
            # النتائج (Labels) - بناءً على الشبكة
            'is_stable': y[i] == 1,
            'has_disconnection': y[i] == 0,
            'network_quality': 'Good' if y[i] == 1 else 'Poor',
            'deviation_score': abs(X[i][8]) * 0.5,
            'stability_score': 0.8 if y[i] == 1 else 0.3,
            'quality_score': 0.9 if y[i] == 1 else 0.2,
            
            # تصحيحات BARH
            'buffer_optimization': 1 if X[i][2] > 0.5 else 0,
            'connection_pooling': 1 if X[i][3] > 0.3 else 0,
            'route_optimization': 1 if X[i][4] > 0.4 else 0,
            'adaptive_compression': 1 if X[i][5] > 0.6 else 0,
            'parallel_connections': 1 if X[i][6] > 0.2 else 0,
            'predictive_prefetch': 1 if X[i][7] > 0.1 else 0
        }
        
        data.append(sample)
    
    df = pd.DataFrame(data)
    print("✅ تم إنشاء البيانات الإضافية!")
    return df

def merge_datasets():
    """دمج البيانات الحالية مع البيانات الإضافية"""
    
    print("🔄 دمج البيانات...")
    
    # تحميل البيانات الحالية
    try:
        current_data = pd.read_csv('realistic_network_dataset.csv')
        print(f"✅ تم تحميل البيانات الحالية: {len(current_data):,} عينة")
    except:
        print("❌ لم يتم العثور على البيانات الحالية")
        return None
    
    # إنشاء بيانات إضافية
    additional_data = create_network_intrusion_dataset(25000)
    
    # دمج البيانات
    combined_data = pd.concat([current_data, additional_data], ignore_index=True)
    
    # حفظ البيانات المدمجة
    combined_data.to_csv('combined_network_dataset.csv', index=False)
    
    print(f"🎉 تم الدمج بنجاح!")
    print(f"📊 إجمالي العينات: {len(combined_data):,}")
    print(f"📁 تم الحفظ في: combined_network_dataset.csv")
    
    return combined_data

# تشغيل الدمج
if __name__ == "__main__":
    combined_dataset = merge_datasets()
    
    if combined_dataset is not None:
        print(f"\n📋 عينة من البيانات المدمجة:")
        print(combined_dataset.head())
        
        print(f"\n📊 إحصائيات البيانات المدمجة:")
        print(combined_dataset.describe())
