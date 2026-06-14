from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("file:///app/index.html")
    page.wait_for_selector("canvas#simCanvas")
    page.screenshot(path="/home/jules/verification/screenshots/deep_one.png")
    context.close()
    browser.close()
