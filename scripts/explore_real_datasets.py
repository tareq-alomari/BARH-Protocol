import pandas as pd
import numpy as np

def explore_datasets():
    """استكشاف جميع datasets الموجودة"""
    
    datasets_info = []
    
    print("🔍 استكشاف Datasets الموجودة...\n")
    
    # Dataset 1: Network Anomaly Detection
    try:
        df1 = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive/network_dataset_labeled.csv')
        info1 = {
            'name': 'Network Anomaly Detection',
            'file': 'network_dataset_labeled.csv',
            'samples': len(df1),
            'features': len(df1.columns),
            'columns': list(df1.columns),
            'target': 'anomaly',
            'description': 'كشف الشذوذ في الشبكة مع معاملات: bandwidth, throughput, congestion, packet_loss, latency, jitter'
        }
        datasets_info.append(info1)
        print(f"✅ {info1['name']}: {info1['samples']:,} عينة، {info1['features']} معامل")
        
    except Exception as e:
        print(f"❌ خطأ في تحميل Network Anomaly: {e}")
    
    # Dataset 2: Internet Speed Prediction
    try:
        df2 = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive (1)/Internet Speed.csv')
        info2 = {
            'name': 'Internet Speed Prediction',
            'file': 'Internet Speed.csv',
            'samples': len(df2),
            'features': len(df2.columns),
            'columns': list(df2.columns),
            'target': 'Internet_speed',
            'description': 'التنبؤ بسرعة الإنترنت مع معاملات: Ping_latency, Download_speed, Upload_speed, Packet_loss_rate'
        }
        datasets_info.append(info2)
        print(f"✅ {info2['name']}: {info2['samples']:,} عينة، {info2['features']} معامل")
        
    except Exception as e:
        print(f"❌ خطأ في تحميل Internet Speed: {e}")
    
    # Dataset 3: IoT Network Traffic (ESP32)
    try:
        df3a = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive (2)/esp32_1_data.csv')
        df3b = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive (2)/esp32_2_data.csv')
        info3 = {
            'name': 'IoT Network Traffic (ESP32)',
            'file': 'esp32_1_data.csv + esp32_2_data.csv',
            'samples': len(df3a) + len(df3b),
            'features': len(df3a.columns),
            'columns': list(df3a.columns),
            'target': 'time_series_prediction',
            'description': 'بيانات IoT حقيقية: temperature, humidity, latency, throughput, packet_loss, rssi'
        }
        datasets_info.append(info3)
        print(f"✅ {info3['name']}: {info3['samples']:,} عينة، {info3['features']} معامل")
        
    except Exception as e:
        print(f"❌ خطأ في تحميل IoT Traffic: {e}")
    
    return datasets_info

def create_unified_dataset(datasets_info):
    """دمج جميع datasets في dataset موحد لـ BARH"""
    
    print(f"\n🔄 دمج جميع Datasets...")
    
    unified_data = []
    
    # معالجة Network Anomaly Dataset
    try:
        df1 = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive/network_dataset_labeled.csv')
        
        for _, row in df1.iterrows():
            sample = {
                'download_speed': row.get('throughput', 50) * 10,  # تحويل لـ Mbps
                'upload_speed': row.get('throughput', 50) * 5,
                'latency': row.get('latency', 50),
                'packet_loss': row.get('packet_loss', 0) * 100,  # تحويل لنسبة مئوية
                'jitter': row.get('jitter', 5),
                'bandwidth_utilization': row.get('congestion', 0.5) * 100,
                'connected_devices': np.random.randint(1, 10),
                'concurrent_connections': np.random.randint(1, 20),
                'time_of_day': np.random.randint(0, 24),
                'network_type_encoded': np.random.randint(0, 5),
                'location_encoded': np.random.randint(0, 4),
                
                # النتائج
                'is_stable': row.get('anomaly', 0) == 0,
                'has_disconnection': row.get('anomaly', 0) == 1,
                'network_quality': 'Good' if row.get('anomaly', 0) == 0 else 'Poor',
                'deviation_score': row.get('anomaly', 0) * 0.8,
                'stability_score': 0.9 if row.get('anomaly', 0) == 0 else 0.2,
                'quality_score': 0.8 if row.get('anomaly', 0) == 0 else 0.3,
                
                # تصحيحات BARH
                'buffer_optimization': 1 if row.get('packet_loss', 0) > 0.01 else 0,
                'connection_pooling': 1 if row.get('latency', 0) > 50 else 0,
                'route_optimization': 1 if row.get('latency', 0) > 100 else 0,
                'adaptive_compression': 1 if row.get('congestion', 0) > 0.7 else 0,
                'parallel_connections': 1 if row.get('throughput', 0) < 1 else 0,
                'predictive_prefetch': 1 if row.get('jitter', 0) > 10 else 0
            }
            unified_data.append(sample)
            
        print(f"✅ تم معالجة Network Anomaly: {len(df1):,} عينة")
        
    except Exception as e:
        print(f"❌ خطأ في معالجة Network Anomaly: {e}")
    
    # معالجة Internet Speed Dataset
    try:
        df2 = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive (1)/Internet Speed.csv')
        
        for _, row in df2.iterrows():
            sample = {
                'download_speed': row.get('Download_speed', 50),
                'upload_speed': row.get('Upload_speed', 25),
                'latency': row.get('Ping_latency', 30),
                'packet_loss': row.get('Packet_loss_rate', 1),
                'jitter': row.get('Ping_latency', 30) * 0.1,  # تقدير
                'bandwidth_utilization': row.get('Network_congestion', 2) * 20,
                'connected_devices': np.random.randint(1, 8),
                'concurrent_connections': np.random.randint(1, 15),
                'time_of_day': np.random.randint(0, 24),
                'network_type_encoded': 1 if row.get('Connection_type_DSL', 0) > 0 else (2 if row.get('Connection_type_Cable', 0) > 0 else 3),
                'location_encoded': np.random.randint(0, 4),
                
                # النتائج بناءً على جودة الشبكة
                'is_stable': row.get('Internet_speed', 500) > 500,
                'has_disconnection': row.get('Packet_loss_rate', 1) > 2,
                'network_quality': 'Good' if row.get('Internet_speed', 500) > 800 else ('Average' if row.get('Internet_speed', 500) > 400 else 'Poor'),
                'deviation_score': abs(row.get('Internet_speed', 500) - 500) / 1000,
                'stability_score': min(1.0, row.get('Internet_speed', 500) / 1000),
                'quality_score': min(1.0, row.get('Internet_speed', 500) / 1200),
                
                # تصحيحات BARH
                'buffer_optimization': 1 if row.get('Packet_loss_rate', 1) > 1.5 else 0,
                'connection_pooling': 1 if row.get('Ping_latency', 30) > 40 else 0,
                'route_optimization': 1 if row.get('Ping_latency', 30) > 60 else 0,
                'adaptive_compression': 1 if row.get('Network_congestion', 2) > 3 else 0,
                'parallel_connections': 1 if row.get('Download_speed', 50) < 30 else 0,
                'predictive_prefetch': 1 if row.get('ISP_quality', 5) < 4 else 0
            }
            unified_data.append(sample)
            
        print(f"✅ تم معالجة Internet Speed: {len(df2):,} عينة")
        
    except Exception as e:
        print(f"❌ خطأ في معالجة Internet Speed: {e}")
    
    # معالجة IoT Traffic Dataset
    try:
        df3a = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive (2)/esp32_1_data.csv')
        df3b = pd.read_csv('/home/tareq/CS/paper/BARH-Project/research/data/archive (2)/esp32_2_data.csv')
        
        for df3 in [df3a, df3b]:
            for _, row in df3.iterrows():
                sample = {
                    'download_speed': row.get('throughput(bytes/sec)', 0.054) * 1000,  # تحويل لـ Mbps
                    'upload_speed': row.get('throughput(bytes/sec)', 0.054) * 500,
                    'latency': row.get('latency(ms)', 0.3),
                    'packet_loss': row.get('packet_loss(%)', 0),
                    'jitter': row.get('latency(ms)', 0.3) * 0.2,
                    'bandwidth_utilization': min(100, abs(row.get('rssi(dBm)', -60)) + 20),
                    'connected_devices': np.random.randint(1, 5),  # IoT عادة أقل
                    'concurrent_connections': np.random.randint(1, 8),
                    'time_of_day': np.random.randint(0, 24),
                    'network_type_encoded': 0,  # WiFi للـ IoT
                    'location_encoded': np.random.randint(0, 4),
                    
                    # النتائج بناءً على قوة الإشارة
                    'is_stable': row.get('rssi(dBm)', -60) > -70,
                    'has_disconnection': row.get('packet_loss(%)', 0) > 0,
                    'network_quality': 'Good' if row.get('rssi(dBm)', -60) > -60 else ('Average' if row.get('rssi(dBm)', -60) > -75 else 'Poor'),
                    'deviation_score': abs(row.get('rssi(dBm)', -60) + 60) / 100,
                    'stability_score': max(0, (100 + row.get('rssi(dBm)', -60)) / 100),
                    'quality_score': max(0, (90 + row.get('rssi(dBm)', -60)) / 90),
                    
                    # تصحيحات BARH للـ IoT
                    'buffer_optimization': 1 if row.get('packet_loss(%)', 0) > 0 else 0,
                    'connection_pooling': 1 if row.get('latency(ms)', 0.3) > 0.5 else 0,
                    'route_optimization': 1 if row.get('rssi(dBm)', -60) < -75 else 0,
                    'adaptive_compression': 1 if row.get('throughput(bytes/sec)', 0.054) < 0.05 else 0,
                    'parallel_connections': 1 if row.get('rssi(dBm)', -60) < -70 else 0,
                    'predictive_prefetch': 1 if row.get('latency(ms)', 0.3) > 0.4 else 0
                }
                unified_data.append(sample)
                
        print(f"✅ تم معالجة IoT Traffic: {len(df3a) + len(df3b):,} عينة")
        
    except Exception as e:
        print(f"❌ خطأ في معالجة IoT Traffic: {e}")
    
    # إنشاء DataFrame موحد
    unified_df = pd.DataFrame(unified_data)
    
    # حفظ البيانات الموحدة
    unified_df.to_csv('/home/tareq/CS/paper/BARH-Project/ultimate_network_dataset.csv', index=False)
    
    print(f"\n🎉 تم إنشاء Dataset موحد!")
    print(f"📊 إجمالي العينات: {len(unified_df):,}")
    print(f"📁 تم الحفظ في: ultimate_network_dataset.csv")
    
    return unified_df

# تشغيل الاستكشاف والدمج
if __name__ == "__main__":
    datasets_info = explore_datasets()
    
    print(f"\n📋 ملخص Datasets المكتشفة:")
    for info in datasets_info:
        print(f"  • {info['name']}: {info['samples']:,} عينة")
        print(f"    المعاملات: {', '.join(info['columns'][:5])}...")
        print(f"    الوصف: {info['description']}\n")
    
    # دمج جميع البيانات
    ultimate_dataset = create_unified_dataset(datasets_info)
    
    if ultimate_dataset is not None:
        print(f"\n📊 إحصائيات Dataset النهائي:")
        correction_cols = ['buffer_optimization', 'connection_pooling', 'route_optimization',
                          'adaptive_compression', 'parallel_connections', 'predictive_prefetch']
        
        for col in correction_cols:
            count = ultimate_dataset[col].sum()
            percentage = count / len(ultimate_dataset) * 100
            print(f"  {col}: {count:,} ({percentage:.1f}%)")
