from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    # Local application path
    filepath = "file:///app/index.html"
    page.goto(filepath)
    page.wait_for_timeout(1000)

    # Let the simulation run for a bit
    page.wait_for_timeout(5000)

    # Take screenshot at the key moment showing the grid with the new state colors
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Ensure directories exist
        os.makedirs("/home/jules/verification/videos", exist_ok=True)

        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
