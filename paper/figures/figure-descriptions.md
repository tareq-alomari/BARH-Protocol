# Figure Descriptions for IEEE Paper

## Fig. 1. BARH Protocol Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                    │
├─────────────────────────────────────────────────────────┤
│                    BARH Protocol                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Network   │  │ Deviation   │  │ Correction  │     │
│  │   Monitor   │→ │  Detector   │→ │   Engine    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         ↑                                    ↓          │
│  ┌─────────────┐                    ┌─────────────┐     │
│  │Performance  │←───────────────────│  Action     │     │
│  │ Evaluator   │                    │ Executor    │     │
│  └─────────────┘                    └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                   Network Layer                         │
└─────────────────────────────────────────────────────────┘
```

**Caption**: BARH Protocol Architecture showing the four main components: Network Monitor for continuous performance tracking, Deviation Detector for anomaly identification, Correction Engine for action selection, and Performance Evaluator for effectiveness assessment.

---

## Fig. 2. Protocol State Machine

```
     ┌─────────┐
     │  IDLE   │
     └────┬────┘
          │ Network Event
          ▼
   ┌─────────────┐
   │ DETECTING   │
   └──────┬──────┘
          │ Deviation Found
          ▼
   ┌─────────────┐
   │ CORRECTING  │
   └──────┬──────┘
          │ Action Applied
          ▼
   ┌─────────────┐
   │ EVALUATING  │
   └──────┬──────┘
          │ Assessment Complete
          ▼
   ┌─────────────┐
   │  ADAPTING   │
   └──────┬──────┘
          │ Learning Complete
          └──────→ Back to IDLE
```

**Caption**: BARH Protocol State Machine illustrating the five operational states and transition conditions for real-time network correction.

---

## Fig. 3. Fix App System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Android Application Layer                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │     UI      │  │ Config Mgr  │  │   Logger    │     │
│  │ Components  │  │             │  │             │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                    JNI Interface                        │
├─────────────────────────────────────────────────────────┤
│              Native Layer (C/C++ NDK)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │    BARH     │  │   Network   │  │   Memory    │     │
│  │   Engine    │  │ Interface   │  │ Manager     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│              Research Layer (Python)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Algorithm   │  │ Simulation  │  │ Data        │     │
│  │ Validation  │  │ Framework   │  │ Analysis    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

**Caption**: Fix App multi-layered system architecture showing the integration between Android Application Layer, Native Processing Layer via JNI, and Python Research Layer.

---

## Fig. 4. Performance Comparison Results

```
Performance Metrics Comparison

Latency (ms)
    Baseline: ████████████ 12.3ms
    BARH:     ████ 4.1ms (-66.7%)

Packet Loss (%)
    Baseline: ███ 3.5%
    BARH:     █ 0.8% (-77.1%)

Throughput (Mbps)
    Baseline: █████████ 45.2 Mbps
    BARH:     ██████████ 52.1 Mbps (+15.3%)

Correction Time
    Detection: ██ 1.2ms
    Application: ███ 2.8ms
    Total: █████ 4.0ms
```

**Caption**: Performance comparison showing significant improvements in latency, packet loss, and throughput when BARH protocol is active, with sub-5ms correction response time.

---

## Additional Technical Diagrams

### Algorithm Flowchart - Deviation Detection
```
Start → Monitor Network → Calculate Metrics → 
Check Thresholds → [Deviation?] → Yes: Calculate Severity → 
Trigger Correction → No: Continue Monitoring → Loop
```

### Data Flow Diagram
```
Network Interface → Raw Data → Metrics Extraction → 
Statistical Analysis → Deviation Detection → 
Correction Selection → Action Execution → 
Performance Feedback → Loop
```

---

## Figure Implementation Notes

**For IEEE Submission:**
1. Convert ASCII diagrams to professional vector graphics (SVG/EPS)
2. Use IEEE-standard fonts and styling
3. Ensure high resolution (300 DPI minimum)
4. Include proper figure numbering and captions
5. Reference figures in text using "Fig. X" format

**Recommended Tools:**
- Draw.io (free, professional diagrams)
- Visio (Microsoft)
- Lucidchart (online)
- TikZ (LaTeX-based)

**Color Scheme:**
- Use IEEE-compliant colors
- Ensure readability in grayscale
- Maintain consistency across all figures
