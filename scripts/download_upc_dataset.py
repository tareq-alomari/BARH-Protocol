#!/usr/bin/env python3
import requests
import os
from tqdm import tqdm

def download_file(url, filename):
    """تحميل ملف مع شريط التقدم"""
    print(f"🔄 تحميل {filename}...")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                pbar.update(len(chunk))
    
    print(f"✅ تم تحميل {filename}")

# URLs للتحميل
datasets = {
    "gnnet-ch23-dataset-mb.zip": "https://bnn.upc.edu/download/gnnet-ch23-dataset-mb/",
    "gnnet-ch23-dataset-cbr-mb.zip": "https://bnn.upc.edu/download/gnnet-ch23-dataset-cbr-mb/"
}

print("🚀 بدء تحميل UPC Network Datasets...")

for filename, url in datasets.items():
    if not os.path.exists(filename):
        try:
            download_file(url, filename)
        except Exception as e:
            print(f"❌ خطأ في تحميل {filename}: {e}")
    else:
        print(f"✅ {filename} موجود مسبقاً")

print("🎉 تم الانتهاء من التحميل!")
