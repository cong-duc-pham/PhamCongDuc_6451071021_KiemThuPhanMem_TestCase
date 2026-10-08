import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseTest:
    """
    BaseTest: Initializes WebDriver and manages browser lifecycle.
    Integrates automatic screenshot capture and attaches artifacts to Allure Report upon test failure.
    """

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, request):
        options = Options()
        is_headed = os.environ.get("HEADED", "false").lower() == "true"
        if not is_headed:
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(30)

        request.cls.driver = self.driver

        yield

        # Capture screenshot and attach to Allure Report on test failure
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "build", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"{request.node.name}.png")
            try:
                self.driver.save_screenshot(screenshot_path)
                print(f"\n[Screenshot on Failure] Saved screenshot to: {screenshot_path}")
            except Exception as e:
                print(f"\n[Screenshot Error] Failed to capture screenshot: {e}")

            try:
                import allure
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name=f"Screenshot_{request.node.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass

        if self.driver:
            self.driver.quit()
