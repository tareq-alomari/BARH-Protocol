# 🏆 UPC Network Dataset - الأفضل للتدريب!

## 📊 **مواصفات Dataset**:

### ✅ **البيانات الحقيقية**:
- **8 أجهزة راوتر Huawei NetEngine 8000**
- **شبكة فعلية** بسرعة 1-40 Gbps
- **11 topologies** مختلفة (5-8 عقد)
- **10 routing policies** لكل topology

### ✅ **المعاملات المتوفرة**:
1. **Delay**: متوسط التأخير لكل حزمة (ثواني)
2. **Jitter**: تباين التأخير 
3. **Packet Loss**: عدد الحزم المفقودة/ثانية
4. **Throughput**: معدل البيانات (bits/s)
5. **Packet Size**: حجم الحزم (bits)
6. **Per-packet Info**: معلومات مفصلة لكل حزمة

### ✅ **أنواع Traffic**:
- **CBR (Constant Bit Rate)**: معدل ثابت
- **MB (Multi Burst)**: دفعات متعددة

## 🚀 **كيفية الاستخدام**:

### 1. تحميل البيانات:
```bash
python3 download_upc_dataset.py
```

### 2. استخراج الملفات:
```bash
unzip gnnet-ch23-dataset-mb.zip
unzip gnnet-ch23-dataset-cbr-mb.zip
```

### 3. معالجة البيانات:
```python
import networkx as nx
import pickle
import pandas as pd

# قراءة topology
G = nx.read_gml('graphs/graph_topology1.txt', destringizer=int)

# قراءة النتائج
with open('experimentResults.txt', 'r') as f:
    results = f.readlines()

# معالجة البيانات
for line in results:
    global_stats, path_metrics = line.strip().split('|')
    
    # الإحصائيات العامة
    capture_time, global_packets, global_losses, global_delay = global_stats.split(',')
    
    # معاملات كل مسار
    paths = path_metrics.split(';')
    for path in paths:
        metrics = path.split(',')
        # metrics[0] = traffic rate
        # metrics[1] = packets/sec
        # metrics[2] = packet loss/sec
        # metrics[3] = average delay
        # metrics[4] = log delay
        # metrics[5-9] = delay percentiles
        # metrics[10] = jitter (variance)
```

## 🎯 **المقارنة مع Dataset الحالي**:

| المعيار | Dataset الحالي | UPC Dataset |
|---------|----------------|-------------|
| **الحجم** | 50,000 عينة | 400GB+ |
| **المصدر** | مصطنع | **حقيقي** ✅ |
| **الأجهزة** | محاكاة | **راوترات فعلية** ✅ |
| **التفاصيل** | أساسي | **per-packet info** ✅ |
| **الجودة** | جيد | **احترافي** ✅ |

## 🤔 **التوصية**:

### **للبحث الأكاديمي**: استخدم UPC Dataset
- بيانات حقيقية من شبكة فعلية
- مقبول في المؤتمرات العالمية
- تفاصيل دقيقة جداً

### **للتطوير السريع**: استخدم Dataset الحالي
- جاهز للاستخدام فوراً
- متوافق مع الكود الموجود
- حجم مناسب للتجريب

## 🚀 **الخطة المقترحة**:

1. **ابدأ بـ Dataset الحالي** للتجريب السريع
2. **حمل UPC Dataset** للنتائج النهائية
3. **ادمج البيانات** للحصول على أفضل نتيجة

**🎉 UPC Dataset هو الأفضل للبحث الأكاديمي الجاد!**
