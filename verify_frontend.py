from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = context.new_page()
        page.goto("file:///app/index.html")
        page.wait_for_timeout(2000) # Give it a second to render
        page.screenshot(path="/home/jules/verification/screenshots/screenshot.png")
        context.close()
        browser.close()
        print("Frontend verification assets saved.")

if __name__ == "__main__":
    verify_frontend()