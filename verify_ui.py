from playwright.sync_api import sync_playwright
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Wait for the simulation logic to render initially
    page.goto(f"file:///app/index.html")
    page.wait_for_timeout(2000)

    # Take screenshot
    os.makedirs("/home/jules/verification/screenshots/", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/leviathan_sim.png")

    # Record video
    os.makedirs("/home/jules/verification/videos/", exist_ok=True)
    # Re-create context to start recording
    context.close()

    context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
    page = context.new_page()
    page.goto(f"file:///app/index.html")

    # Wait to record a few seconds of animation
    page.wait_for_timeout(3000)

    context.close() # close context to save video
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
