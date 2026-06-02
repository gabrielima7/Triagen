import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("file:///app/index.html")
        await page.wait_for_timeout(2000)  # wait for canvas to render
        await page.screenshot(path="/home/jules/verification/screenshots/ui_verification.png")
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
