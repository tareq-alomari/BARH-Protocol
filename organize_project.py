#!/usr/bin/env python3
"""
منظم مشروع BARH - تنظيم الملفات والمجلدات
"""

import os
import shutil
from pathlib import Path

def organize_barh_project():
    """تنظيم ملفات مشروع BARH"""
    
    base_dir = Path("/home/tareq/CS/paper/BARH-Project")
    
    # إنشاء البنية المنظمة
    directories = {
        "src": "الكود المصدري الأساسي",
        "tests": "ملفات الاختبار",
        "data": "مجموعات البيانات",
        "models": "النماذج المدربة", 
        "docs": "التوثيق",
        "scripts": "سكريبتات التشغيل",
        "results": "نتائج التجارب",
        "temp": "ملفات مؤقتة للحذف",
        "archive": "ملفات قديمة للأرشفة"
    }
    
    # إنشاء المجلدات
    for dir_name in directories:
        (base_dir / dir_name).mkdir(exist_ok=True)
    
    # قواعد التنظيم
    file_rules = {
        # الكود المصدري
        "src": [
            "simple_barh.py", "simple_api.py", "barh_api.py",
            "barh_model_loader.py", "mobile_api_server.py"
        ],
        
        # الاختبارات
        "tests": [
            "test_integration.py", "test_new_data.py", "test_android_app.py",
            "detailed_analysis.py", "quick_test.py", "test_mobile_integration.py"
        ],
        
        # البيانات
        "data": [
            "*.csv", "*.pkl", "*.json"
        ],
        
        # السكريبتات
        "scripts": [
            "*.sh", "download_model.py", "create_paper_figures.py",
            "clean_mega_dataset.py"
        ],
        
        # الملفات المؤقتة للحذف
        "temp": [
            "__pycache__", "*.pyc", "*_env", "*.zip", "*.tar.gz"
        ]
    }
    
    print("🚀 بدء تنظيم مشروع BARH...")
    
    # تطبيق قواعد التنظيم
    for target_dir, patterns in file_rules.items():
        target_path = base_dir / target_dir
        
        for pattern in patterns:
            if "*" in pattern:
                # البحث عن الملفات بالنمط
                for file_path in base_dir.glob(pattern):
                    if file_path.is_file() and file_path.parent == base_dir:
                        try:
                            shutil.move(str(file_path), str(target_path / file_path.name))
                            print(f"✅ نقل {file_path.name} إلى {target_dir}/")
                        except Exception as e:
                            print(f"❌ خطأ في نقل {file_path.name}: {e}")
            else:
                # نقل ملف محدد
                file_path = base_dir / pattern
                if file_path.exists():
                    try:
                        if file_path.is_dir():
                            shutil.move(str(file_path), str(target_path / file_path.name))
                        else:
                            shutil.move(str(file_path), str(target_path / file_path.name))
                        print(f"✅ نقل {pattern} إلى {target_dir}/")
                    except Exception as e:
                        print(f"❌ خطأ في نقل {pattern}: {e}")
    
    # إنشاء ملف README منظم
    create_organized_readme(base_dir)
    
    print("\n🎉 تم تنظيم المشروع بنجاح!")
    print("\n📁 البنية الجديدة:")
    for dir_name, desc in directories.items():
        count = len(list((base_dir / dir_name).iterdir()))
        print(f"  {dir_name}/ - {desc} ({count} عنصر)")

def create_organized_readme(base_dir):
    """إنشاء README منظم"""
    
    readme_content = """# BARH Protocol - مشروع منظم

## 📁 بنية المشروع المنظمة

```
BARH-Project/
├── src/                    # الكود المصدري الأساسي
├── tests/                  # ملفات الاختبار والتحليل
├── data/                   # مجموعات البيانات
├── models/                 # النماذج المدربة
├── docs/                   # التوثيق والأدلة
├── scripts/                # سكريبتات التشغيل
├── results/                # نتائج التجارب
├── research/               # البحث الأكاديمي
├── paper/                  # الورقة البحثية
├── android-app/            # تطبيق Android
└── README.md              # هذا الملف
```

## 🚀 البدء السريع

```bash
# تشغيل النموذج البسيط
python src/simple_barh.py

# تشغيل الاختبارات
python tests/test_integration.py

# تشغيل الخادم
python src/mobile_api_server.py
```

## 📊 الملفات الرئيسية

- `src/simple_barh.py` - النموذج الأساسي
- `tests/test_integration.py` - اختبار التكامل
- `models/best_model.h5` - النموذج المدرب
- `docs/implementation-strategy.md` - دليل التنفيذ

## 🧹 تنظيف المشروع

تم نقل الملفات القديمة والمؤقتة إلى مجلد `temp/` للمراجعة قبل الحذف.
"""
    
    with open(base_dir / "README_ORGANIZED.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    organize_barh_project()
