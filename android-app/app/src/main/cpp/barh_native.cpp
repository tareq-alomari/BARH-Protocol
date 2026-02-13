#include <jni.h>
#include <string>
#include <cmath>
#include <android/log.h>

#define LOG_TAG "BARH_Native"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

// BARH Protocol Version
const char* BARH_VERSION = "BARH v1.0 - Native Engine";

extern "C" {

JNIEXPORT jstring JNICALL
Java_com_barh_fixapp_MainActivity_getBARHVersion(JNIEnv *env, jobject thiz) {
    return env->NewStringUTF(BARH_VERSION);
}

JNIEXPORT jint JNICALL
Java_com_barh_fixapp_MainActivity_initializeBARH(JNIEnv *env, jobject thiz) {
    LOGI("Initializing BARH Native Engine");
    
    // Initialize BARH components
    // In a real implementation, this would load ML models, etc.
    
    LOGI("BARH Native Engine initialized successfully");
    return 0; // Success
}

JNIEXPORT jstring JNICALL
Java_com_barh_fixapp_MainActivity_processBARHDecision(JNIEnv *env, jobject thiz, 
                                                      jdoubleArray networkData) {
    
    // Get array elements
    jsize length = env->GetArrayLength(networkData);
    if (length != 8) {
        LOGE("Invalid network data length: %d", length);
        return env->NewStringUTF("no_action");
    }
    
    jdouble* data = env->GetDoubleArrayElements(networkData, nullptr);
    if (data == nullptr) {
        LOGE("Failed to get network data array");
        return env->NewStringUTF("no_action");
    }
    
    // Extract network metrics
    double latency = data[0];
    double bandwidth = data[1];
    double cpu = data[2];
    double memory = data[3];
    double packets = data[4];
    double quality = data[5];
    double errorRate = data[6];
    double responseTime = data[7];
    
    // BARH Decision Logic (optimized C++ version)
    std::string decision;
    
    if (errorRate > 0.05) {
        // High error rate - enable data compression
        decision = "data_compression";
        LOGI("BARH Decision: Data Compression (Error Rate: %.3f)", errorRate);
        
    } else if (latency > 150.0) {
        // High latency - optimize route
        decision = "route_optimization";
        LOGI("BARH Decision: Route Optimization (Latency: %.1f ms)", latency);
        
    } else if (quality > 0.9 && responseTime < 100.0) {
        // Excellent performance - predictive prefetch
        decision = "predictive_prefetch";
        LOGI("BARH Decision: Predictive Prefetch (Quality: %.1f%%, RT: %.1f ms)", 
             quality * 100, responseTime);
        
    } else {
        // Normal operation - no action needed
        decision = "no_action";
        LOGI("BARH Decision: No Action (Normal Operation)");
    }
    
    // Release array
    env->ReleaseDoubleArrayElements(networkData, data, JNI_ABORT);
    
    return env->NewStringUTF(decision.c_str());
}

// Additional native functions for performance optimization

JNIEXPORT jdouble JNICALL
Java_com_barh_fixapp_BARHEngine_calculateQualityScore(JNIEnv *env, jobject thiz,
                                                      jdoubleArray metrics) {
    jsize length = env->GetArrayLength(metrics);
    if (length < 3) return 0.0;
    
    jdouble* data = env->GetDoubleArrayElements(metrics, nullptr);
    if (data == nullptr) return 0.0;
    
    double latency = data[0];
    double bandwidth = data[1];
    double errorRate = data[2];
    
    // Calculate composite quality score
    double latencyScore = std::max(0.0, 1.0 - (latency - 20.0) / 180.0);
    double bandwidthScore = std::min(1.0, bandwidth / 50.0);
    double errorScore = std::max(0.0, 1.0 - errorRate * 10.0);
    
    double qualityScore = (latencyScore + bandwidthScore + errorScore) / 3.0;
    
    env->ReleaseDoubleArrayElements(metrics, data, JNI_ABORT);
    
    return qualityScore;
}

JNIEXPORT jboolean JNICALL
Java_com_barh_fixapp_BARHEngine_optimizeNetworkNative(JNIEnv *env, jobject thiz,
                                                      jstring action) {
    const char* actionStr = env->GetStringUTFChars(action, nullptr);
    
    bool result = false;
    
    if (strcmp(actionStr, "route_optimization") == 0) {
        // Implement native route optimization
        LOGI("Executing native route optimization");
        result = true;
        
    } else if (strcmp(actionStr, "data_compression") == 0) {
        // Implement native data compression
        LOGI("Executing native data compression");
        result = true;
        
    } else if (strcmp(actionStr, "predictive_prefetch") == 0) {
        // Implement native predictive prefetch
        LOGI("Executing native predictive prefetch");
        result = true;
        
    } else {
        LOGI("No native optimization needed");
        result = true;
    }
    
    env->ReleaseStringUTFChars(action, actionStr);
    
    return result;
}

} // extern "C"
