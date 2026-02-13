import pandas as pd
import numpy as np
import random

def create_additional_network_data(n_samples=25000):
    """إنشاء بيانات شبكة إضافية بدون sklearn"""
    
    print(f"🔄 إنشاء {n_samples:,} عينة إضافية...")
    
    data = []
    
    for i in range(n_samples):
        # أنواع شبكات مختلفة
        network_types = ['WiFi', '4G', '5G', 'LAN', 'Satellite']
        locations = ['Urban', 'Suburban', 'Rural', 'Remote']
        
        network_type = random.choice(network_types)
        location = random.choice(locations)
        
        # معاملات أساسية بناءً على نوع الشبكة
        if network_type == '5G':
            base_speed = random.uniform(150, 300)
            base_latency = random.uniform(5, 25)
            base_stability = 0.9
        elif network_type == 'LAN':
            base_speed = random.uniform(500, 1000)
            base_latency = random.uniform(1, 10)
            base_stability = 0.95
        elif network_type == 'WiFi':
            base_speed = random.uniform(50, 200)
            base_latency = random.uniform(10, 50)
            base_stability = 0.8
        elif network_type == '4G':
            base_speed = random.uniform(20, 100)
            base_latency = random.uniform(30, 100)
            base_stability = 0.7
        else:  # Satellite
            base_speed = random.uniform(10, 50)
            base_latency = random.uniform(500, 800)
            base_stability = 0.6
        
        # تأثير الموقع
        location_factor = {
            'Urban': random.uniform(1.0, 1.2),
            'Suburban': random.uniform(0.8, 1.0),
            'Rural': random.uniform(0.5, 0.8),
            'Remote': random.uniform(0.3, 0.6)
        }[location]
        
        # تأثير الوقت
        hour = i % 24
        if 8 <= hour <= 10 or 18 <= hour <= 22:  # ذروة
            time_factor = random.uniform(0.6, 0.8)
        elif 2 <= hour <= 6:  # هدوء
            time_factor = random.uniform(1.1, 1.3)
        else:
            time_factor = random.uniform(0.9, 1.1)
        
        # الأجهزة والاتصالات
        connected_devices = random.randint(1, 12)
        concurrent_connections = random.randint(1, connected_devices * 3)
        
        # حساب المعاملات النهائية
        download_speed = base_speed * location_factor * time_factor
        upload_speed = download_speed * random.uniform(0.1, 0.8)
        latency = base_latency / location_factor * (1 + connected_devices * 0.02)
        packet_loss = (1 - base_stability) * 5 * random.uniform(0.5, 2.0)
        jitter = latency * random.uniform(0.05, 0.3)
        bandwidth_util = min(100, concurrent_connections * 8 + random.uniform(10, 40))
        
        # تقييم الجودة
        stability_score = (
            (1 - packet_loss / 20) * 0.4 +
            (1 - jitter / max(latency, 1)) * 0.3 +
            (download_speed / base_speed) * 0.3
        )
        
        is_stable = stability_score > 0.6
        has_disconnection = random.random() < (packet_loss / 100 + latency / 1000)
        
        if stability_score > 0.8:
            quality = 'Good'
        elif stability_score > 0.5:
            quality = 'Average'
        else:
            quality = 'Poor'
        
        # إنشاء العينة
        sample = {
            'download_speed': round(download_speed, 2),
            'upload_speed': round(upload_speed, 2),
            'latency': round(latency, 2),
            'packet_loss': round(max(0, packet_loss), 3),
            'jitter': round(jitter, 2),
            'bandwidth_utilization': round(bandwidth_util, 1),
            'network_type': network_type,
            'connected_devices': connected_devices,
            'concurrent_connections': concurrent_connections,
            'time_of_day': hour,
            'location': location,
            'is_stable': is_stable,
            'has_disconnection': has_disconnection,
            'network_quality': quality,
            'deviation_score': round(abs(stability_score - base_stability), 4),
            'stability_score': round(stability_score, 4),
            'quality_score': round(stability_score, 4),
            
            # تصحيحات BARH
            'buffer_optimization': 1 if packet_loss > 3 or has_disconnection else 0,
            'connection_pooling': 1 if latency > 80 or quality == 'Poor' else 0,
            'route_optimization': 1 if latency > 150 else 0,
            'adaptive_compression': 1 if bandwidth_util > 75 else 0,
            'parallel_connections': 1 if download_speed < 25 or concurrent_connections > 10 else 0,
            'predictive_prefetch': 1 if jitter > 20 or not is_stable else 0
        }
        
        data.append(sample)
    
    df = pd.DataFrame(data)
    print("✅ تم إنشاء البيانات الإضافية!")
    return df

def merge_datasets():
    """دمج البيانات"""
    
    print("🔄 دمج البيانات...")
    
    # تحميل البيانات الحالية
    try:
        current_data = pd.read_csv('realistic_network_dataset.csv')
        print(f"✅ البيانات الحالية: {len(current_data):,} عينة")
    except:
        print("❌ لم يتم العثور على البيانات الحالية")
        return None
    
    # إنشاء بيانات إضافية
    additional_data = create_additional_network_data(25000)
    
    # معالجة البيانات النصية في البيانات الإضافية
    network_type_map = {'WiFi': 0, '4G': 1, '5G': 2, 'LAN': 3, 'Satellite': 4}
    location_map = {'Urban': 0, 'Suburban': 1, 'Rural': 2, 'Remote': 3}
    
    additional_data['network_type_encoded'] = additional_data['network_type'].map(network_type_map)
    additional_data['location_encoded'] = additional_data['location'].map(location_map)
    
    # إزالة الأعمدة النصية للتوافق
    additional_data = additional_data.drop(['network_type', 'location'], axis=1)
    
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
        print(f"\n📊 إحصائيات التصحيحات في البيانات المدمجة:")
        correction_cols = ['buffer_optimization', 'connection_pooling', 'route_optimization',
                          'adaptive_compression', 'parallel_connections', 'predictive_prefetch']
        
        for col in correction_cols:
            count = combined_dataset[col].sum()
            percentage = count / len(combined_dataset) * 100
            print(f"  {col}: {count:,} ({percentage:.1f}%)")
        
        print(f"\n📋 حجم الملف النهائي:")
        import os
        file_size = os.path.getsize('combined_network_dataset.csv') / (1024 * 1024)
        print(f"  {file_size:.1f} MB")
