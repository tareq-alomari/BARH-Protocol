# 📊 Dataset واقعي لتدريب الذكاء الاصطناعي - بروتوكول BARH

## 🎯 المواصفات المطلوبة (تم تنفيذها)

### ✅ الخصائص (Features) - 11 معامل أساسي:

1. **سرعة التحميل والتنزيل** (Download/Upload speed)
   - `download_speed`: 0.5 - 1300 Mbps
   - `upload_speed`: 0.05 - 1040 Mbps (عادة أقل من التحميل)

2. **الكمون** (Latency أو Ping)
   - `latency`: 1 - 850 ms حسب نوع الشبكة

3. **فقدان الحزم** (Packet Loss)
   - `packet_loss`: 0 - 20% (واقعي)

4. **التذبذب في الكمون** (Jitter)
   - `jitter`: 0.05 - 255 ms

5. **استخدام الباندويث** (Bandwidth utilization)
   - `bandwidth_utilization`: 10 - 100%

6. **نوع الشبكة** (Network Type)
   - `network_type`: WiFi, 4G, 5G, LAN, Satellite

7. **الأجهزة المتصلة**
   - `connected_devices`: 1 - 15 جهاز

8. **عدد الاتصالات المتزامنة**
   - `concurrent_connections`: 0 - 30 اتصال

9. **التوقيت** (Time of day)
   - `time_of_day`: 0 - 23 ساعة

10. **المواقع الجغرافية** (اختياري)
    - `location`: Urban, Suburban, Rural, Remote

11. **عوامل إضافية**:
    - `congestion_factor`: عامل الازدحام
    - `time_factor`: تأثير الوقت
    - `location_factor`: تأثير الموقع

---

### ✅ النتائج أو العلامات (Labels) - 6 مخرجات:

1. **استقرار الاتصال** (Stable/Unstable)
   - `is_stable`: True/False
   - `stability_score`: 0.0 - 1.0

2. **حدوث انقطاع** (Yes/No)
   - `has_disconnection`: True/False

3. **مستوى جودة الشبكة** (Good, Average, Poor)
   - `network_quality`: Good/Average/Poor
   - `quality_score`: 0.0 - 1.0

4. **قيم الانحراف** (Deviation score)
   - `deviation_score`: 0.0 - 1.0 (انحراف عن الأداء المتوقع)

5. **تصحيحات BARH المطلوبة** (6 أنواع):
   - `buffer_optimization`: 0/1
   - `connection_pooling`: 0/1
   - `route_optimization`: 0/1
   - `adaptive_compression`: 0/1
   - `parallel_connections`: 0/1
   - `predictive_prefetch`: 0/1

---

## 🔬 المنطق الواقعي المطبق:

### 📡 أنواع الشبكات وخصائصها:
- **WiFi**: سرعة متوسطة، كمون منخفض، استقرار جيد
- **4G**: سرعة متوسطة، كمون متوسط، استقرار متوسط
- **5G**: سرعة عالية، كمون منخفض جداً، استقرار ممتاز
- **LAN**: سرعة عالية جداً، كمون منخفض جداً، استقرار ممتاز
- **Satellite**: سرعة منخفضة، كمون عالي جداً، استقرار ضعيف

### ⏰ تأثير التوقيت:
- **ساعات الذروة** (8-10 صباحاً، 6-10 مساءً): أداء أقل
- **ساعات الهدوء** (2-6 صباحاً): أداء أفضل
- **الأوقات العادية**: أداء متوسط

### 🌍 تأثير الموقع الجغرافي:
- **Urban**: تغطية ممتازة (عامل 1.0-1.2)
- **Suburban**: تغطية جيدة (عامل 0.8-1.0)
- **Rural**: تغطية متوسطة (عامل 0.5-0.8)
- **Remote**: تغطية ضعيفة (عامل 0.3-0.6)

### 🔧 قواعد التصحيح الذكية:
- **Buffer Optimization**: عند فقدان حزم > 3% أو انقطاع
- **Connection Pooling**: عند كمون > 80ms أو جودة ضعيفة
- **Route Optimization**: عند كمون > 150ms
- **Adaptive Compression**: عند استخدام باندويث > 75%
- **Parallel Connections**: عند سرعة < 25 Mbps أو اتصالات كثيرة
- **Predictive Prefetch**: عند تذبذب > 20ms أو عدم استقرار

---

## 📈 إحصائيات Dataset (100,000 عينة):

### توزيع جودة الشبكة:
- **Good**: ~35,000 عينة (35%)
- **Average**: ~40,000 عينة (40%)
- **Poor**: ~25,000 عينة (25%)

### توزيع أنواع الشبكات:
- **WiFi**: ~20% من العينات
- **4G**: ~20% من العينات
- **5G**: ~20% من العينات
- **LAN**: ~20% من العينات
- **Satellite**: ~20% من العينات

### توزيع التصحيحات:
- **Buffer Optimization**: ~25% من العينات
- **Connection Pooling**: ~30% من العينات
- **Route Optimization**: ~20% من العينات
- **Adaptive Compression**: ~35% من العينات
- **Parallel Connections**: ~40% من العينات
- **Predictive Prefetch**: ~15% من العينات

---

## 🚀 كيفية الاستخدام:

```python
# تشغيل مولد البيانات
python realistic_dataset_generator.py

# تحميل البيانات
import pandas as pd
dataset = pd.read_csv('/content/BARH-AI/data/realistic_network_dataset.csv')

# فحص البيانات
print(dataset.head())
print(dataset.info())
print(dataset.describe())
```

---

## ✅ مطابقة المتطلبات:

| المتطلب | الحالة | التفاصيل |
|---------|--------|----------|
| سرعة التحميل/التنزيل | ✅ | `download_speed`, `upload_speed` |
| الكمون | ✅ | `latency` (1-850ms) |
| فقدان الحزم | ✅ | `packet_loss` (0-20%) |
| التذبذب | ✅ | `jitter` |
| استخدام الباندويث | ✅ | `bandwidth_utilization` |
| نوع الشبكة | ✅ | 5 أنواع مختلفة |
| الأجهزة المتصلة | ✅ | `connected_devices` |
| الاتصالات المتزامنة | ✅ | `concurrent_connections` |
| التوقيت | ✅ | `time_of_day` (0-23) |
| الموقع الجغرافي | ✅ | 4 مواقع مختلفة |
| استقرار الاتصال | ✅ | `is_stable`, `stability_score` |
| حدوث انقطاع | ✅ | `has_disconnection` |
| مستوى الجودة | ✅ | `network_quality` (3 مستويات) |
| قيم الانحراف | ✅ | `deviation_score` |

**🎉 جميع المتطلبات تم تنفيذها بنجاح مع منطق واقعي ومتقدم!**
