# BARH Protocol - Configuration
# تكوين بروتوكول BARH

# Network Monitoring Settings
MONITOR_INTERVAL = 0.1          # 100ms monitoring interval
METRICS_BUFFER_SIZE = 1000      # Keep last 1000 measurements
BASELINE_WINDOW_SIZE = 100      # Use last 100 measurements for baseline

# Deviation Detection Settings
SENSITIVITY_FACTOR = 2.0        # 2 standard deviations threshold
MIN_SAMPLES_FOR_BASELINE = 10   # Minimum samples before detection

# Correction Settings
MAX_CORRECTION_TIME = 0.005     # 5ms maximum correction time
CORRECTION_RETRY_LIMIT = 3      # Maximum retry attempts
CORRECTION_COOLDOWN = 1.0       # 1 second cooldown between corrections

# Performance Targets (from research paper)
TARGET_LATENCY_IMPROVEMENT = 0.667    # 66.7% improvement
TARGET_PACKET_LOSS_REDUCTION = 0.771  # 77.1% reduction  
TARGET_THROUGHPUT_INCREASE = 0.153    # 15.3% increase

# Simulation Settings
SIMULATION_DURATION = 300       # 5 minutes simulation
NETWORK_INSTABILITY_PROBABILITY = 0.1  # 10% chance of instability per interval
