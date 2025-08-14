from playwright.sync_api import sync_playwright
from python_ghost_cursor.playwright_sync import create_cursor
from python_ghost_cursor import path

import random
from time import sleep
import matplotlib.pyplot as plt
import subprocess
import json
import urllib.request

def create_cursor_tracker():
    """Simple red circle cursor tracker"""
    return """
            () => {
                // Initialize mouse position
                window._mousePosition = { x: 0, y: 0 };

                // Create black dot
                const dot = document.createElement('div');
                dot.id = 'cursor-dot';
                Object.assign(dot.style, {
                    position: 'fixed',
                    width: '18px',
                    height: '18px',
                    backgroundColor: 'black',
                    borderRadius: '50%',
                    pointerEvents: 'none',
                    zIndex: '9999',
                    top: '0px',
                    left: '0px',
                    transform: 'translate(-50%, -50%)'
                });
                document.body.appendChild(dot);

                // Track mouse movement and update position
                window.addEventListener('mousemove', (event) => {
                    window._mousePosition.x = event.clientX;
                    window._mousePosition.y = event.clientY;

                    const dot = document.getElementById('cursor-dot');
                    if (dot) {
                        dot.style.left = event.clientX + 'px';
                        dot.style.top = event.clientY + 'px';
                    }
                });

                // Expose mouse position getter
                window.getMousePosition = () => {
                    return window._mousePosition;
                };
            }
        """

class VisualGhostCursor:
    def __init__(self, page, cursor):
        self.page = page
        self.cursor = cursor
        self.setup_tracking()
    
    def setup_tracking(self):
        """Initialize the visual cursor tracker"""
        try:
            result = self.page.evaluate(create_cursor_tracker())
            print(f"✓ {result}")
        except Exception as e:
            print(f"Warning: Could not initialize cursor tracker: {e}")
    
    def move_towards(self, x, y):
        """Move cursor with visual tracking"""
        try:
            # Update visual cursor first
            self.page.evaluate(f"window.updateGhostCursor && updateGhostCursor({x}, {y})")
        except:
            pass
        
        # Move the actual cursor
        return self.cursor.move_to({"x":x, "y":y})
    
    def click(self, locator_or_coords, **kwargs):
        """Click with visual feedback"""
        try:
            # Get coordinates if locator is provided
            if hasattr(locator_or_coords, 'bounding_box'):
                bbox = locator_or_coords.bounding_box()
                print("has bounding box")
                if bbox:
                    print("got bbox")
                    x = bbox['x'] + bbox['width'] / 2
                    y = bbox['y'] + bbox['height'] / 2
                    print(x,y)
                    pos = self.page.evaluate("() => getCurrentMousePos()")
                    current_x = pos['x']
                    current_y = pos['y']
                    mouse_path = path({x:current_x,y:current_y},{x:x,y:y})
                    print("printing mouse path .... ")
                    for item in mouse_path:
                        print(f"point -- {item = }")
                    path_x, path_y = zip(*mouse_path)
                    plt.plot(path_x,path_y)
                    plt.show()
                    print("path displayed .... ")
                    sleep(5)
                    self.page.evaluate(f"window.updateGhostCursor && updateGhostCursor({x}, {y})")
            else:
                print("bbox no no")
            
            # Flash cursor for click feedback
            self.page.evaluate("window.flashGhostCursor && flashGhostCursor()")
        except:
            pass
        
        # Perform the actual click
        return self.cursor.click(locator_or_coords, **kwargs)
    
    def move_by_offset(self, x_offset, y_offset):
        """Move by offset with visual tracking"""
        try:
            # Get current position and calculate new position
            current_pos = self.page.evaluate("""
                () => {
                    const circle = document.getElementById('ghost-cursor-tracker');
                    if (circle) {
                        const rect = circle.getBoundingClientRect();
                        return {x: rect.left + rect.width/2, y: rect.top + rect.height/2};
                    }
                    return {x: 0, y: 0};
                }
            """)
            
            new_x = current_pos['x'] + x_offset
            new_y = current_pos['y'] + y_offset
            
            self.page.evaluate(f"window.updateGhostCursor && updateGhostCursor({new_x}, {new_y})")
        except:
            pass
        
        return self.cursor.move_by_offset(x_offset, y_offset)

user_data_dir = "/home/neo-new/playwright-profiles/cloned-profile"  # Replace with your actual path
chrome_executable_path = "/usr/bin/google-chrome"  # Replace with your actual Chrome path

# subprocess.Popen([
#     chrome_executable_path,
#     f'--user-data-dir={user_data_dir}',
#     '--remote-debugging-port=9222',
#     '--no-first-run',
#     '--no-default-browser-check'
# ])
ws_url = json.load(urllib.request.urlopen("http://localhost:9222/json/version"))["webSocketDebuggerUrl"]

# with sync_playwright() as p:
#     browser = p.chromium.launch_persistent_context(
#         user_data_dir=user_data_dir,
#         executable_path=chrome_executable_path,
#         headless=False,
#         args=[
#         "--disable-blink-features=AutomationControlled",
#         "--disable-infobars",
#         "--start-maximized",
#         "--no-sandbox",
#         "--disable-dev-shm-usage"
#     ],
#         viewport={"width": 1920, "height": 1080},
#         color_scheme="dark",
#         locale="en-US",
#         timezone_id="America/New_York",
#     )

#     init_page = browser.new_page()
#     init_page.goto("https://www.google.com/", wait_until="domcontentloaded")

#     sleep(60)

#     page = browser.new_page()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(ws_url)
    page = browser.contexts[0].pages[0]

    page.add_init_script("""
        // Our injection code here
        Element.prototype._attachShadow = Element.prototype.attachShadow;
        Element.prototype.attachShadow = function() {
            console.log('Shadow DOM creation intercepted');
            const shadow = this._attachShadow({ mode: 'open' });
            return shadow;
        };
    """)

    original_cursor = create_cursor(page=page)
    page.goto("https://google.com", wait_until="domcontentloaded",)  # Your local site with captcha
    sleep(2)

    search_keyword = "upwork"

    google_cursor = VisualGhostCursor(page, original_cursor)

    google_search_locator = page.locator("textarea[title='Search']")
    google_cursor.click(google_search_locator)

    page.keyboard.type(search_keyword, delay=random.randint(10, 300))
    page.keyboard.press("Enter")

    # Target the iframe containing the checkbox
    # iframe_element = page.frame_locator("iframe[title='Widget containing a Cloudflare security challenge']")
    # location = page.locator("#cf-turnstile")
    # cursor.click(iframe_element.locator(".cb-i"))
    # sleep(60)

    # print("Clicked iframe with ghost cursor")

    # page.wait_for_timeout(30000)
    input("Enter:")
    browser.close()

