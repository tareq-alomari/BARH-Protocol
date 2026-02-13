"""
BARH Protocol - Advanced Configuration for Maximum Accuracy
تكوين متقدم لبروتوكول BARH لتحقيق أقصى دقة
"""

# Enhanced Network Monitoring Settings
MONITOR_INTERVAL = 0.05         # 50ms monitoring (more frequent)
METRICS_BUFFER_SIZE = 2000      # Larger buffer for better statistics
BASELINE_WINDOW_SIZE = 200      # Larger baseline window

# Advanced Deviation Detection Settings
SENSITIVITY_FACTOR = 1.5        # More sensitive detection
MIN_SAMPLES_FOR_BASELINE = 20   # More samples for accurate baseline
ADAPTIVE_THRESHOLD_ENABLED = True

# Enhanced Correction Settings
MAX_CORRECTION_TIME = 0.003     # 3ms maximum (more aggressive)
CORRECTION_RETRY_LIMIT = 5      # More retries
CORRECTION_COOLDOWN = 0.5       # Shorter cooldown for frequent corrections
PARALLEL_CORRECTIONS_ENABLED = True

# Advanced Performance Targets (more aggressive)
TARGET_LATENCY_IMPROVEMENT = 0.75     # 75% improvement target
TARGET_PACKET_LOSS_REDUCTION = 0.85   # 85% reduction target  
TARGET_THROUGHPUT_INCREASE = 0.25     # 25% increase target

# Machine Learning Enhancement
ML_PREDICTION_ENABLED = True
ML_LEARNING_RATE = 0.1
ML_ADAPTATION_WINDOW = 100

# Advanced Simulation Settings
SIMULATION_DURATION = 180       # 3 minutes for better results
NETWORK_INSTABILITY_PROBABILITY = 0.2  # 20% chance for more testing
CORRECTION_EFFECTIVENESS_MULTIPLIER = 1.8  # Stronger corrections

# Multi-layer Correction Strategy
CORRECTION_LAYERS = {
    "immediate": {"timeout": 0.001, "effectiveness": 1.2},
    "adaptive": {"timeout": 0.002, "effectiveness": 1.5}, 
    "aggressive": {"timeout": 0.003, "effectiveness": 2.0}
}

# Advanced Metrics Tracking
TRACK_MICRO_IMPROVEMENTS = True
STATISTICAL_CONFIDENCE_LEVEL = 0.99  # 99% confidence
PERFORMANCE_SMOOTHING_FACTOR = 0.3
