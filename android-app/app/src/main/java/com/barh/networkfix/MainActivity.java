package com.barh.networkfix;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;
import android.widget.Button;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.content.Context;
import java.io.IOException;
import okhttp3.*;
import org.json.JSONObject;

public class MainActivity extends Activity {
    private TextView statusText;
    private TextView latencyText;
    private TextView recommendationText;
    private Button testButton;
    private Handler handler = new Handler();
    private OkHttpClient client = new OkHttpClient();
    
    // عنوان خادم BARH (غير هذا لعنوان الخادم الفعلي)
    private static final String BARH_SERVER = "http://192.168.0.237:5000";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        statusText = findViewById(R.id.statusText);
        latencyText = findViewById(R.id.latencyText);
        recommendationText = findViewById(R.id.recommendationText);
        testButton = findViewById(R.id.testButton);
        
        testButton.setOnClickListener(v -> testBarhConnection());
        
        // اختبار تلقائي كل 10 ثوان
        startAutoTest();
    }
    
    private void testBarhConnection() {
        statusText.setText("🔍 اختبار الاتصال...");
        
        Request request = new Request.Builder()
            .url(BARH_SERVER + "/api/barh/test")
            .build();
        
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                handler.post(() -> {
                    statusText.setText("❌ فشل الاتصال: " + e.getMessage());
                });
            }
            
            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        String responseBody = response.body().string();
                        JSONObject json = new JSONObject(responseBody);
                        
                        handler.post(() -> {
                            try {
                                statusText.setText("✅ متصل بـ BARH");
                                latencyText.setText("🏓 التأخير: " + 
                                    json.getDouble("current_latency") + "ms");
                                recommendationText.setText("🎯 التوصية: " + 
                                    getArabicAction(json.getString("recommendation")));
                            } catch (Exception e) {
                                statusText.setText("❌ خطأ في البيانات");
                            }
                        });
                    } catch (Exception e) {
                        handler.post(() -> statusText.setText("❌ خطأ في التحليل"));
                    }
                } else {
                    handler.post(() -> statusText.setText("❌ خطأ الخادم: " + response.code()));
                }
            }
        });
    }
    
    private String getArabicAction(String action) {
        switch (action) {
            case "no_action": return "لا حاجة لإجراء";
            case "route_optimization": return "تحسين المسار";
            case "data_compression": return "ضغط البيانات";
            case "predictive_prefetch": return "جلب تنبؤي";
            default: return action;
        }
    }
    
    private void startAutoTest() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                testBarhConnection();
                handler.postDelayed(this, 10000); // كل 10 ثوان
            }
        }, 1000);
    }
    
    private boolean isNetworkAvailable() {
        ConnectivityManager cm = (ConnectivityManager) 
            getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = cm.getActiveNetworkInfo();
        return networkInfo != null && networkInfo.isConnected();
    }
}
