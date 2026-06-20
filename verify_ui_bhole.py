from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Set up context to record video
        context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = context.new_page()

        # Navigate to the generated HTML file
        page.goto("file:///app/index.html")

        # Wait for the canvas to render
        page.wait_for_selector("canvas")

        # Take a screenshot
        page.screenshot(path="/home/jules/verification/bhole_screenshot.png")

        # Let the simulation run for a bit
        page.wait_for_timeout(3000)

        # Close context first to ensure video is saved properly
        context.close()
        browser.close()

if __name__ == "__main__":
    verify()
