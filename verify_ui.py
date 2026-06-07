from playwright.sync_api import sync_playwright
import os
import time

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Ensure verification directories exist
        os.makedirs('/home/jules/verification/screenshots', exist_ok=True)
        os.makedirs('/home/jules/verification/videos', exist_ok=True)

        # Start a context that records video
        context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = context.new_page()

        # Navigate to the auto-generated HTML
        page.goto('file:///app/index.html')

        # Give it a tiny bit of time to render
        time.sleep(1)

        # Take a screenshot
        screenshot_path = '/home/jules/verification/screenshots/investigator_cultist_ui.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # VERY IMPORTANT: Close context to flush video to disk before closing browser
        context.close()
        browser.close()

if __name__ == "__main__":
    # Ensure state and html is generated first
    import simulation
    verify_frontend()
