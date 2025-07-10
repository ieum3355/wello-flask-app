import time
import functools
from flask import request, g
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log performance metrics
            logger.info(f"Function {func.__name__} executed in {execution_time:.3f}s")
            
            # Add performance header to response
            if hasattr(g, 'response_headers'):
                g.response_headers['X-Execution-Time'] = f"{execution_time:.3f}s"
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Function {func.__name__} failed after {execution_time:.3f}s: {str(e)}")
            raise
    
    return wrapper

def log_request_info():
    """Log request information for performance analysis"""
    if request:
        logger.info(f"Request: {request.method} {request.path} - User-Agent: {request.headers.get('User-Agent', 'Unknown')}")

def get_cache_stats(cache):
    """Get cache statistics"""
    try:
        # This is a simple implementation - in production you might want to use Redis
        # and get actual cache statistics
        return {
            "cache_type": "simple",
            "status": "active"
        }
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return {"error": str(e)}

class PerformanceMonitor:
    """Performance monitoring class"""
    
    def __init__(self):
        self.request_times = []
        self.api_calls = 0
        self.cache_hits = 0
        self.cache_misses = 0
    
    def record_request_time(self, duration):
        """Record request duration"""
        self.request_times.append(duration)
        if len(self.request_times) > 100:  # Keep only last 100 requests
            self.request_times.pop(0)
    
    def record_api_call(self):
        """Record API call"""
        self.api_calls += 1
    
    def record_cache_hit(self):
        """Record cache hit"""
        self.cache_hits += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        self.cache_misses += 1
    
    def get_stats(self):
        """Get performance statistics"""
        if not self.request_times:
            return {
                "avg_request_time": 0,
                "total_requests": 0,
                "api_calls": self.api_calls,
                "cache_hit_rate": 0 if (self.cache_hits + self.cache_misses) == 0 else self.cache_hits / (self.cache_hits + self.cache_misses)
            }
        
        return {
            "avg_request_time": sum(self.request_times) / len(self.request_times),
            "total_requests": len(self.request_times),
            "api_calls": self.api_calls,
            "cache_hit_rate": self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()