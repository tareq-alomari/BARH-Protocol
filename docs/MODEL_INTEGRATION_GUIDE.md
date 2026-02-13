# دليل تحميل ودمج نموذج BARH

## الخطوات السريعة

### 1. تحضير البيئة
```bash
pip install -r requirements.txt
```

### 2. تنزيل النموذج من Colab
```bash
python download_model.py
```

**يدوياً من Colab:**
1. في Colab، اذهب إلى Files panel (📁)
2. انقر بالزر الأيمن على `best_model.h5` → Download
3. انقر بالزر الأيمن على `scaler.pkl` → Download
4. ضع الملفات في مجلد `models/`

### 3. اختبار النموذج
```bash
python barh_model_loader.py
```

### 4. تشغيل API
```bash
python barh_api.py
```

## استخدام النموذج في الكود

```python
from barh_model_loader import BARHModelLoader

# تحميل النموذج
loader = BARHModelLoader()
loader.load_model()

# بيانات الشبكة (8 قيم)
network_data = [100.5, 50.2, 0.8, 1024, 512, 0.95, 0.1, 200]

# التوقع
result = loader.predict_network_action(network_data)
print(f"الإجراء: {result['action']}")
print(f"الثقة: {result['confidence']:.2%}")
```

## استخدام API

```bash
# فحص الحالة
curl http://localhost:5000/health

# توقع واحد
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"network_data": [100.5, 50.2, 0.8, 1024, 512, 0.95, 0.1, 200]}'

# معلومات النموذج
curl http://localhost:5000/model-info
```

## هيكل الملفات
```
BARH-Project/
├── models/
│   ├── best_model.h5      # النموذج المدرب
│   └── scaler.pkl         # معالج البيانات
├── barh_model_loader.py   # محمل النموذج
├── barh_api.py           # واجهة API
├── download_model.py     # تنزيل النموذج
└── requirements.txt      # المتطلبات
```

## الإجراءات المتاحة
- `no_action`: لا يوجد إجراء مطلوب
- `route_optimization`: تحسين المسار
- `data_compression`: ضغط البيانات  
- `predictive_prefetch`: جلب تنبؤي للبيانات
