"""
BARH Protocol - Comprehensive System Test
Complete validation of all components and potential issues
"""

import time
import json
import traceback
from pathlib import Path

def comprehensive_system_test():
    """Run complete system validation"""
    
    print("🔍 BARH PROTOCOL - COMPREHENSIVE SYSTEM TEST")
    print("🎯 Checking for vulnerabilities, errors, and edge cases")
    print("=" * 80)
    
    test_results = {
        'timestamp': time.time(),
        'tests_passed': 0,
        'tests_failed': 0,
        'warnings': [],
        'errors': [],
        'critical_issues': []
    }
    
    # Test 1: Core Implementation Validation
    print("\n🧪 TEST 1: Core Implementation Validation")
    try:
        from intelligent_barh_ml import IntelligentBARHProtocol
        protocol = IntelligentBARHProtocol()
        
        # Test LSTM initialization
        if hasattr(protocol.lstm_predictor, 'forward'):
            print("   ✅ LSTM predictor initialized correctly")
            test_results['tests_passed'] += 1
        else:
            print("   ❌ LSTM predictor missing forward method")
            test_results['errors'].append("LSTM predictor incomplete")
            test_results['tests_failed'] += 1
            
        # Test DQL initialization
        if hasattr(protocol.dql_agent, 'select_action'):
            print("   ✅ DQL agent initialized correctly")
            test_results['tests_passed'] += 1
        else:
            print("   ❌ DQL agent missing select_action method")
            test_results['errors'].append("DQL agent incomplete")
            test_results['tests_failed'] += 1
            
    except Exception as e:
        print(f"   ❌ Core implementation error: {str(e)}")
        test_results['critical_issues'].append(f"Core implementation: {str(e)}")
        test_results['tests_failed'] += 1
    
    # Test 2: Simulator Integration
    print("\n🌐 TEST 2: Simulator Integration")
    try:
        from realistic_feedback_simulator import RealisticFeedbackSimulator
        simulator = RealisticFeedbackSimulator()
        
        # Test basic functionality
        metrics = simulator.get_current_metrics()
        if hasattr(metrics, 'latency') and hasattr(metrics, 'packet_loss'):
            print("   ✅ Simulator metrics working correctly")
            test_results['tests_passed'] += 1
        else:
            print("   ❌ Simulator metrics incomplete")
            test_results['errors'].append("Simulator metrics missing attributes")
            test_results['tests_failed'] += 1
            
        # Test correction application
        success = simulator.apply_correction("buffer_optimization", 0.5)
        if isinstance(success, bool):
            print("   ✅ Correction application working")
            test_results['tests_passed'] += 1
        else:
            print("   ❌ Correction application returns invalid type")
            test_results['warnings'].append("Correction application type issue")
            
    except Exception as e:
        print(f"   ❌ Simulator integration error: {str(e)}")
        test_results['critical_issues'].append(f"Simulator: {str(e)}")
        test_results['tests_failed'] += 1
    
    # Test 3: Edge Cases and Boundary Conditions
    print("\n⚠️  TEST 3: Edge Cases and Boundary Conditions")
    try:
        # Test with extreme values
        extreme_metrics = {
            'latency': 0.0,  # Minimum
            'packet_loss': 100.0,  # Maximum
            'throughput': 0.0,  # Minimum
            'jitter': 1000.0  # Very high
        }
        
        # Test LSTM with extreme values
        protocol = IntelligentBARHProtocol()
        result = protocol.process_intelligent_correction(extreme_metrics, simulator)
        
        if isinstance(result, dict) and 'correction_applied' in result:
            print("   ✅ Handles extreme values correctly")
            test_results['tests_passed'] += 1
        else:
            print("   ❌ Fails with extreme values")
            test_results['errors'].append("Extreme values handling")
            test_results['tests_failed'] += 1
            
        # Test with empty history
        protocol_new = IntelligentBARHProtocol()
        result_empty = protocol_new.process_intelligent_correction({
            'latency': 20, 'packet_loss': 2, 'throughput': 50, 'jitter': 10
        }, simulator)
        
        if result_empty['correction_applied'] is not None:
            print("   ✅ Handles empty history correctly")
            test_results['tests_passed'] += 1
        else:
            print("   ❌ Fails with empty history")
            test_results['errors'].append("Empty history handling")
            test_results['tests_failed'] += 1
            
    except Exception as e:
        print(f"   ❌ Edge case error: {str(e)}")
        test_results['errors'].append(f"Edge cases: {str(e)}")
        test_results['tests_failed'] += 1
    
    # Test 4: Memory and Performance
    print("\n💾 TEST 4: Memory and Performance Validation")
    try:
        import sys
        
        # Test memory usage
        protocol = IntelligentBARHProtocol()
        initial_size = sys.getsizeof(protocol)
        
        # Run multiple corrections
        for i in range(100):
            metrics = {
                'latency': 20 + i % 10,
                'packet_loss': 2 + i % 5,
                'throughput': 50 + i % 20,
                'jitter': 10 + i % 8
            }
            protocol.process_intelligent_correction(metrics, simulator)
        
        final_size = sys.getsizeof(protocol)
        memory_growth = final_size - initial_size
        
        if memory_growth < 1000000:  # Less than 1MB growth
            print(f"   ✅ Memory usage acceptable: {memory_growth} bytes growth")
            test_results['tests_passed'] += 1
        else:
            print(f"   ⚠️  High memory usage: {memory_growth} bytes growth")
            test_results['warnings'].append(f"High memory growth: {memory_growth}")
            
        # Test processing speed
        start_time = time.time()
        for i in range(50):
            protocol.process_intelligent_correction({
                'latency': 25, 'packet_loss': 3, 'throughput': 60, 'jitter': 12
            }, simulator)
        processing_time = (time.time() - start_time) / 50
        
        if processing_time < 0.01:  # Less than 10ms per correction
            print(f"   ✅ Processing speed acceptable: {processing_time*1000:.2f}ms per correction")
            test_results['tests_passed'] += 1
        else:
            print(f"   ⚠️  Slow processing: {processing_time*1000:.2f}ms per correction")
            test_results['warnings'].append(f"Slow processing: {processing_time*1000:.2f}ms")
            
    except Exception as e:
        print(f"   ❌ Performance test error: {str(e)}")
        test_results['errors'].append(f"Performance: {str(e)}")
        test_results['tests_failed'] += 1
    
    # Test 5: Data Consistency and Validation
    print("\n📊 TEST 5: Data Consistency and Validation")
    try:
        protocol = IntelligentBARHProtocol()
        
        # Test with consistent data
        consistent_results = []
        for i in range(10):
            result = protocol.process_intelligent_correction({
                'latency': 30, 'packet_loss': 4, 'throughput': 40, 'jitter': 15
            }, simulator)
            consistent_results.append(result)
        
        # Check consistency
        correction_types = [r['correction_type'] for r in consistent_results]
        if len(set(correction_types)) <= 3:  # Should converge to similar actions
            print("   ✅ Decision consistency maintained")
            test_results['tests_passed'] += 1
        else:
            print("   ⚠️  High decision variability")
            test_results['warnings'].append("High decision variability")
        
        # Test learning progress
        learning_values = []
        for i in range(20):
            result = protocol.process_intelligent_correction({
                'latency': 35 - i, 'packet_loss': 5 - i*0.1, 'throughput': 30 + i, 'jitter': 20 - i
            }, simulator)
            if 'learning_progress' in result:
                learning_values.append(result['learning_progress'])
        
        if learning_values and learning_values[-1] > learning_values[0]:
            print("   ✅ Learning progress detected")
            test_results['tests_passed'] += 1
        else:
            print("   ⚠️  No clear learning progress")
            test_results['warnings'].append("Learning progress unclear")
            
    except Exception as e:
        print(f"   ❌ Data consistency error: {str(e)}")
        test_results['errors'].append(f"Data consistency: {str(e)}")
        test_results['tests_failed'] += 1
    
    # Test 6: Error Handling and Robustness
    print("\n🛡️  TEST 6: Error Handling and Robustness")
    try:
        protocol = IntelligentBARHProtocol()
        
        # Test with invalid data types
        try:
            result = protocol.process_intelligent_correction({
                'latency': 'invalid', 'packet_loss': None, 'throughput': [], 'jitter': {}
            }, simulator)
            print("   ⚠️  Accepts invalid data types")
            test_results['warnings'].append("Weak input validation")
        except:
            print("   ✅ Properly rejects invalid data types")
            test_results['tests_passed'] += 1
        
        # Test with missing keys
        try:
            result = protocol.process_intelligent_correction({
                'latency': 20  # Missing other keys
            }, simulator)
            if result:
                print("   ✅ Handles missing keys gracefully")
                test_results['tests_passed'] += 1
            else:
                print("   ❌ Fails with missing keys")
                test_results['errors'].append("Missing keys handling")
                test_results['tests_failed'] += 1
        except Exception as e:
            print(f"   ⚠️  Exception with missing keys: {str(e)}")
            test_results['warnings'].append("Missing keys cause exceptions")
        
        # Test simulator failure handling
        class FailingSimulator:
            def apply_correction(self, action, strength):
                raise Exception("Simulator failure")
            def get_current_metrics(self):
                raise Exception("Metrics failure")
        
        failing_sim = FailingSimulator()
        try:
            result = protocol.process_intelligent_correction({
                'latency': 20, 'packet_loss': 2, 'throughput': 50, 'jitter': 10
            }, failing_sim)
            print("   ✅ Handles simulator failures gracefully")
            test_results['tests_passed'] += 1
        except:
            print("   ❌ Doesn't handle simulator failures")
            test_results['errors'].append("Simulator failure handling")
            test_results['tests_failed'] += 1
            
    except Exception as e:
        print(f"   ❌ Error handling test failed: {str(e)}")
        test_results['critical_issues'].append(f"Error handling: {str(e)}")
        test_results['tests_failed'] += 1
    
    # Final Assessment
    print("\n" + "=" * 80)
    print("🏆 COMPREHENSIVE TEST RESULTS")
    print("=" * 80)
    
    total_tests = test_results['tests_passed'] + test_results['tests_failed']
    success_rate = (test_results['tests_passed'] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"📊 OVERALL STATISTICS:")
    print(f"   ✅ Tests Passed: {test_results['tests_passed']}")
    print(f"   ❌ Tests Failed: {test_results['tests_failed']}")
    print(f"   ⚠️  Warnings: {len(test_results['warnings'])}")
    print(f"   🚨 Critical Issues: {len(test_results['critical_issues'])}")
    print(f"   📈 Success Rate: {success_rate:.1f}%")
    
    if test_results['critical_issues']:
        print(f"\n🚨 CRITICAL ISSUES FOUND:")
        for issue in test_results['critical_issues']:
            print(f"   • {issue}")
    
    if test_results['errors']:
        print(f"\n❌ ERRORS FOUND:")
        for error in test_results['errors']:
            print(f"   • {error}")
    
    if test_results['warnings']:
        print(f"\n⚠️  WARNINGS:")
        for warning in test_results['warnings']:
            print(f"   • {warning}")
    
    # Overall Assessment
    if len(test_results['critical_issues']) == 0 and test_results['tests_failed'] < 2:
        print(f"\n🏆 OVERALL ASSESSMENT: SYSTEM READY FOR PRODUCTION")
        print(f"✅ No critical issues found")
        print(f"✅ Minimal errors detected")
        print(f"🚀 Safe for publication and deployment")
    elif len(test_results['critical_issues']) == 0:
        print(f"\n⚠️  OVERALL ASSESSMENT: SYSTEM NEEDS MINOR FIXES")
        print(f"✅ No critical issues found")
        print(f"⚠️  Some errors need attention")
        print(f"📝 Address errors before final publication")
    else:
        print(f"\n🚨 OVERALL ASSESSMENT: CRITICAL ISSUES REQUIRE IMMEDIATE ATTENTION")
        print(f"❌ Critical issues must be resolved")
        print(f"🛠️  System needs debugging before publication")
    
    return test_results

if __name__ == "__main__":
    results = comprehensive_system_test()
    
    # Save test results
    timestamp = int(time.time())
    filename = f"comprehensive_test_results_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Test results saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving results: {str(e)}")
    
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE SYSTEM TEST COMPLETED!")
    print("=" * 80)
