package com.barh.fixapp;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.TrafficStats;
import android.os.Handler;
import android.os.HandlerThread;
import java.util.Random;

public class NetworkMonitor {
    
    public interface NetworkCallback {
        void onNetworkDataReceived(double[] networkData);
    }
    
    private Context context;
    private ConnectivityManager connectivityManager;
    private HandlerThread monitorThread;
    private Handler monitorHandler;
    private NetworkCallback callback;
    private boolean isMonitoring = false;
    
    // Monitoring interval (2 seconds)
    private static final int MONITOR_INTERVAL = 2000;
    
    public NetworkMonitor(Context context) {
        this.context = context;
        this.connectivityManager = (ConnectivityManager) 
            context.getSystemService(Context.CONNECTIVITY_SERVICE);
    }
    
    public void startMonitoring(NetworkCallback callback) {
        this.callback = callback;
        this.isMonitoring = true;
        
        // Create background thread for monitoring
        monitorThread = new HandlerThread("NetworkMonitor");
        monitorThread.start();
        monitorHandler = new Handler(monitorThread.getLooper());
        
        // Start monitoring loop
        monitorHandler.post(monitoringRunnable);
    }
    
    public void stopMonitoring() {
        isMonitoring = false;
        if (monitorHandler != null) {
            monitorHandler.removeCallbacks(monitoringRunnable);
        }
        if (monitorThread != null) {
            monitorThread.quitSafely();
        }
    }
    
    private Runnable monitoringRunnable = new Runnable() {
        @Override
        public void run() {
            if (isMonitoring) {
                double[] networkData = collectNetworkData();
                if (callback != null) {
                    callback.onNetworkDataReceived(networkData);
                }
                
                // Schedule next monitoring cycle
                monitorHandler.postDelayed(this, MONITOR_INTERVAL);
            }
        }
    };
    
    private double[] collectNetworkData() {
        double[] data = new double[8];
        
        try {
            // Get network info
            NetworkInfo activeNetwork = connectivityManager.getActiveNetworkInfo();
            boolean isConnected = activeNetwork != null && activeNetwork.isConnected();
            
            if (isConnected) {
                // Simulate realistic network metrics
                // In real implementation, use actual network measurement APIs
                
                // Latency (ms) - simulate ping measurement
                data[0] = simulateLatency();
                
                // Bandwidth (Mbps) - simulate speed test
                data[1] = simulateBandwidth();
                
                // CPU usage (0-1) - simulate system load
                data[2] = simulateCPUUsage();
                
                // Memory (MB) - get actual available memory
                data[3] = getAvailableMemory();
                
                // Packets per second - simulate traffic
                data[4] = simulatePacketsPerSecond();
                
                // Quality (0-1) - calculate from other metrics
                data[5] = calculateQuality(data[0], data[1], data[6]);
                
                // Error rate (0-1) - simulate packet loss
                data[6] = simulateErrorRate();
                
                // Response time (ms) - simulate HTTP response
                data[7] = simulateResponseTime();
                
            } else {
                // No connection - set poor values
                data[0] = 1000; // High latency
                data[1] = 0;    // No bandwidth
                data[2] = 0.9;  // High CPU
                data[3] = 256;  // Low memory
                data[4] = 0;    // No packets
                data[5] = 0.1;  // Poor quality
                data[6] = 0.5;  // High error rate
                data[7] = 2000; // High response time
            }
            
        } catch (Exception e) {
            // Fallback values on error
            data = new double[]{100, 50, 0.5, 1024, 500, 0.8, 0.02, 120};
        }
        
        return data;
    }
    
    private double simulateLatency() {
        // Simulate realistic latency variations (20-200ms)
        Random random = new Random();
        return 20 + random.nextDouble() * 180;
    }
    
    private double simulateBandwidth() {
        // Simulate bandwidth variations (1-100 Mbps)
        Random random = new Random();
        return 1 + random.nextDouble() * 99;
    }
    
    private double simulateCPUUsage() {
        // Simulate CPU usage (0.2-0.9)
        Random random = new Random();
        return 0.2 + random.nextDouble() * 0.7;
    }
    
    private double getAvailableMemory() {
        // Get actual available memory in MB
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxHeapSize() / (1024 * 1024);
        long usedMemory = (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
        return maxMemory - usedMemory;
    }
    
    private double simulatePacketsPerSecond() {
        // Simulate packet rate (100-2000 pps)
        Random random = new Random();
        return 100 + random.nextDouble() * 1900;
    }
    
    private double calculateQuality(double latency, double bandwidth, double errorRate) {
        // Calculate quality score based on metrics
        double latencyScore = Math.max(0, 1 - (latency - 20) / 180);
        double bandwidthScore = Math.min(1, bandwidth / 50);
        double errorScore = Math.max(0, 1 - errorRate * 10);
        
        return (latencyScore + bandwidthScore + errorScore) / 3;
    }
    
    private double simulateErrorRate() {
        // Simulate error rate (0.001-0.1)
        Random random = new Random();
        return 0.001 + random.nextDouble() * 0.099;
    }
    
    private double simulateResponseTime() {
        // Simulate HTTP response time (10-300ms)
        Random random = new Random();
        return 10 + random.nextDouble() * 290;
    }
}
