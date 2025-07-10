from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_compress import Compress
from flask_caching import Cache
from dotenv import load_dotenv
from utils.gpt import get_ai_recommendation
from utils.performance import performance_monitor, monitor_performance, log_request_info
import hashlib
import json
import time

load_dotenv()

app = Flask(__name__)

# Enable compression
Compress(app)

# Configure caching
cache_config = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
}
app.config.from_mapping(cache_config)
cache = Cache(app)

@app.before_request
def before_request():
    """Log request information and start timing"""
    log_request_info()
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """Record request time and add performance headers"""
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        performance_monitor.record_request_time(duration)
        response.headers['X-Request-Time'] = f"{duration:.3f}s"
    
    return response

@app.route("/", methods=["GET", "POST"])
@monitor_performance
def index():
    recommendation = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            # Create cache key based on query
            cache_key = f"recommendation_{hashlib.md5(query.encode()).hexdigest()}"
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result:
                recommendation = cached_result
                performance_monitor.record_cache_hit()
            else:
                # Get fresh recommendation
                performance_monitor.record_cache_miss()
                performance_monitor.record_api_call()
                recommendation = get_ai_recommendation(query)
                # Cache the result for 5 minutes
                cache.set(cache_key, recommendation, timeout=300)
    
    return render_template("index.html", recommendation=recommendation)

@app.route("/api/recommendation", methods=["POST"])
@monitor_performance
def api_recommendation():
    """AJAX endpoint for recommendations"""
    data = request.get_json()
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    # Create cache key
    cache_key = f"recommendation_{hashlib.md5(query.encode()).hexdigest()}"
    
    # Try cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        performance_monitor.record_cache_hit()
        return jsonify({"recommendation": cached_result})
    
    # Get fresh recommendation
    try:
        performance_monitor.record_cache_miss()
        performance_monitor.record_api_call()
        recommendation = get_ai_recommendation(query)
        # Cache the result
        cache.set(cache_key, recommendation, timeout=300)
        return jsonify({"recommendation": recommendation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/performance")
def performance_stats():
    """Get performance statistics"""
    stats = performance_monitor.get_stats()
    cache_stats = {
        "cache_type": "simple",
        "status": "active"
    }
    
    return jsonify({
        "performance": stats,
        "cache": cache_stats
    })

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/ads.txt")
def ads():
    return send_from_directory("static", "ads.txt")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")

@app.after_request
def add_security_headers(response):
    """Add security and performance headers"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Cache static assets
    if response.mimetype in ['text/css', 'application/javascript', 'image/png', 'image/jpeg', 'image/gif', 'image/svg+xml']:
        response.headers["Cache-Control"] = "public, max-age=31536000"  # 1 year
    else:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    
    return response

if __name__ == "__main__":
    app.run(debug=True)




