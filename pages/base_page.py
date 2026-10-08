from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Foundation layer: BasePage
    Parent class for all Page Objects: encapsulates WebDriver and Explicit Wait.
    Follows Page Object Model design principles:
    - Principle 1: Page Objects do NOT contain test assertions.
    - Principle 2: Locators are private and encapsulated.
    - Principle 3: Fluent Navigation (returns next Page Object).
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Explicit wait up to 10 seconds

    def click(self, locator):
        """Wait for element to become clickable before clicking."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def js_click(self, locator):
        """Execute JavaScript click for elements styled with CSS overlays."""
        el = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", el)

    def type(self, locator, text):
        """Input text: wait for visibility and clear existing text before typing."""
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        """Retrieve visible text with Explicit Wait."""
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def get_attribute(self, locator, attr_name):
        """Retrieve HTML attribute value of a given locator."""
        el = self.wait.until(EC.presence_of_element_located(locator))
        return el.get_attribute(attr_name)

    def is_element_present(self, locator):
        """Check whether an element is present in the DOM."""
        return len(self.driver.find_elements(*locator)) > 0
