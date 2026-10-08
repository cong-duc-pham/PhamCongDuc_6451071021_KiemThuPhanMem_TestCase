import os
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture to initialize and teardown WebDriver for test functions and methods.
    """
    options = Options()
    is_headed = os.environ.get("HEADED", "false").lower() == "true"
    if not is_headed:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")

    driver_instance = webdriver.Chrome(options=options)
    driver_instance.maximize_window()
    driver_instance.set_page_load_timeout(30)

    yield driver_instance

    # Capture screenshot on test failure and attach to Allure report
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = os.path.join(os.path.dirname(__file__), "build", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshots_dir, f"{request.node.name}.png")
        try:
            driver_instance.save_screenshot(screenshot_path)
            print(f"\n[Screenshot on Failure] Saved screenshot to: {screenshot_path}")
        except Exception:
            pass

        try:
            import allure
            allure.attach(
                driver_instance.get_screenshot_as_png(),
                name=f"Screenshot_Failure_{request.node.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass

    if driver_instance:
        driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture test outcome for failure reporting."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
