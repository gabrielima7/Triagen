from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = context.new_page()

        try:
            # Navigate to the generated HTML page
            page.goto("file:///app/index.html")

            # Wait a moment for simulation to render
            page.wait_for_timeout(2000)

            # Take a screenshot
            page.screenshot(path="/home/jules/verification/screenshots/ghatanothoa_ui.png")
            print("Screenshot saved to /home/jules/verification/screenshots/ghatanothoa_ui.png")

        except Exception as e:
            print(f"Error during frontend verification: {e}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    verify_frontend()
