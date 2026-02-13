"""
إنشاء الرسوم البيانية للورقة البحثية
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# إعداد النمط
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_figure1_protocol_architecture():
    """الرسم 1: معمارية بروتوكول BARH"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # مكونات النظام
    components = ['Network Monitor', 'BARH Engine', 'Decision Module', 'Action Executor']
    y_positions = [3, 2, 1, 0]
    
    # رسم المكونات
    for i, (comp, y) in enumerate(zip(components, y_positions)):
        rect = plt.Rectangle((1, y), 8, 0.8, 
                           facecolor=f'C{i}', alpha=0.7, 
                           edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(5, y+0.4, comp, ha='center', va='center', 
                fontsize=12, fontweight='bold')
    
    # الأسهم
    for i in range(len(y_positions)-1):
        ax.arrow(5, y_positions[i]-0.1, 0, -0.7, 
                head_width=0.3, head_length=0.1, 
                fc='red', ec='red', linewidth=2)
    
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 4)
    ax.set_title('BARH Protocol Architecture', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('paper/figures/figure1_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_figure2_performance_comparison():
    """الرسم 2: مقارنة الأداء"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # البيانات
    methods = ['Traditional', 'BARH Simple', 'BARH Advanced']
    accuracy = [4.09, 85, 99.10]
    speed = [50, 1250000, 1000000]  # predictions per second
    
    # الرسم الأول: الدقة
    bars1 = ax1.bar(methods, accuracy, color=['red', 'orange', 'green'], alpha=0.7)
    ax1.set_ylabel('Accuracy (%)', fontsize=12)
    ax1.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 105)
    
    # إضافة القيم على الأعمدة
    for bar, acc in zip(bars1, accuracy):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{acc}%', ha='center', va='bottom', fontweight='bold')
    
    # الرسم الثاني: السرعة
    bars2 = ax2.bar(methods, [s/1000 for s in speed], color=['red', 'orange', 'green'], alpha=0.7)
    ax2.set_ylabel('Speed (K predictions/sec)', fontsize=12)
    ax2.set_title('Processing Speed Comparison', fontsize=14, fontweight='bold')
    ax2.set_yscale('log')
    
    # إضافة القيم على الأعمدة
    for bar, spd in zip(bars2, speed):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.1,
                f'{spd/1000:.0f}K', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('paper/figures/figure2_performance.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_figure3_decision_flow():
    """الرسم 3: مخطط تدفق القرارات"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    
    # العقد والقرارات
    nodes = [
        ('Network Data Input', 0, 10, 'lightblue'),
        ('Error Rate > 5%?', 0, 8, 'yellow'),
        ('Data Compression', -3, 6, 'orange'),
        ('Latency > 150ms?', 0, 6, 'yellow'),
        ('Route Optimization', 3, 4, 'red'),
        ('Quality > 90% & RT < 100ms?', 0, 4, 'yellow'),
        ('Predictive Prefetch', -3, 2, 'green'),
        ('No Action', 3, 2, 'gray'),
        ('Execute Action', 0, 0, 'purple')
    ]
    
    # رسم العقد
    for name, x, y, color in nodes:
        if '?' in name:  # قرار
            rect = plt.Polygon([(x-1.5, y), (x, y+0.5), (x+1.5, y), (x, y-0.5)], 
                             facecolor=color, edgecolor='black', linewidth=2)
        else:  # عملية
            rect = plt.Rectangle((x-1.5, y-0.3), 3, 0.6, 
                               facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # الأسهم والتسميات
    arrows = [
        (0, 10, 0, 8, ''),
        (0, 8, -3, 6, 'Yes'),
        (0, 8, 0, 6, 'No'),
        (0, 6, 3, 4, 'Yes'),
        (0, 6, 0, 4, 'No'),
        (0, 4, -3, 2, 'Yes'),
        (0, 4, 3, 2, 'No'),
        (-3, 6, 0, 0, ''),
        (3, 4, 0, 0, ''),
        (-3, 2, 0, 0, ''),
        (3, 2, 0, 0, '')
    ]
    
    for x1, y1, x2, y2, label in arrows:
        if x1 == x2:  # سهم عمودي
            ax.arrow(x1, y1-0.3, 0, y2-y1+0.6, head_width=0.2, head_length=0.2,
                    fc='black', ec='black')
        else:  # سهم مائل
            dx, dy = x2-x1, y2-y1
            length = np.sqrt(dx**2 + dy**2)
            ax.arrow(x1, y1-0.3, dx*0.8, dy*0.8, head_width=0.2, head_length=0.2,
                    fc='black', ec='black')
        
        if label:
            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            ax.text(mid_x+0.3, mid_y, label, fontsize=8, fontweight='bold', color='red')
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-1, 11)
    ax.set_title('BARH Decision Flow Chart', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('paper/figures/figure3_decision_flow.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_figure4_results_timeline():
    """الرسم 4: تطور النتائج عبر الزمن"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # البيانات الزمنية
    phases = ['Initial\nBaseline', 'Data\nBalancing', 'LSTM\nIntegration', 
              'Advanced\nOptimization', 'Final\nSystem']
    accuracy = [4.09, 45, 78, 95, 99.10]
    dates = ['Jan 26', 'Jan 27', 'Jan 28', 'Jan 28', 'Jan 29']
    
    # رسم الخط
    line = ax.plot(phases, accuracy, 'o-', linewidth=3, markersize=8, color='blue')
    
    # تلوين المناطق
    ax.fill_between(phases, accuracy, alpha=0.3, color='lightblue')
    
    # إضافة القيم
    for i, (phase, acc, date) in enumerate(zip(phases, accuracy, dates)):
        ax.text(i, acc + 2, f'{acc}%', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')
        ax.text(i, -5, date, ha='center', va='top', 
                fontsize=9, style='italic')
    
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('BARH Development Progress Timeline', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    
    # خط الهدف
    ax.axhline(y=90, color='red', linestyle='--', alpha=0.7, label='Target (90%)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('paper/figures/figure4_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("🎨 إنشاء الرسوم البيانية للورقة البحثية...")
    
    # إنشاء مجلد الرسوم
    import os
    os.makedirs('paper/figures', exist_ok=True)
    
    # إنشاء الرسوم
    create_figure1_protocol_architecture()
    print("✅ تم إنشاء الرسم 1: معمارية البروتوكول")
    
    create_figure2_performance_comparison()
    print("✅ تم إنشاء الرسم 2: مقارنة الأداء")
    
    create_figure3_decision_flow()
    print("✅ تم إنشاء الرسم 3: مخطط تدفق القرارات")
    
    create_figure4_results_timeline()
    print("✅ تم إنشاء الرسم 4: تطور النتائج")
    
    print("\n🎯 تم إنشاء جميع الرسوم البيانية بنجاح!")
    print("📁 الملفات محفوظة في: paper/figures/")
