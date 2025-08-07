from playwright.sync_api import sync_playwright
from python_ghost_cursor.playwright_sync import create_cursor

user_data_dir = "/home/neo-new/playwright-profiles/cloned-profile"  # Replace with your actual path

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = browser.new_page()
    page.goto("http://127.0.0.1:8000")  # Your local site with captcha

    cursor = create_cursor(page)

    # Target the iframe containing the checkbox
    iframe_locator = page.locator("iframe[src*='recaptcha/api2/anchor']")
    location = page.locator("h2")
    # cursor.click(iframe_locator)

    print("Clicked iframe with ghost cursor")

    page.wait_for_timeout(30000)
    input("Enter:")
    browser.close()


        # stealth_sync(page)

#         page.add_init_script("""
#     Object.defineProperty(navigator, 'webdriver', {
#         get: () => false
#     });
# """)


        # page.add_init_script("""
        #     (() => {
        #         const cursor = document.createElement('div');
        #         cursor.id = 'playwright-cursor';
        #         cursor.style.position = 'fixed';
        #         cursor.style.top = '0';
        #         cursor.style.left = '0';
        #         cursor.style.width = '10px';
        #         cursor.style.height = '10px';
        #         cursor.style.background = 'red';
        #         cursor.style.borderRadius = '50%';
        #         cursor.style.zIndex = '999999';
        #         cursor.style.pointerEvents = 'none';
        #         document.body.appendChild(cursor);

        #         document.addEventListener('mousemove', e => {
        #             cursor.style.left = e.clientX + 'px';
        #             cursor.style.top = e.clientY + 'px';
        #         });
        #     })();
        #     """)
