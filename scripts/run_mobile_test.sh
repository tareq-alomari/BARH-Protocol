#!/bin/bash

echo "📱 إعداد اختبار BARH للتطبيقات المحمولة"
echo "=============================================="

# التحقق من المتطلبات
echo "🔍 فحص المتطلبات..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت"
    exit 1
fi

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات..."
pip3 install flask requests --user

# التحقق من الملفات
required_files=("simple_barh.py" "mobile_api_server.py" "mobile_app_simulator.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ ملف مفقود: $file"
        exit 1
    fi
done

echo "✅ جميع الملفات موجودة"

# إنشاء ملف تشغيل الخادم
cat > start_server.py << 'EOF'
import subprocess
import sys
import time

print("🚀 بدء خادم BARH API...")
try:
    subprocess.run([sys.executable, "mobile_api_server.py"])
except KeyboardInterrupt:
    print("\n⏹️  تم إيقاف الخادم")
EOF

# إنشاء ملف تشغيل المحاكي
cat > start_simulator.py << 'EOF'
import subprocess
import sys
import time

print("⏳ انتظار بدء الخادم...")
time.sleep(3)

print("📱 بدء محاكي التطبيق...")
try:
    subprocess.run([sys.executable, "mobile_app_simulator.py"])
except KeyboardInterrupt:
    print("\n⏹️  تم إيقاف المحاكي")
EOF

echo ""
echo "🎯 خيارات التشغيل:"
echo "1. تشغيل الخادم فقط: python3 mobile_api_server.py"
echo "2. تشغيل المحاكي فقط: python3 mobile_app_simulator.py"
echo "3. تشغيل كلاهما في نوافذ منفصلة"
echo ""

read -p "اختر الخيار (1/2/3): " choice

case $choice in
    1)
        echo "🚀 تشغيل الخادم..."
        python3 mobile_api_server.py
        ;;
    2)
        echo "📱 تشغيل المحاكي..."
        python3 mobile_app_simulator.py
        ;;
    3)
        echo "🚀 تشغيل الخادم والمحاكي..."
        
        # تشغيل الخادم في الخلفية
        python3 mobile_api_server.py &
        SERVER_PID=$!
        
        # انتظار قليل لبدء الخادم
        sleep 3
        
        # تشغيل المحاكي
        python3 mobile_app_simulator.py
        
        # إيقاف الخادم عند الانتهاء
        kill $SERVER_PID 2>/dev/null
        ;;
    *)
        echo "❌ خيار غير صحيح"
        exit 1
        ;;
esac

echo ""
echo "✅ انتهى الاختبار"
