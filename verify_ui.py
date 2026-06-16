import time
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = context.new_page()
        page.goto("file:///app/index.html")

        # Wait a bit for simulation frames
        time.sleep(5)

        page.screenshot(path="/home/jules/verification/screenshots/sim_frontend.png")

        context.close()
        browser.close()

if __name__ == "__main__":
    verify()
