from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.forgot_password_page import ForgotPasswordPage


class LoginPage(BasePage):
    """
    Page Object: LoginPage representing the UTC electronic office login form.
    - Encapsulates private locators for all UI elements.
    - Provides high-level business interaction methods returning next Page Objects.
    """

    URL = "https://vanphongdientu.utc.edu.vn/Login"

    # Private element locators
    _username_field = (By.NAME, "username")
    _password_field = (By.NAME, "userpwd")
    _login_button = (By.CSS_SELECTOR, "input.submit_login")

    # Persistent session checkbox and overlay label
    _persistent_checkbox = (By.ID, "persistent")
    _persistent_fake_box = (By.CSS_SELECTOR, "label.check")

    # SSO button and Forgot Password navigation link
    _google_sso_button = (By.XPATH, "//a[contains(text(),'e-mail UTC')]")
    _forgot_password_link = (By.CSS_SELECTOR, "a[href='/Login/GetPass']")

    # Validation banner and footer elements
    _error_message = (By.CSS_SELECTOR, "div.error")
    _banner_h1 = (By.CSS_SELECTOR, ".caption h1")
    _banner_span = (By.CSS_SELECTOR, ".caption span")
    _help_link = (By.XPATH, "//a[contains(text(), 'Trung tâm trợ giúp')]")
    _feedback_link = (By.XPATH, "//a[contains(text(), 'Ý kiến phản hồi')]")
    _copyright = (By.CSS_SELECTOR, ".footer .left span.a")

    # Public aliases for UI existence assertions
    LOC_USERNAME = _username_field
    LOC_PASSWORD = _password_field
    LOC_SUBMIT_BTN = _login_button
    LOC_PERSISTENT_CHECKBOX = _persistent_checkbox
    LOC_GOOGLE_SSO = _google_sso_button
    LOC_FORGOT_PASS = _forgot_password_link
    LOC_ERROR_MSG = _error_message

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Navigate to Login URL and return self."""
        self.driver.get(self.URL)
        return self

    def login_as(self, username, password):
        """
        Authenticate with given credentials and return HomePage instance.
        Follows Fluent Navigation pattern.
        """
        if username:
            self.type(self._username_field, username)
        if password:
            self.type(self._password_field, password)
        self.click(self._login_button)
        return HomePage(self.driver)

    def submit_by_enter(self, username, password):
        """Submit login form by pressing the Enter keyboard key."""
        from selenium.webdriver.common.keys import Keys
        if username:
            self.type(self._username_field, username)
        if password:
            self.type(self._password_field, password)
            self.driver.find_element(*self._password_field).send_keys(Keys.ENTER)
        else:
            self.driver.find_element(*self._username_field).send_keys(Keys.ENTER)
        return HomePage(self.driver)

    def login(self, username, password, keep_signed_in=False):
        """Convenience alias for login_as()."""
        if keep_signed_in:
            self.toggle_remember_me()
        return self.login_as(username, password)

    def is_on_login_page(self):
        """Check whether browser is currently on Login URL."""
        return "/Login" in self.driver.current_url

    def get_error_message(self, timeout=7):
        """Retrieve displayed error message with Explicit Wait."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self._error_message)
            )
            return el.text.strip()
        except Exception:
            return ""

    def toggle_remember_me(self, target_state=None):
        """Toggle 'Keep me logged in' persistent session checkbox."""
        checkbox = self.driver.find_element(*self._persistent_checkbox)
        fake_box = self.driver.find_element(*self._persistent_fake_box)
        current = checkbox.is_selected()
        if target_state is None or current != target_state:
            fake_box.click()
        return self

    def toggle_persistent(self, target_state=None):
        return self.toggle_remember_me(target_state)

    def is_remember_me_checked(self):
        checkbox = self.driver.find_element(*self._persistent_checkbox)
        return checkbox.is_selected()

    def is_persistent_checked(self):
        return self.is_remember_me_checked()

    def click_forgot_password(self):
        self.click(self._forgot_password_link)
        return ForgotPasswordPage(self.driver)

    def is_password_field_masked(self):
        return self.get_attribute(self._password_field, "type") == "password"

    def is_password_masked(self):
        return self.is_password_field_masked()

    def get_google_sso_href(self):
        return self.get_attribute(self._google_sso_button, "href")

    def click_google_sso(self):
        self.click(self._google_sso_button)
        return self

    def click_login(self):
        self.click(self._login_button)
        return self

    def get_banner_title(self):
        return self.get_text(self._banner_h1)

    def get_banner_subtitle(self):
        return self.get_text(self._banner_span)

    def get_help_link_href(self):
        return self.get_attribute(self._help_link, "href")

    def get_help_link_target(self):
        return self.get_attribute(self._help_link, "target")

    def get_feedback_link_href(self):
        return self.get_attribute(self._feedback_link, "href")

    def get_copyright_text(self):
        return self.get_text(self._copyright)
