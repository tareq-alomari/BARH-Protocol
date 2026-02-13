#!/usr/bin/env python3
"""
تنظيف الملفات المتبقية في مشروع BARH
"""

import os
import shutil
from pathlib import Path

def cleanup_remaining_files():
    """تنظيف الملفات المتبقية"""
    
    base_dir = Path("/home/tareq/CS/paper/BARH-Project")
    
    # الملفات التي يجب نقلها إلى مجلدات محددة
    file_moves = {
        # التقارير والتوثيق
        "docs": [
            "SIMPLE_GUIDE.md", "MODEL_INTEGRATION_GUIDE.md", "ACADEMIC-OPTIMIZATION-GUIDE.md",
            "SUPERVISOR_REPORT.md", "SUCCESS_REPORT.md", "FINAL-SUCCESS-REPORT.md",
            "COMPREHENSIVE_PROJECT_REPORT.md", "EXECUTIVE_SUMMARY.md", "PROJECT_INDEX_COMPLETE.md",
            "PROJECT_PROGRESS_UPDATE.md", "NETWORK_TEST_REPORT.md", "NETWORK_TEST_GUIDE.md",
            "ANDROID_APP_TEST_REPORT.md", "OPTIMIZATION-SUCCESS-REPORT.md", "ULTRA-PRECISION-FINAL-REPORT.md"
        ],
        
        # السكريبتات والأدوات
        "scripts": [
            "mobile_app_simulator.py", "android_app_simulator.py", "network_integration_demo.py",
            "advanced_network_test.py", "real_network_test.py", "academic_optimization_barh.py",
            "improve_barh_training.py", "analyze_all_datasets.py", "create_mega_dataset.py",
            "explore_real_datasets.py", "simple_merge_datasets.py", "merge_datasets.py",
            "download_upc_dataset.py", "simple_dataset_generator.py", "realistic_dataset_generator.py",
            "realistic_network_dataset.py", "test_model_files.py"
        ],
        
        # ملفات البيانات والنتائج
        "data": [
            "dataset_generation.log"
        ],
        
        # الملفات للأرشفة
        "archive": [
            "presentation_slides.md", "progress-day1.md", "timeline.md",
            "COMPLETE-PROJECT-ROADMAP.md", "IMMEDIATE-ACTION-PLAN.md", "AI-TRAINING-PLAN.md",
            "DETAILED-EXPERIMENTAL-REPORT.md", "DATASET-STRATEGY.md", "UPC-DATASET-GUIDE.md",
            "COLAB-UPDATE-GUIDE.md", "DATASET-READY.md", "DATASET-SPECIFICATIONS.md",
            "COMPLETE-DATASET-ANALYSIS.md"
        ],
        
        # البيئات الافتراضية للحذف
        "temp": [
            "mobile_env", "barh_env"
        ]
    }
    
    print("🧹 بدء تنظيف الملفات المتبقية...")
    
    # نقل الملفات
    for target_dir, files in file_moves.items():
        target_path = base_dir / target_dir
        target_path.mkdir(exist_ok=True)
        
        for file_name in files:
            file_path = base_dir / file_name
            if file_path.exists():
                try:
                    if file_path.is_dir():
                        shutil.move(str(file_path), str(target_path / file_path.name))
                    else:
                        shutil.move(str(file_path), str(target_path / file_path.name))
                    print(f"✅ نقل {file_name} إلى {target_dir}/")
                except Exception as e:
                    print(f"❌ خطأ في نقل {file_name}: {e}")
    
    # إنشاء ملف .gitignore محدث
    create_gitignore(base_dir)
    
    # إنشاء requirements.txt محدث
    create_requirements(base_dir)
    
    print("\n🎉 تم تنظيف المشروع بنجاح!")

def create_gitignore(base_dir):
    """إنشاء ملف .gitignore محدث"""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
*_env/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
temp/
*.log
*.zip
*.tar.gz

# Models (too large for git)
models/*.h5
models/*.pkl

# Data files (too large for git)
data/*.csv
data/*.json
"""
    
    with open(base_dir / ".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("✅ تم إنشاء .gitignore محدث")

def create_requirements(base_dir):
    """إنشاء requirements.txt محدث"""
    
    requirements_content = """# Core dependencies
tensorflow>=2.10.0
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0

# API and web
flask>=2.0.0
requests>=2.25.0

# Data processing
matplotlib>=3.5.0
seaborn>=0.11.0

# Android integration
pyjnius>=1.4.0

# Development
pytest>=6.0.0
jupyter>=1.0.0
"""
    
    with open(base_dir / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    
    print("✅ تم إنشاء requirements.txt محدث")

if __name__ == "__main__":
    cleanup_remaining_files()
