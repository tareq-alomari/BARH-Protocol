#!/bin/bash

echo "🚀 إعداد وتشغيل اختبار BARH للشبكة الحقيقية"
echo "=================================================="

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت"
    exit 1
fi

echo "✅ Python3 موجود"

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip3 install psutil --user

# التحقق من وجود الملفات المطلوبة
if [ ! -f "simple_barh.py" ]; then
    echo "❌ ملف simple_barh.py غير موجود"
    exit 1
fi

if [ ! -f "real_network_test.py" ]; then
    echo "❌ ملف real_network_test.py غير موجود"
    exit 1
fi

echo "✅ جميع الملفات موجودة"

# إعطاء صلاحيات التنفيذ
chmod +x real_network_test.py

echo ""
echo "🌐 بدء اختبار الشبكة..."
echo "=================================================="

# تشغيل الاختبار
python3 real_network_test.py

echo ""
echo "✅ انتهى الاختبار"
