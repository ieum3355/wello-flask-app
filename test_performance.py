#!/usr/bin/env python3
"""
Performance test script for Wello application
Tests response times, cache efficiency, and API call optimization
"""

import requests
import time
import json
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

class PerformanceTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = []
        
    def test_single_request(self, query):
        """Test a single API request"""
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/api/recommendation",
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                "query": query,
                "duration": duration,
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response_size": len(response.content) if response.content else 0
            }
            
        except Exception as e:
            return {
                "query": query,
                "duration": time.time() - start_time,
                "status_code": None,
                "success": False,
                "error": str(e)
            }
    
    def test_cache_efficiency(self, queries, iterations=3):
        """Test cache efficiency with repeated queries"""
        print(f"Testing cache efficiency with {len(queries)} queries, {iterations} iterations each...")
        
        all_results = []
        
        for i in range(iterations):
            print(f"Iteration {i+1}/{iterations}")
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(self.test_single_request, query) for query in queries]
                
                for future in as_completed(futures):
                    result = future.result()
                    all_results.append(result)
        
        return all_results
    
    def test_concurrent_requests(self, query, num_requests=10):
        """Test concurrent request handling"""
        print(f"Testing {num_requests} concurrent requests for query: '{query}'")
        
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(self.test_single_request, query) for _ in range(num_requests)]
            
            results = []
            for future in as_completed(futures):
                results.append(future.result())
        
        return results
    
    def get_performance_stats(self):
        """Get current performance statistics from the app"""
        try:
            response = requests.get(f"{self.base_url}/api/performance")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get stats: {response.status_code}"}
        except Exception as e:
            return {"error": f"Failed to connect: {str(e)}"}
    
    def analyze_results(self, results):
        """Analyze test results"""
        if not results:
            return {}
        
        successful_results = [r for r in results if r.get("success", False)]
        failed_results = [r for r in results if not r.get("success", False)]
        
        if not successful_results:
            return {
                "total_requests": len(results),
                "successful_requests": 0,
                "failed_requests": len(failed_results),
                "success_rate": 0,
                "error": "No successful requests"
            }
        
        durations = [r["duration"] for r in successful_results]
        
        return {
            "total_requests": len(results),
            "successful_requests": len(successful_results),
            "failed_requests": len(failed_results),
            "success_rate": len(successful_results) / len(results),
            "avg_response_time": statistics.mean(durations),
            "min_response_time": min(durations),
            "max_response_time": max(durations),
            "median_response_time": statistics.median(durations),
            "avg_response_size": statistics.mean([r.get("response_size", 0) for r in successful_results])
        }
    
    def run_comprehensive_test(self):
        """Run comprehensive performance test"""
        print("🚀 Starting comprehensive performance test...")
        
        # Test queries
        test_queries = [
            "비타민D",
            "오메가3",
            "탈모",
            "피로",
            "면역력"
        ]
        
        # 1. Test cache efficiency
        print("\n📊 Testing cache efficiency...")
        cache_results = self.test_cache_efficiency(test_queries, iterations=2)
        cache_analysis = self.analyze_results(cache_results)
        
        # 2. Test concurrent requests
        print("\n⚡ Testing concurrent requests...")
        concurrent_results = self.test_concurrent_requests("비타민D", num_requests=5)
        concurrent_analysis = self.analyze_results(concurrent_results)
        
        # 3. Get app performance stats
        print("\n📈 Getting application performance stats...")
        app_stats = self.get_performance_stats()
        
        # Print results
        print("\n" + "="*50)
        print("📊 PERFORMANCE TEST RESULTS")
        print("="*50)
        
        print(f"\n🎯 Cache Efficiency Test:")
        print(f"   Total Requests: {cache_analysis.get('total_requests', 0)}")
        print(f"   Success Rate: {cache_analysis.get('success_rate', 0):.1%}")
        print(f"   Avg Response Time: {cache_analysis.get('avg_response_time', 0):.3f}s")
        print(f"   Min Response Time: {cache_analysis.get('min_response_time', 0):.3f}s")
        print(f"   Max Response Time: {cache_analysis.get('max_response_time', 0):.3f}s")
        
        print(f"\n⚡ Concurrent Request Test:")
        print(f"   Total Requests: {concurrent_analysis.get('total_requests', 0)}")
        print(f"   Success Rate: {concurrent_analysis.get('success_rate', 0):.1%}")
        print(f"   Avg Response Time: {concurrent_analysis.get('avg_response_time', 0):.3f}s")
        
        if "performance" in app_stats:
            perf = app_stats["performance"]
            print(f"\n📈 Application Performance Stats:")
            print(f"   Avg Request Time: {perf.get('avg_request_time', 0):.3f}s")
            print(f"   Total Requests: {perf.get('total_requests', 0)}")
            print(f"   API Calls: {perf.get('api_calls', 0)}")
            print(f"   Cache Hit Rate: {perf.get('cache_hit_rate', 0):.1%}")
        
        # Performance recommendations
        print(f"\n💡 Performance Recommendations:")
        
        avg_time = cache_analysis.get('avg_response_time', 0)
        if avg_time > 2.0:
            print("   ⚠️  Response time is high (>2s). Consider:")
            print("      - Increasing cache timeout")
            print("      - Optimizing API calls")
            print("      - Adding more server resources")
        elif avg_time > 1.0:
            print("   ⚠️  Response time is moderate (>1s). Consider:")
            print("      - Fine-tuning cache settings")
            print("      - Monitoring API performance")
        else:
            print("   ✅ Response time is good (<1s)")
        
        success_rate = cache_analysis.get('success_rate', 0)
        if success_rate < 0.95:
            print("   ⚠️  Success rate is low (<95%). Check:")
            print("      - API key configuration")
            print("      - Network connectivity")
            print("      - Server logs")
        else:
            print("   ✅ Success rate is good (>95%)")
        
        return {
            "cache_test": cache_analysis,
            "concurrent_test": concurrent_analysis,
            "app_stats": app_stats
        }

if __name__ == "__main__":
    tester = PerformanceTester()
    results = tester.run_comprehensive_test()
    
    # Save results to file
    with open("performance_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to performance_test_results.json")