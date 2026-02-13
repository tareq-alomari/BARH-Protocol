import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from sklearn.preprocessing import LabelEncoder
import json

class RealisticNetworkDataset:
    """مولد بيانات شبكة واقعية للتدريب"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        # أنواع الشبكات وخصائصها
        self.network_types = {
            'WiFi': {'base_speed': 100, 'latency_range': (10, 50), 'stability': 0.8},
            '4G': {'base_speed': 50, 'latency_range': (30, 100), 'stability': 0.7},
            '5G': {'base_speed': 200, 'latency_range': (5, 30), 'stability': 0.9},
            'LAN': {'base_speed': 1000, 'latency_range': (1, 10), 'stability': 0.95},
            'Satellite': {'base_speed': 25, 'latency_range': (500, 800), 'stability': 0.6}
        }
        
        # المواقع الجغرافية (اختياري)
        self.locations = ['Urban', 'Suburban', 'Rural', 'Remote']
        
    def generate_realistic_dataset(self, num_samples=100000):
        """توليد dataset واقعي"""
        
        print(f"🔄 توليد {num_samples:,} عينة من بيانات الشبكة الواقعية...")
        
        data = []
        
        for i in range(num_samples):
            if i % 10000 == 0:
                print(f"   تم توليد {i:,} عينة...")
            
            # اختيار نوع الشبكة
            network_type = random.choice(list(self.network_types.keys()))
            network_props = self.network_types[network_type]
            
            # التوقيت (24 ساعة)
            hour = i % 24
            time_factor = self._get_time_factor(hour)
            
            # الموقع الجغرافي
            location = random.choice(self.locations)
            location_factor = self._get_location_factor(location)
            
            # عدد الأجهزة المتصلة
            connected_devices = np.random.poisson(5) + 1  # 1-15 جهاز عادة
            
            # عدد الاتصالات المتزامنة
            concurrent_connections = np.random.poisson(connected_devices * 2)
            
            # === الخصائص الأساسية (Features) ===
            
            # 1. سرعة التحميل والتنزيل
            base_speed = network_props['base_speed']
            download_speed = base_speed * time_factor * location_factor * np.random.uniform(0.7, 1.3)
            upload_speed = download_speed * np.random.uniform(0.1, 0.8)  # عادة أقل من التحميل
            
            # تأثير الازدحام
            congestion_factor = max(0.1, 1 - (connected_devices - 1) * 0.05)
            download_speed *= congestion_factor
            upload_speed *= congestion_factor
            
            # 2. الكمون (Latency/Ping)
            base_latency = np.random.uniform(*network_props['latency_range'])
            latency = base_latency / location_factor * (1 + connected_devices * 0.02)
            
            # 3. فقدان الحزم (Packet Loss)
            base_packet_loss = (1 - network_props['stability']) * 5  # 0-5%
            packet_loss = base_packet_loss * (1 + concurrent_connections * 0.001)
            packet_loss = max(0, min(20, packet_loss))  # حد أقصى 20%
            
            # 4. التذبذب في الكمون (Jitter)
            jitter = latency * np.random.uniform(0.05, 0.3)
            
            # 5. استخدام الباندويث
            bandwidth_utilization = min(100, (concurrent_connections * 10) + np.random.uniform(10, 40))
            
            # === حساب النتائج (Labels) ===
            
            # 1. استقرار الاتصال
            stability_score = (
                (1 - packet_loss / 20) * 0.4 +  # تأثير فقدان الحزم
                (1 - jitter / latency) * 0.3 +   # تأثير التذبذب
                (download_speed / base_speed) * 0.3  # تأثير السرعة
            )
            is_stable = stability_score > 0.6
            
            # 2. حدوث انقطاع
            disconnection_probability = (
                packet_loss / 100 +  # كلما زاد فقدان الحزم
                (latency / 1000) +   # كلما زاد الكمون
                (1 - network_props['stability'])  # عدم استقرار نوع الشبكة
            )
            has_disconnection = np.random.random() < min(0.5, disconnection_probability)
            
            # 3. مستوى جودة الشبكة
            quality_score = (
                min(1, download_speed / 50) * 0.4 +  # سرعة جيدة > 50 Mbps
                min(1, (100 - latency) / 100) * 0.3 + # كمون منخفض
                (1 - packet_loss / 10) * 0.3          # فقدان حزم قليل
            )
            
            if quality_score > 0.8:
                network_quality = 'Good'
            elif quality_score > 0.5:
                network_quality = 'Average'
            else:
                network_quality = 'Poor'
            
            # 4. قيمة الانحراف (Deviation Score)
            # انحراف عن الأداء المتوقع لنوع الشبكة
            expected_performance = (
                network_props['base_speed'] / 100 +  # السرعة المتوقعة
                (1000 - network_props['latency_range'][1]) / 1000 +  # الكمون المتوقع
                network_props['stability']  # الاستقرار المتوقع
            ) / 3
            
            actual_performance = (
                download_speed / 100 +
                (1000 - latency) / 1000 +
                stability_score
            ) / 3
            
            deviation_score = abs(expected_performance - actual_performance)
            
            # إضافة البيانات
            sample = {
                # === الخصائص (Features) ===
                'download_speed': round(download_speed, 2),
                'upload_speed': round(upload_speed, 2),
                'latency': round(latency, 2),
                'packet_loss': round(packet_loss, 3),
                'jitter': round(jitter, 2),
                'bandwidth_utilization': round(bandwidth_utilization, 1),
                'network_type': network_type,
                'connected_devices': connected_devices,
                'concurrent_connections': concurrent_connections,
                'time_of_day': hour,
                'location': location,
                
                # معاملات إضافية مفيدة
                'congestion_factor': round(congestion_factor, 3),
                'time_factor': round(time_factor, 3),
                'location_factor': round(location_factor, 3),
                
                # === النتائج (Labels) ===
                'is_stable': is_stable,
                'has_disconnection': has_disconnection,
                'network_quality': network_quality,
                'deviation_score': round(deviation_score, 4),
                'stability_score': round(stability_score, 4),
                'quality_score': round(quality_score, 4),
                
                # تسميات BARH للتصحيح
                'needs_buffer_optimization': packet_loss > 2,
                'needs_connection_pooling': latency > 100,
                'needs_route_optimization': latency > 150,
                'needs_adaptive_compression': bandwidth_utilization > 80,
                'needs_parallel_connections': download_speed < 20,
                'needs_predictive_prefetch': jitter > latency * 0.2
            }
            
            data.append(sample)
        
        df = pd.DataFrame(data)
        print("✅ تم توليد البيانات الواقعية بنجاح!")
        return df
    
    def _get_time_factor(self, hour):
        """عامل التوقيت - الذروة في المساء"""
        if 8 <= hour <= 10 or 18 <= hour <= 22:  # ساعات الذروة
            return np.random.uniform(0.6, 0.8)  # أداء أقل
        elif 2 <= hour <= 6:  # ساعات الهدوء
            return np.random.uniform(1.1, 1.3)  # أداء أفضل
        else:
            return np.random.uniform(0.9, 1.1)  # أداء عادي
    
    def _get_location_factor(self, location):
        """عامل الموقع الجغرافي"""
        factors = {
            'Urban': np.random.uniform(1.0, 1.2),    # أفضل تغطية
            'Suburban': np.random.uniform(0.8, 1.0), # تغطية جيدة
            'Rural': np.random.uniform(0.5, 0.8),    # تغطية متوسطة
            'Remote': np.random.uniform(0.3, 0.6)    # تغطية ضعيفة
        }
        return factors[location]
    
    def add_barh_corrections(self, df):
        """إضافة تصحيحات BARH المطلوبة"""
        
        print("🔧 إضافة تصحيحات BARH...")
        
        # تصحيحات ذكية بناءً على الحالة الفعلية
        corrections = []
        
        for _, row in df.iterrows():
            correction = {
                'buffer_optimization': 0,
                'connection_pooling': 0,
                'route_optimization': 0,
                'adaptive_compression': 0,
                'parallel_connections': 0,
                'predictive_prefetch': 0
            }
            
            # قواعد ذكية للتصحيح
            if row['packet_loss'] > 3 or row['has_disconnection']:
                correction['buffer_optimization'] = 1
                
            if row['latency'] > 80 or row['network_quality'] == 'Poor':
                correction['connection_pooling'] = 1
                correction['route_optimization'] = 1
                
            if row['bandwidth_utilization'] > 75:
                correction['adaptive_compression'] = 1
                
            if row['download_speed'] < 25 or row['concurrent_connections'] > 10:
                correction['parallel_connections'] = 1
                
            if row['jitter'] > 20 or not row['is_stable']:
                correction['predictive_prefetch'] = 1
                
            corrections.append(correction)
        
        correction_df = pd.DataFrame(corrections)
        result = pd.concat([df, correction_df], axis=1)
        
        print("✅ تم إضافة تصحيحات BARH!")
        return result

# إنشاء Dataset واقعي
print("🚀 إنشاء Dataset واقعي لتدريب الذكاء الاصطناعي...")
generator = RealisticNetworkDataset()

# توليد 100,000 عينة
dataset = generator.generate_realistic_dataset(100000)

# إضافة تصحيحات BARH
final_dataset = generator.add_barh_corrections(dataset)

# حفظ البيانات
final_dataset.to_csv('/content/BARH-AI/data/realistic_network_dataset.csv', index=False)

print(f"\n📊 إحصائيات Dataset:")
print(f"عدد العينات: {len(final_dataset):,}")
print(f"عدد الخصائص: {len(final_dataset.columns)}")

# إحصائيات الجودة
print(f"\n📈 توزيع جودة الشبكة:")
quality_dist = final_dataset['network_quality'].value_counts()
for quality, count in quality_dist.items():
    print(f"  {quality}: {count:,} ({count/len(final_dataset)*100:.1f}%)")

print(f"\n🔧 إحصائيات التصحيحات:")
correction_cols = ['buffer_optimization', 'connection_pooling', 'route_optimization',
                  'adaptive_compression', 'parallel_connections', 'predictive_prefetch']
for col in correction_cols:
    count = final_dataset[col].sum()
    print(f"  {col}: {count:,} ({count/len(final_dataset)*100:.1f}%)")

print(f"\n💾 تم حفظ Dataset في: /content/BARH-AI/data/realistic_network_dataset.csv")
