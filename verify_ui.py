from playwright.sync_api import sync_playwright
import time

def run_cuj(page):
    # Navigate to the generated HTML file directly
    page.goto("file:///app/index.html")
    page.wait_for_timeout(500)

    # Let the simulation run for a few seconds if there was dynamic JS (though our index.html is static render for now)
    page.wait_for_timeout(1000)

    # Take screenshot at the key moment
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)  # Hold final state for the video

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
