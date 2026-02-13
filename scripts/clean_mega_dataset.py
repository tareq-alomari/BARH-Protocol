import pandas as pd
import numpy as np

def clean_mega_dataset():
    """تنظيف ومعالجة MEGA DATASET"""
    
    print("🔧 بدء تنظيف MEGA DATASET...")
    
    # تحميل البيانات
    data = pd.read_csv('MEGA_NETWORK_DATASET.csv')
    original_size = len(data)
    
    print(f"📊 البيانات الأصلية: {original_size:,} عينة")
    
    # 1. إزالة القيم المكررة
    data = data.drop_duplicates()
    print(f"🔄 بعد إزالة المكررات: {len(data):,} عينة (-{original_size - len(data):,})")
    
    # 2. تنظيف القيم الشاذة
    print("🧹 تنظيف القيم الشاذة...")
    
    # تحديد الحدود المنطقية
    limits = {
        'download_speed': (0.1, 2000),      # 0.1 - 2000 Mbps
        'upload_speed': (0.05, 1000),       # 0.05 - 1000 Mbps  
        'latency': (0.1, 1000),             # 0.1 - 1000 ms
        'packet_loss': (0, 50),             # 0 - 50%
        'jitter': (0, 200),                 # 0 - 200 ms
        'bandwidth_utilization': (0, 100),  # 0 - 100%
        'connected_devices': (1, 50),       # 1 - 50 devices
        'concurrent_connections': (1, 100)  # 1 - 100 connections
    }
    
    # تطبيق الحدود
    for col, (min_val, max_val) in limits.items():
        before = len(data)
        data = data[(data[col] >= min_val) & (data[col] <= max_val)]
        removed = before - len(data)
        if removed > 0:
            print(f"   {col}: أزيل {removed:,} عينة شاذة")
    
    print(f"✅ بعد تنظيف القيم الشاذة: {len(data):,} عينة")
    
    # 3. معالجة القيم المتطرفة باستخدام IQR
    print("📊 معالجة القيم المتطرفة...")
    
    numeric_cols = ['download_speed', 'upload_speed', 'latency', 'packet_loss', 'jitter', 'bandwidth_utilization']
    
    for col in numeric_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # حدود IQR المتساهلة (3 * IQR بدلاً من 1.5)
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        
        before = len(data)
        data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
        removed = before - len(data)
        
        if removed > 0:
            print(f"   {col}: أزيل {removed:,} قيمة متطرفة")
    
    print(f"✅ بعد معالجة القيم المتطرفة: {len(data):,} عينة")
    
    # 4. توازن البيانات
    print("⚖️ توازن البيانات...")
    
    # عد العينات لكل جودة
    quality_counts = data['network_quality'].value_counts()
    print(f"   توزيع الجودة الحالي:")
    for quality, count in quality_counts.items():
        print(f"     {quality}: {count:,} ({count/len(data)*100:.1f}%)")
    
    # تحديد الحد الأدنى للتوازن
    min_samples = min(quality_counts)
    target_samples = min(min_samples * 3, 15000)  # حد أقصى 15,000 لكل فئة
    
    print(f"   هدف التوازن: {target_samples:,} عينة لكل فئة")
    
    # أخذ عينات متوازنة
    balanced_data = []
    for quality in quality_counts.index:
        quality_data = data[data['network_quality'] == quality]
        if len(quality_data) > target_samples:
            quality_sample = quality_data.sample(n=target_samples, random_state=42)
        else:
            quality_sample = quality_data
        balanced_data.append(quality_sample)
    
    data = pd.concat(balanced_data, ignore_index=True)
    
    # خلط البيانات
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"✅ بعد التوازن: {len(data):,} عينة")
    
    # 5. التحقق النهائي
    print("\n🔍 التحقق النهائي:")
    print(f"   📊 العينات النهائية: {len(data):,}")
    print(f"   📋 الأعمدة: {len(data.columns)}")
    print(f"   ❌ قيم مفقودة: {data.isnull().sum().sum()}")
    print(f"   🔄 قيم مكررة: {data.duplicated().sum()}")
    
    # توزيع الجودة النهائي
    final_quality = data['network_quality'].value_counts()
    print(f"\n📈 التوزيع النهائي:")
    for quality, count in final_quality.items():
        print(f"   {quality}: {count:,} ({count/len(data)*100:.1f}%)")
    
    # حفظ البيانات المنظفة
    clean_file = 'MEGA_NETWORK_DATASET_CLEAN.csv'
    data.to_csv(clean_file, index=False)
    
    print(f"\n💾 تم حفظ البيانات المنظفة في: {clean_file}")
    print(f"📉 تم تقليل البيانات من {original_size:,} إلى {len(data):,} عينة")
    print(f"🎯 معدل الاحتفاظ: {len(data)/original_size*100:.1f}%")
    
    return data

if __name__ == "__main__":
    cleaned_data = clean_mega_dataset()
    
    print(f"\n✅ تنظيف البيانات مكتمل!")
    print(f"🎯 البيانات جاهزة للتدريب بجودة عالية")
