from flask import Flask, request, render_template, jsonify
from playwright.sync_api import sync_playwright
import os
import uuid

app = Flask(__name__)

# Helper to construct the public URL for Runway files
RUNWAY_FILES_URL = os.environ.get("RUNWAY_FILES_URL", "https://files.runwayml.com/0dd6e6f0-6631-456a-a2d6-ded7f85e7262")

@app.route('/generate-pendant', methods=['POST'])
def generate_pendant():
    name = request.json.get('name', 'Thaamu')
    unique_id = uuid.uuid4().hex
    html_file = f"render_{unique_id}.html"
    output_file = f"/files/pendant_{unique_id}.png"
    
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
    
    # Construct the public URL (replace <your-app> with your actual app slug)
    public_url = f"{RUNWAY_FILES_URL}/pendant_{unique_id}.png"
    return jsonify({"url": public_url})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8083) 