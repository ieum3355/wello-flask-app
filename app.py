from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
from utils.gpt import get_ai_recommendation
from flask_caching import Cache
import hashlib
import gzip
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Configure caching for better performance
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes for API responses
cache = Cache(app)

def cache_key_for_query(query):
    """Generate a stable cache key for queries"""
    return f"recommendation_{hashlib.md5(query.lower().strip().encode()).hexdigest()}"

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            # Try to get cached response first
            cache_key = cache_key_for_query(query)
            recommendation = cache.get(cache_key)
            
            if recommendation is None:
                # Not in cache, get fresh response
                recommendation = get_ai_recommendation(query)
                # Cache for 5 minutes
                cache.set(cache_key, recommendation, timeout=300)
    
    return render_template("index.html", recommendation=recommendation)

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
def optimize_response(response):
    """Apply intelligent caching and compression based on content type"""
    
    # Static assets get long-term caching
    if request.endpoint == 'static' or request.path.endswith(('.css', '.js', '.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
        response.headers['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
    
    # HTML pages get short-term caching
    elif response.content_type.startswith('text/html'):
        response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minutes
    
    # API responses and dynamic content
    else:
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    
    # Add security and performance headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Enable compression for text content
    if (response.content_type.startswith(('text/', 'application/json', 'application/javascript')) 
        and 'gzip' in request.headers.get('Accept-Encoding', '')):
        response.direct_passthrough = False
        if len(response.data) > 500:  # Only compress if worth it
            response.data = gzip.compress(response.data)
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Content-Length'] = len(response.data)
    
    return response

if __name__ == "__main__":
    app.run(debug=True)




