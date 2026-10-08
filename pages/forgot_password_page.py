from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    """
    Page Object: ForgotPasswordPage representing password reset form (/Login/GetPass).
    """

    URL = "https://vanphongdientu.utc.edu.vn/Login/GetPass"

    # Private element locators
    _captcha_field = (By.NAME, "captcha")
    _email_field = (By.NAME, "email")
    _submit_button = (By.CSS_SELECTOR, "input[type='submit']")
    _captcha_image = (By.CSS_SELECTOR, "form img")
    _back_to_login_link = (By.CSS_SELECTOR, ".helps a")
    _error_message = (By.CSS_SELECTOR, "div.error")
    _logo = (By.CSS_SELECTOR, "#logo img.logo")

    # Public locators for test assertions
    LOC_CAPTCHA_IMG = _captcha_image
    LOC_CAPTCHA_INPUT = _captcha_field
    LOC_EMAIL_INPUT = _email_field
    LOC_SUBMIT_BTN = _submit_button
    LOC_BACK_TO_LOGIN = _back_to_login_link
    LOC_ERROR_MSG = _error_message
    LOC_LOGO = _logo

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.driver.get(self.URL)
        return self

    def request_reset(self, captcha="", email=""):
        if captcha:
            self.type(self._captcha_field, captcha)
        if email:
            self.type(self._email_field, email)
        self.click(self._submit_button)
        return self

    def click_submit(self):
        self.click(self._submit_button)
        return self

    def get_error_message(self, timeout=7):
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            el = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self._error_message)
            )
            return el.text.strip()
        except Exception:
            return ""

    def is_captcha_image_displayed(self):
        return self.is_element_present(self._captcha_image)

    def get_captcha_image_src(self):
        return self.get_attribute(self._captcha_image, "src")

    def is_logo_displayed(self):
        return self.is_element_present(self._logo)

    def click_back_to_login(self):
        from pages.login_page import LoginPage
        self.click(self._back_to_login_link)
        return LoginPage(self.driver)
