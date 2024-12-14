from flask import Flask, request, render_template, jsonify, send_file
import os
import subprocess
import tempfile
import yaml
from flask_talisman import Talisman
from flask_seasurf import SeaSurf
from ratelimit import limits, RateLimitException
from functools import wraps
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv('config.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max file size

# Security headers
Talisman(app, 
         force_https=os.getenv('FLASK_ENV') == 'production',  # Only force HTTPS in production
         strict_transport_security=True,
         session_cookie_secure=os.getenv('FLASK_ENV') == 'production',  # Only secure cookies in production
         content_security_policy={
             'default-src': "'self'",
             'script-src': ["'self'", 'cdnjs.cloudflare.com', "'unsafe-inline'"],
             'style-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net'],
             'img-src': ["'self'", 'raw.githubusercontent.com', 'kompose.io'],
         })

# CSRF protection
csrf = SeaSurf(app)

@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=csrf._get_token())

# Setup logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/kompose_online.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Kompose Online startup')

def validate_yaml(content):
    try:
        yaml.safe_load(content)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)

# Rate limiting decorator
def rate_limit_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RateLimitException:
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
    return wrapper

# Rate limit: 30 requests per minute
@limits(calls=int(os.getenv('RATE_LIMIT', 30)), period=60)
def rate_limited_function():
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
@rate_limit_error_handler
def validate():
    rate_limited_function()
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    
    is_valid, error = validate_yaml(content)
    return jsonify({
        'valid': is_valid,
        'error': error
    })

@app.route('/convert', methods=['POST'])
@rate_limit_error_handler
def convert():
    rate_limited_function()
    yaml_content = None
    
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            yaml_content = file.read().decode('utf-8')
        elif 'content' in request.form:
            yaml_content = request.form['content']
        else:
            return jsonify({'error': 'No file or content provided'}), 400

        # Validate YAML
        is_valid, error = validate_yaml(yaml_content)
        if not is_valid:
            return jsonify({'error': f'Invalid YAML: {error}'}), 400

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the compose content
            compose_path = os.path.join(temp_dir, 'docker-compose.yml')
            with open(compose_path, 'w') as f:
                f.write(yaml_content)

            try:
                # Run kompose convert
                process = subprocess.run(
                    ['kompose', 'convert', '-f', compose_path],
                    cwd=temp_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Read all generated files
                helm_files = {}
                for filename in os.listdir(temp_dir):
                    if filename.endswith('.yaml') and filename != 'docker-compose.yml':
                        with open(os.path.join(temp_dir, filename), 'r') as f:
                            helm_files[filename] = f.read()

                app.logger.info(f'Successfully converted compose file')
                return jsonify({
                    'success': True,
                    'files': helm_files
                })

            except subprocess.CalledProcessError as e:
                app.logger.error(f'Conversion failed: {str(e)}\nOutput: {e.output}')
                return jsonify({
                    'error': f'Conversion failed: {e.output}'
                }), 500

    except Exception as e:
        app.logger.error(f'Error during conversion: {str(e)}')
        return jsonify({
            'error': 'An unexpected error occurred'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
