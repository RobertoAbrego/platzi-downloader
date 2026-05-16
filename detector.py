from playwright.sync_api import sync_playwright

def get_m3u8(url):
    found = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context()

        page = context.new_page()

        def handle_response(response):
            response_url = response.url

            if "index" in response_url and ".m3u8" in response_url:
                found.append(response_url)

        page.on("response", handle_response)

        page.goto(url)

        page.wait_for_timeout(10000)

        browser.close()

    return found