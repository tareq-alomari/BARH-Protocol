"""
BARH Protocol - Data Structures
هياكل البيانات الأساسية لبروتوكول BARH
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import time

@dataclass
class NetworkMetrics:
    """مقاييس أداء الشبكة"""
    latency: float          # زمن الاستجابة (ms)
    packet_loss: float      # نسبة فقدان الحزم (%)
    throughput: float       # معدل النقل (Mbps)
    timestamp: float        # وقت القياس
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()

@dataclass
class Deviation:
    """انحراف في أداء الشبكة"""
    detected: bool
    severity: float
    metric_type: str        # 'latency', 'packet_loss', 'throughput'
    current_value: float
    baseline_value: float
    timestamp: float = 0
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()

class CorrectionType(Enum):
    """أنواع التصحيحات المتاحة"""
    BUFFER_OPTIMIZATION = "buffer_optimization"
    TIMEOUT_ADJUSTMENT = "timeout_adjustment"
    RETRANSMISSION_CONTROL = "retransmission_control"
    INTERFACE_SWITCH = "interface_switch"
    NO_ACTION = "no_action"

@dataclass
class CorrectionAction:
    """إجراء تصحيحي"""
    action_type: CorrectionType
    parameters: dict
    priority: float
    estimated_time: float   # Expected execution time (ms)
    resource_cost: float    # Resource usage (0-1)

@dataclass
class CorrectionResult:
    """نتيجة تطبيق التصحيح"""
    success: bool
    execution_time: float   # Actual execution time (ms)
    error_message: str = ""
    timestamp: float = 0
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()

@dataclass
class PerformanceReport:
    """تقرير أداء التصحيح"""
    before_metrics: NetworkMetrics
    after_metrics: NetworkMetrics
    correction_action: CorrectionAction
    correction_result: CorrectionResult
    improvement_percentage: dict  # {'latency': 0.5, 'packet_loss': 0.3, ...}
    overall_effectiveness: float
    
@dataclass
class Statistics:
    """إحصائيات للبيانات"""
    mean: float
    variance: float
    std_deviation: float
    min_value: float
    max_value: float
    sample_count: int
