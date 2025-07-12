from flask import Flask, request, render_template, jsonify, send_from_directory
from playwright.sync_api import sync_playwright
import uuid
import os
import requests
import json

app = Flask(__name__)

# Use environment variable for images directory, default to ./images for local
IMAGES_DIR = os.environ.get('IMAGES_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images'))
os.makedirs(IMAGES_DIR, exist_ok=True)

# DeepSeek API configuration
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def analyze_intent_with_deepseek(user_input):
    """
    Send user input to DeepSeek for intent analysis
    Returns a dictionary with identified intents and parameters
    """
    if not DEEPSEEK_API_KEY:
        return {"error": "DeepSeek API key not configured"}
    
    # Prompt for intent analysis
    system_prompt = """
    You are an intent analyzer for an API system. Analyze the user's input and identify their intent.
    
    Available intents and their parameters:
    1. generate_pendant: {"intent": "generate_pendant", "parameters": {"name": "string"}}
    2. create_gift: {"intent": "create_gift", "parameters": {"type": "string", "recipient": "string"}}
    3. customize_design: {"intent": "customize_design", "parameters": {"style": "string", "color": "string"}}
    4. get_catalog: {"intent": "get_catalog", "parameters": {"category": "string"}}
    5. contact_support: {"intent": "contact_support", "parameters": {"issue": "string"}}
    
    Respond with ONLY a valid JSON object containing the identified intent and parameters.
    If no clear intent is found, use: {"intent": "unknown", "parameters": {}}
    """
    
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.1,
            "max_tokens": 200
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Parse the JSON response from DeepSeek
        try:
            intent_data = json.loads(content)
            return intent_data
        except json.JSONDecodeError:
            return {"intent": "unknown", "parameters": {}, "error": "Failed to parse DeepSeek response"}
            
    except requests.exceptions.RequestException as e:
        return {"intent": "unknown", "parameters": {}, "error": f"DeepSeek API error: {str(e)}"}

def route_to_internal_endpoint(intent, parameters):
    """
    Route the request to appropriate internal endpoint based on intent
    """
    try:
        if intent == "generate_pendant":
            # Route to existing pendant generation endpoint
            name = parameters.get('name', 'Thaamu')
            return generate_pendant_internal(name)
            
        elif intent == "create_gift":
            # Route to gift creation endpoint (to be implemented)
            gift_type = parameters.get('type', 'general')
            recipient = parameters.get('recipient', 'friend')
            return create_gift_internal(gift_type, recipient)
            
        elif intent == "customize_design":
            # Route to design customization endpoint (to be implemented)
            style = parameters.get('style', 'classic')
            color = parameters.get('color', 'gold')
            return customize_design_internal(style, color)
            
        elif intent == "get_catalog":
            # Route to catalog endpoint (to be implemented)
            category = parameters.get('category', 'all')
            return get_catalog_internal(category)
            
        elif intent == "contact_support":
            # Route to support endpoint (to be implemented)
            issue = parameters.get('issue', 'general inquiry')
            return contact_support_internal(issue)
            
        else:
            return {
                "success": False,
                "error": f"Unknown intent: {intent}",
                "available_intents": [
                    "generate_pendant", "create_gift", "customize_design", 
                    "get_catalog", "contact_support"
                ]
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error routing to internal endpoint: {str(e)}"
        }

# Internal endpoint implementations
def generate_pendant_internal(name):
    """Internal implementation of pendant generation"""
    unique_id = uuid.uuid4().hex
    html_file = f"render_{unique_id}.html"
    output_file = os.path.join(IMAGES_DIR, f"pendant_{unique_id}.png")
    
    # Render the Jinja2 HTML with name
    rendered_html = render_template("pendant_template.html", name=name)
    
    # Save temporary HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
        
    # Launch Playwright and render the page to screenshot
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1000, 'height': 600})
        page.goto(f'file://{os.path.abspath(html_file)}')
        page.wait_for_timeout(1000)  # wait for fonts/images to load
        # Screenshot only the pendant-wrapper for a zoomed-in effect
        pendant_wrapper = page.locator('.pendant-wrapper')
        pendant_wrapper.screenshot(path=output_file)
        browser.close()
    
    os.remove(html_file)  # Clean up
    
    # Construct the public URL for Railway (served by Flask)
    public_url = f"/images/{os.path.basename(output_file)}"
    return {
        "success": True,
        "intent": "generate_pendant",
        "url": public_url,
        "file_path": output_file,
        "parameters": {"name": name}
    }

def create_gift_internal(gift_type, recipient):
    """Internal implementation of gift creation"""
    return {
        "success": True,
        "intent": "create_gift",
        "message": f"Gift creation initiated for {recipient} with type: {gift_type}",
        "parameters": {"type": gift_type, "recipient": recipient}
    }

def customize_design_internal(style, color):
    """Internal implementation of design customization"""
    return {
        "success": True,
        "intent": "customize_design",
        "message": f"Design customized with style: {style} and color: {color}",
        "parameters": {"style": style, "color": color}
    }

def get_catalog_internal(category):
    """Internal implementation of catalog retrieval"""
    return {
        "success": True,
        "intent": "get_catalog",
        "message": f"Catalog retrieved for category: {category}",
        "parameters": {"category": category}
    }

def contact_support_internal(issue):
    """Internal implementation of support contact"""
    return {
        "success": True,
        "intent": "contact_support",
        "message": f"Support ticket created for issue: {issue}",
        "parameters": {"issue": issue}
    }

@app.route('/mediator', methods=['POST'])
def mediator_endpoint():
    """
    Mediator API endpoint that:
    1. Accepts user input
    2. Sends to DeepSeek for intent analysis
    3. Routes to appropriate internal endpoints
    """
    try:
        # Get user input from request
        data = request.get_json()
        if not data or 'user_input' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'user_input' in request body"
            }), 400
        
        user_input = data['user_input']
        
        # Analyze intent with DeepSeek
        intent_analysis = analyze_intent_with_deepseek(user_input)
        
        if "error" in intent_analysis:
            return jsonify({
                "success": False,
                "error": intent_analysis["error"],
                "user_input": user_input
            }), 500
        
        # Extract intent and parameters
        intent = intent_analysis.get("intent", "unknown")
        parameters = intent_analysis.get("parameters", {})
        
        # Route to internal endpoint
        result = route_to_internal_endpoint(intent, parameters)
        
        # Add metadata to response
        result.update({
            "user_input": user_input,
            "intent_analysis": intent_analysis,
            "timestamp": str(uuid.uuid4())
        })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Mediator endpoint error: {str(e)}",
            "user_input": data.get('user_input', 'unknown') if 'data' in locals() else 'unknown'
        }), 500

@app.route('/generate-pendant', methods=['POST'])
def generate_pendant():
    name = request.json.get('name', 'Thaamu')
    unique_id = uuid.uuid4().hex
    html_file = f"render_{unique_id}.html"
    output_file = os.path.join(IMAGES_DIR, f"pendant_{unique_id}.png")
    
    # Render the Jinja2 HTML with name
    rendered_html = render_template("pendant_template.html", name=name)
    
    # Save temporary HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
        
    
    # Launch Playwright and render the page to screenshot
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1000, 'height': 600})
        page.goto(f'file://{os.path.abspath(html_file)}')
        page.wait_for_timeout(1000)  # wait for fonts/images to load
        # Screenshot only the pendant-wrapper for a zoomed-in effect
        pendant_wrapper = page.locator('.pendant-wrapper')
        pendant_wrapper.screenshot(path=output_file)
        browser.close()
    
    os.remove(html_file)  # Clean up
    
    # Construct the public URL for Railway (served by Flask)
    public_url = f"/images/{os.path.basename(output_file)}"
    return jsonify({
        "url": public_url,
        "file_path": output_file
    })

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8082))
    app.run(debug=True, host='0.0.0.0', port=port) 