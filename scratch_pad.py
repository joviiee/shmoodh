from playwright.sync_api import sync_playwright
import json
import urllib.request

ws_url = json.load(urllib.request.urlopen("http://localhost:9222/json/version"))["webSocketDebuggerUrl"]

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(ws_url)
    page = browser.new_page()
    page.goto("https://www.google.com", wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
