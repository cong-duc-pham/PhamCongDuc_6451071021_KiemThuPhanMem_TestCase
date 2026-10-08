from pages.base_page import BasePage


class HomePage(BasePage):
    """
    HomePage: Dashboard page displayed after successful authentication.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def is_loaded(self):
        """Verify whether user has navigated away from login page."""
        return "/Login" not in self.driver.current_url
