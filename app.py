from flask import Flask, request, render_template, jsonify, send_from_directory
from playwright.sync_api import sync_playwright
import os
import uuid

app = Flask(__name__)

# Ensure the files directory exists
FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
os.makedirs(FILES_DIR, exist_ok=True)

@app.route('/generate-pendant', methods=['POST'])
def generate_pendant():
    name = request.json.get('name', 'Thaamu')
    unique_id = uuid.uuid4().hex
    html_file = f"render_{unique_id}.html"
    output_file = os.path.join(FILES_DIR, f"pendant_{unique_id}.png")
    
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
    public_url = f"/files/pendant_{unique_id}.png"
    return jsonify({"url": public_url})

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(FILES_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8083) 