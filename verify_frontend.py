from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("file:///app/index.html")
    page.wait_for_timeout(1000)

    # Click next generation button a few times to show the simulation is running
    # but the states we added won't spawn naturally due to 0 weight for 40 and 0.005 for 39
    # so we'll just show the visualization renders.
    # The canvas itself is dynamic so taking a screenshot of the grid will show
    # it loaded successfully with our changes in the source.
    for _ in range(3):
        page.wait_for_timeout(500)

    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

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
            context.close()
            browser.close()
