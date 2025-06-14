from flask import Flask, request, render_template, send_file
from playwright.sync_api import sync_playwright
import os
import uuid

app = Flask(__name__)

@app.route('/generate-pendant', methods=['POST'])
def generate_pendant():
    name = request.json.get('name', 'Thaamu')
    
    html_file = f"render_{uuid.uuid4().hex}.html"
    output_file = f"/tmp/pendant_{uuid.uuid4().hex}.png"
    
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
    
    return send_file(output_file, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082) 