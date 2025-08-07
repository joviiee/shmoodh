import matplotlib.pyplot as plt
from python_ghost_cursor import path
from playwright.sync_api import sync_playwright
from python_ghost_cursor.playwright_sync import create_cursor

from typing_extensions import Dict,List,Union

import bezier
import numpy as np

import random
from time import sleep

def unpack_points(payload:Dict):
    try:
        return payload["x"],payload["y"]
    except:
        Warning("Make the key names 'x' and 'y'.")

def generate_focal_point(start:Dict,end:Dict):
    '''
    - generate random but not so random focal point
    '''
    start_x,start_y = unpack_points(start)
    end_x,end_y = unpack_points(end)




def create_bezier_curve(start:Dict,end:Dict):
    '''
    - calculate the focal point
    - generate the curve 
    - give the op as two arrays
    '''
    start_x,start_y = unpack_points(start)
    end_x,end_y = unpack_points(end)

    # calculating the focal point


user_data_dir = "/home/neo-new/playwright-profiles/cloned-profile"  # Replace with your actual path
    
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        slow_mo=1000, 
    )

    page = browser.new_page()
    
    print("🚀 Navigating to Upwork job page...")
    page.goto(
        "https://www.upwork.com/freelance-jobs/apply/Anamorphic-Video-Creator-Needed_~021945883745462019793",
        wait_until="domcontentloaded",
    )

    page.evaluate("""
            () => {
                // Initialize mouse position
                window._mousePosition = { x: 0, y: 0 };

                // Create black dot
                const dot = document.createElement('div');
                dot.id = 'cursor-dot';
                Object.assign(dot.style, {
                    position: 'fixed',
                    width: '8px',
                    height: '8px',
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
        """)

    sleep(2)
    print("fetching mouse coords")
    position = page.evaluate("() => window.getMousePosition()")
    print(position)

    # page.wait_for_selector('input.thebutton')
    page.wait_for_selector('#navSearchForm')

    button = page.query_selector('input.thebutton')
    element = page.locator("#navSearchForm")
    bbox = element.bounding_box()

    print(f"Button Bounding Box: {bbox}")

    # Get target point (center of button)
    target_x = bbox["x"] + bbox["width"] / 2
    target_y = bbox["y"] + bbox["height"] / 2

    # ghost = create_cursor(page=page)
    # ghost.click(element)

    mouse_path = path(start={'x':position['x'],'y': position['y']}, end={'x':target_x,'y': target_y})

    print(mouse_path)
    
    for point in mouse_path:
        page.mouse.move(x=point['x'],y=point['y'])
        print(f"reached {point['x'],point['y']}")
        sleep(random.uniform(0.001,0.01))

    page.mouse.down()
    
    input("=========")

# from playwright.sync_api import sync_playwright
# from python_ghost_cursor import path_generator
# from python_ghost_cursor.playwright_sync import move as human_move
# import time

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False, slow_mo=50)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("file:///absolute/path/to/your/form.html")  # Replace with actual URL if hosted

#     # Wait for the button to appear
#     page.wait_for_selector('input[type="submit"]')

#     # Locate the submit button
#     button = page.query_selector('input[type="submit"]')
#     bbox = button.bounding_box()

#     print(f"Button Bounding Box: {bbox}")

#     # Get target point (center of button)
#     target_x = bbox["x"] + bbox["width"] / 2
#     target_y = bbox["y"] + bbox["height"] / 2

#     # Optional: Move to initial position before path
#     page.mouse.move(0, 0)

#     # Simulate human-like movement
#     human_move(page.mouse, start=(0, 0), end=(target_x, target_y))

#     # Pause slightly to mimic human delay
#     time.sleep(0.3)

#     # Click the button
#     page.mouse.click(target_x, target_y)

#     time.sleep(3)
#     browser.close()
