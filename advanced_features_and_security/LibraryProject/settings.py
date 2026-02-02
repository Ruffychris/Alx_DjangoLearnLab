# ----------------------------
# SECURITY SETTINGS (HTTPS)
# ----------------------------

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True
# Explanation: Ensures any HTTP request is automatically redirected to HTTPS.

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Explanation: Instructs browsers to only access the site via HTTPS, including all subdomains.
# Preload allows browsers to remember this setting before first visit.

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Explanation: Ensures that session and CSRF cookies are only sent over HTTPS, preventing interception.

# Additional secure headers
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# Explanation: 
# - X_FRAME_OPTIONS prevents clickjacking by disallowing the site to be embedded in frames.
# - SECURE_CONTENT_TYPE_NOSNIFF prevents MIME type sniffing.
# - SECURE_BROWSER_XSS_FILTER enables browser XSS protection.

# DEBUG should always be False in production
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[your_production_domain_here]']
