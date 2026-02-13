package com.barh.fixapp;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Button;
import android.widget.ProgressBar;
import android.view.View;
import android.os.Handler;
import android.os.Looper;

public class MainActivity extends Activity {
    
    // UI Components
    private TextView statusText;
    private TextView latencyText;
    private TextView actionText;
    private Button startButton;
    private Button stopButton;
    private ProgressBar progressBar;
    
    // BARH Components
    private NetworkMonitor networkMonitor;
    private BARHEngine barhEngine;
    private Handler uiHandler;
    
    // Native methods
    static {
        System.loadLibrary("barh_native");
    }
    
    public native String getBARHVersion();
    public native int initializeBARH();
    public native String processBARHDecision(double[] networkData);
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        initializeUI();
        initializeBARH();
        setupEventHandlers();
    }
    
    private void initializeUI() {
        statusText = findViewById(R.id.status_text);
        latencyText = findViewById(R.id.latency_text);
        actionText = findViewById(R.id.action_text);
        startButton = findViewById(R.id.start_button);
        stopButton = findViewById(R.id.stop_button);
        progressBar = findViewById(R.id.progress_bar);
        
        uiHandler = new Handler(Looper.getMainLooper());
        
        // Initial state
        statusText.setText("BARH Fix App Ready");
        actionText.setText("No Action");
        stopButton.setEnabled(false);
    }
    
    private void initializeBARH() {
        networkMonitor = new NetworkMonitor(this);
        barhEngine = new BARHEngine();
        
        // Initialize native BARH
        int result = initializeBARH();
        if (result == 0) {
            statusText.setText("BARH Engine Initialized - " + getBARHVersion());
        } else {
            statusText.setText("BARH Initialization Failed");
        }
    }
    
    private void setupEventHandlers() {
        startButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startMonitoring();
            }
        });
        
        stopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stopMonitoring();
            }
        });
    }
    
    private void startMonitoring() {
        startButton.setEnabled(false);
        stopButton.setEnabled(true);
        progressBar.setVisibility(View.VISIBLE);
        statusText.setText("Monitoring Network...");
        
        // Start network monitoring
        networkMonitor.startMonitoring(new NetworkMonitor.NetworkCallback() {
            @Override
            public void onNetworkDataReceived(double[] networkData) {
                // Process with BARH engine
                String decision = processBARHDecision(networkData);
                
                // Update UI on main thread
                uiHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        updateNetworkInfo(networkData, decision);
                    }
                });
            }
        });
    }
    
    private void stopMonitoring() {
        startButton.setEnabled(true);
        stopButton.setEnabled(false);
        progressBar.setVisibility(View.GONE);
        statusText.setText("Monitoring Stopped");
        
        networkMonitor.stopMonitoring();
    }
    
    private void updateNetworkInfo(double[] networkData, String decision) {
        // Update latency
        latencyText.setText(String.format("Latency: %.1f ms", networkData[0]));
        
        // Update action
        actionText.setText("Action: " + decision);
        
        // Update status with confidence
        if (networkData.length > 7) {
            statusText.setText(String.format("BARH Active - Quality: %.1f%%", 
                                            networkData[5] * 100));
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (networkMonitor != null) {
            networkMonitor.stopMonitoring();
        }
    }
}
