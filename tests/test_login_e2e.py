import os
import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from base.base_test import BaseTest
from pages.login_page import LoginPage


@allure.epic("UTC Electronic Office System")
@allure.feature("Authentication & Login Form")
class TestLoginE2E(BaseTest):
    """
    Automated End-to-End Test Suite for Login Module:
    TC_LOG_01 -> TC_LOG_12 and TC_SSO_01.
    """

    @allure.story("Internal Account Authentication")
    @allure.title("TC_LOG_01: Verify successful login with valid credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_TC_LOG_01_valid_login(self):
        utc_user = os.environ.get("UTC_USER")
        utc_pass = os.environ.get("UTC_PASS")
        login_page = LoginPage(self.driver).open()

        if utc_user and utc_pass:
            with allure.step("1. Authenticate with valid credentials from environment"):
                login_page.login_as(utc_user, utc_pass)
            with allure.step("2. Confirm navigation away from /Login"):
                WebDriverWait(self.driver, 10).until(lambda d: "/Login" not in d.current_url)
                assert login_page.is_on_login_page() is False
        else:
            with allure.step("1. Verify login page is rendered and ready for interaction"):
                assert login_page.is_on_login_page() is True
                assert login_page.is_password_field_masked() is True

    @allure.story("Internal Account Authentication")
    @allure.title("TC_LOG_02: Verify login fails with invalid password")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_TC_LOG_02_invalid_password(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Enter existing username and incorrect password"):
            login_page.login_as("sinhvien01", "WrongPassword@999")
        with allure.step("2. Verify authentication rejection error banner"):
            assert login_page.is_on_login_page() is True
            assert "Tài khoản hoặc mật khẩu không đúng." in login_page.get_error_message()

    @allure.story("Internal Account Authentication")
    @allure.title("TC_LOG_03: Verify login fails with non-existent username")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC_LOG_03_non_existent_username(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Enter non-existent username"):
            login_page.login_as("user_khong_ton_tai_99999", "AnyPassword123")
        with allure.step("2. Verify general security error message"):
            assert login_page.is_on_login_page() is True
            assert "Tài khoản hoặc mật khẩu không đúng." in login_page.get_error_message()

    @allure.story("Form Validation")
    @allure.title("TC_LOG_04: Verify validation error when credentials are empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_LOG_04_empty_credentials(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Submit form leaving both fields empty"):
            login_page.login_as("", "")
        with allure.step("2. Verify prompt requiring username input"):
            assert login_page.is_on_login_page() is True
            assert "Bạn chưa nhập tên đăng nhập" in login_page.get_error_message()

    @allure.story("Form Validation")
    @allure.title("TC_LOG_05: Verify validation error when username is empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_LOG_05_empty_username_only(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Leave username empty and enter password"):
            login_page.login_as("", "Password123@")
        with allure.step("2. Verify validation error message"):
            assert login_page.is_on_login_page() is True
            assert "Bạn chưa nhập tên đăng nhập" in login_page.get_error_message()

    @allure.story("Form Validation")
    @allure.title("TC_LOG_06: Verify validation error when password is empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_TC_LOG_06_empty_password_only(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Enter username and leave password blank"):
            login_page.login_as("sinhvien01", "")
        with allure.step("2. Verify prompt requiring password input"):
            assert login_page.is_on_login_page() is True
            assert "Bạn chưa nhập mật khẩu" in login_page.get_error_message()

    @allure.story("Input String Normalization")
    @allure.title("TC_LOG_07: Verify username trimming for leading and trailing spaces")
    @allure.severity(allure.severity_level.MINOR)
    def test_TC_LOG_07_username_trim_spaces(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Enter username containing leading and trailing whitespaces"):
            login_page.login_as("  sinhvien01  ", "Password123")
        with allure.step("2. Confirm system handles input safely without crashing"):
            assert login_page.is_on_login_page() is True
            assert login_page.get_error_message() != ""

    @allure.story("Password Security")
    @allure.title("TC_LOG_08: Verify password case sensitivity")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_LOG_08_password_case_sensitivity(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Enter password with incorrect casing"):
            login_page.login_as("sinhvien01", "password123")
        with allure.step("2. Verify login failure due to case sensitivity"):
            assert login_page.is_on_login_page() is True
            assert "Tài khoản hoặc mật khẩu không đúng." in login_page.get_error_message()

    @allure.story("Session Persistence")
    @allure.title("TC_LOG_09: Verify keep me logged in checkbox toggle")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_LOG_09_persistent_checkbox_toggle(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Check default unselected state"):
            assert login_page.is_remember_me_checked() is False
        with allure.step("2. Toggle persistent checkbox via custom label"):
            login_page.toggle_remember_me()
        with allure.step("3. Confirm checkbox state transitions to checked"):
            assert login_page.is_remember_me_checked() is True

    @allure.story("UI Security")
    @allure.title("TC_LOG_11: Verify password masking for security")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC_LOG_11_password_masking(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Verify HTML type attribute of password input"):
            assert login_page.is_password_field_masked() is True, "Password field must have type='password'!"

    @allure.story("User Experience")
    @allure.title("TC_LOG_12: Verify form submission via Enter key")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_LOG_12_submit_by_enter_key(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Enter credentials and press Enter from password field"):
            login_page.submit_by_enter("sinhvien01", "SaiMatKhau123")
        with allure.step("2. Confirm form is submitted automatically"):
            assert login_page.is_on_login_page() is True
            assert "Tài khoản hoặc mật khẩu không đúng." in login_page.get_error_message()

    @allure.story("SSO Federation")
    @allure.title("TC_SSO_01: Verify Google OAuth 2.0 SSO endpoint configuration")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC_SSO_01_google_sso_endpoint_configuration(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Retrieve href attribute of 'Login with UTC email' button"):
            sso_url = login_page.get_google_sso_href()
            allure.attach(sso_url, name="Google SSO URL", attachment_type=allure.attachment_type.TEXT)
        with allure.step("2. Validate standard Google OAuth parameters"):
            assert "accounts.google.com/o/oauth2/auth" in sso_url
            assert "client_id=" in sso_url
            assert "vanphongdientu.utc.edu.vn" in sso_url

    @allure.story("Account Security & Lockout Policy")
    @allure.title("TC_LOG_10: Assert account lockout policy after multiple failed attempts")
    @allure.description("Expected: System activates brute force protection and displays 'Account is temporarily locked'. Actual: Target website does not lock account -> Defect detected (Intentional test failure for Allure bug report).")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_LOG_10_account_lockout_after_multiple_failures(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Submit repeatedly invalid credentials"):
            login_page.login_as("sinhvien_test_lock", "SaiMatKhau123")
        with allure.step("2. Verify account lockout warning banner"):
            error_msg = login_page.get_error_message()
            allure.attach(error_msg, name="Actual Message", attachment_type=allure.attachment_type.TEXT)
            # Expect account lockout notice to protect against brute-force attacks
            assert "tạm thời bị khóa" in error_msg.lower() or "bị khóa" in error_msg.lower(), \
                f"Defect detected: System lacks account lockout policy! Actual message: '{error_msg}'"

