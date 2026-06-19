from playwright.sync_api import sync_playwright
import os
import glob

def run_cuj(page):
    # We need to run simulation.py first to generate the index.html
    os.system("python3 simulation.py")

    file_path = f"file:///app/index.html"
    page.goto(file_path)
    page.wait_for_timeout(2000)

    # Take screenshot at the key moment
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/nightgaunt_ui.png")
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
