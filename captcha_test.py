from playwright.sync_api import sync_playwright
from python_ghost_cursor.playwright_sync import create_cursor
from python_ghost_cursor import path

import random
from time import sleep
import matplotlib.pyplot as plt

job_url = "https://www.upwork.com/freelance-jobs/apply/Anamorphic-Video-Creator-Needed_~021945883745462019793"
main_url = "https://www.upwork.com/nx/find-work/best-matches"

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

# Custom cursor class that includes visual tracking
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

def main():
    user_data_dir = "/home/neo-new/playwright-profiles/cloned-profile"  # Replace with your actual path
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            # slow_mo=1000, 
        )

        page = browser.new_page()
        
        # Create the original ghost cursor
        original_cursor = create_cursor(page=page)
        
        # Wrap it with visual tracking
        
        
        print("🚀 Navigating to Upwork job page...")
        page.goto(
            main_url,
            wait_until="domcontentloaded",
        )
        
        # Wait for page to load completely
        sleep(2)
        cursor = VisualGhostCursor(page, original_cursor)
        
        print("🔍 Looking for search form element...")
        element = page.locator(".nav-search-autosuggest-input")
        
        if element.count() > 0:
            print(f"✓ Element found: {element}")
            sleep(random.random())
            
            print("🖱️  Clicking on search form...")
            cursor.click(element)
            
            print("✓ Click completed with visual feedback")
        else:
            print("❌ Search form element not found")
            
            # Try to find other clickable elements for demonstration
            print("🔍 Looking for other clickable elements...")
            buttons = page.locator("button, a, input[type='button'], input[type='submit']").first
            if buttons.count() > 0:
                print("Found alternative element to click...")
                cursor.click(buttons)

        # Optional: Move cursor around for demonstration
        print("🎯 Demonstrating cursor movement...")
        try:
            # Move to a few random positions to show the visual tracker
            for i in range(3):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                print(f"Moving to position ({x}, {y})...")
                cursor.move_towards(x=x, y=y)
                sleep(0.5)
        except Exception as e:
            print(f"Movement demonstration error: {e}")

        print("⏳ Pausing for manual interaction...")
        input("Solve any captchas or interact with the page, then press Enter to continue...")

        # Optional: Hide cursor tracker before finishing
        try:
            page.evaluate("window.hideGhostCursor && hideGhostCursor()")
            print("🔇 Visual cursor tracker hidden")
        except:
            pass

        print("📄 Getting page content...")
        content_length = len(page.content())
        print(f"✓ Page content retrieved ({content_length} characters)")

        print("🔚 Closing browser...")
        sleep(10)
        browser.close()

if __name__ == "__main__":
    main()