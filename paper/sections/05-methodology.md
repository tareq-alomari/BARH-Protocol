# Section V: Experimental Methodology

## V. EXPERIMENTAL METHODOLOGY

### A. Test Environment Setup

The experimental evaluation of BARH was conducted in a controlled environment designed to simulate real-world network conditions while maintaining reproducibility.

**1. Hardware Configuration**
- **Test Devices**: Samsung Galaxy S21, Google Pixel 6, OnePlus 9
- **Network Infrastructure**: Controlled WiFi (802.11ac) and 4G LTE connections
- **Server Setup**: Dedicated Ubuntu 20.04 server for baseline measurements

**2. Software Environment**
- **Android Versions**: API levels 21-33 (Android 5.0 to 13)
- **Development Tools**: Android Studio 2022.1, NDK r25, Python 3.11
- **Monitoring Tools**: Wireshark, tcpdump, Android Profiler

### B. Performance Metrics

Four primary metrics were selected to evaluate BARH effectiveness:

**1. Latency (L)**: Round-trip time in milliseconds
**2. Packet Loss Rate (PLR)**: Percentage of lost packets
**3. Throughput (T)**: Data transfer rate in Mbps
**4. Correction Response Time (CRT)**: Time from detection to correction

### C. Experimental Scenarios

Four distinct scenarios were designed to evaluate BARH under different network conditions:

**Scenario 1: Stable Network Baseline**
- Purpose: Verify BARH does not degrade normal performance
- Conditions: Optimal WiFi connection, minimal interference
- Duration: 30 minutes continuous monitoring

**Scenario 2: Sudden Load Increase**
- Purpose: Test rapid deviation detection and correction
- Conditions: Artificial traffic injection causing congestion
- Duration: 5-minute stress periods with 2-minute recovery

**Scenario 3: Intermittent Packet Loss**
- Purpose: Evaluate packet loss mitigation effectiveness
- Conditions: Simulated 2-8% packet loss using network emulation
- Duration: 20 minutes with varying loss patterns

**Scenario 4: Long-term Stress Testing**
- Purpose: Assess system stability and resource consumption
- Conditions: Continuous high network load for extended periods
- Duration: 2 hours continuous operation

### D. Data Collection Methodology

**1. Baseline Measurements**
Each test scenario was first executed without BARH to establish baseline performance metrics.

**2. BARH-Enabled Testing**
Identical scenarios were repeated with BARH protocol active, using the same network conditions and measurement intervals.

**3. Statistical Validation**
- Minimum 30 test runs per scenario for statistical significance
- 95% confidence intervals calculated for all metrics
- Student's t-test applied for performance comparison validation

### E. Measurement Tools and Techniques

**1. Network Performance Monitoring**
```python
class NetworkMeasurement:
    def measure_latency(self, target_host):
        start_time = time.time()
        # ICMP ping implementation
        response = ping(target_host)
        return (time.time() - start_time) * 1000  # ms
    
    def measure_throughput(self, data_size, duration):
        bytes_transferred = self.transfer_data(data_size)
        return (bytes_transferred * 8) / (duration * 1000000)  # Mbps
```

**2. System Resource Monitoring**
- CPU usage via Android Profiler
- Memory consumption through Android Memory Profiler
- Battery drain measurement using Battery Historian

**3. Real-time Data Logging**
All measurements were logged with microsecond precision timestamps to enable detailed temporal analysis of correction effectiveness.

---
