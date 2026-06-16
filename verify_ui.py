from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
    page = context.new_page()
    page.goto("file:///app/index.html")
    page.screenshot(path="/home/jules/verification/screenshots/ui.png")
    context.close()
    browser.close()
