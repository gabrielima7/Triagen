from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    # Navigate to the generated HTML file directly
    page.goto("file:///app/index.html")
    page.wait_for_timeout(500)

    # Wait for the canvas to be visible (simulation runs on a canvas)
    page.wait_for_selector("canvas", state="visible", timeout=10000)

    # Wait a bit to let the simulation run a few frames
    page.wait_for_timeout(3000)

    # Take a screenshot to verify visualization
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")

    # Hold for final state for the video
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a context explicitly to record video
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            # MUST close context before browser to save video file
            context.close()
            browser.close()
