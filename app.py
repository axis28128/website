from flask import Flask, render_template, request, session, jsonify
import os
import json
import requests
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY')  # Now using from .env
app.config['LANGUAGES'] = ['ro', 'en', 'ru']
app.config['DISCORD_WEBHOOK_URL'] = os.getenv('DISCORD_WEBHOOK_URL')  # From .env

def load_translations():
    translations = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(base_path, 'translations')
    
    for lang in app.config['LANGUAGES']:
        file_path = os.path.join(translations_dir, f'{lang}.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translations[lang] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Translation file for '{lang}' not found")
            # Fallback to English
            try:
                with open(os.path.join(translations_dir, 'en.json'), 'r', encoding='utf-8') as f:
                    translations[lang] = json.load(f)
            except:
                translations[lang] = {}
    return translations

TRANSLATIONS = load_translations()

@app.route('/')
def index():
    lang = session.get('lang', 'ro')
    return render_template('index.html', 
                         lang=lang,
                         translations=TRANSLATIONS.get(lang, TRANSLATIONS['en']),
                         languages=app.config['LANGUAGES'])

@app.route('/set_language', methods=['POST'])
def set_language():
    lang = request.json.get('lang')
    if lang in app.config['LANGUAGES']:
        session['lang'] = lang
        return jsonify({'status': 'success', 'lang': lang})
    return jsonify({'status': 'error', 'message': 'Invalid language'}), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        
        # Create Discord embed
        embed = {
            "title": "New Contact Form Submission",
            "color": 5814783,  # Purple color
            "fields": [
                {"name": "Name", "value": name, "inline": True},
                {"name": "Email", "value": email, "inline": True},
                {"name": "Subject", "value": subject, "inline": False},
                {"name": "Message", "value": message, "inline": False}
            ],
            "footer": {
                "text": "Axis FTC Contact Form"
            }
        }
        
        payload = {
            "embeds": [embed]
        }
        
        # Send to Discord
        response = requests.post(
            app.config['DISCORD_WEBHOOK_URL'],
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 204:
            return jsonify({'status': 'success', 'message': 'Message sent successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send message to Discord'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500