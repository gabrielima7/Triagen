import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = await context.new_page()
        await page.goto("file:///app/index.html")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="/home/jules/verification/screenshots/grid.png")
        await context.close()
        await browser.close()

asyncio.run(run())
