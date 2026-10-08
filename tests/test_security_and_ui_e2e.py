import pytest
import allure
from selenium.common.exceptions import UnexpectedAlertPresentException
from base.base_test import BaseTest
from pages.login_page import LoginPage


@allure.epic("UTC Electronic Office System")
@allure.feature("Security & UI Verification")
class TestSecurityAndUiE2E(BaseTest):
    """
    Automated End-to-End Test Suite for Security & UI Modules:
    TC_SEC_01 -> TC_SEC_06 and TC_UI_01 -> TC_UI_03.
    """

    @allure.story("Security - SQL Injection Prevention")
    @allure.title("TC_SEC_01: Verify SQL injection prevention on username field")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_TC_SEC_01_sql_injection_in_username(self):
        login_page = LoginPage(self.driver).open()
        sqli_payload = "' OR '1'='1' --"

        with allure.step(f"1. Input SQL injection payload: {sqli_payload}"):
            login_page.login_as(sqli_payload, "password123")

        with allure.step("2. Confirm no raw database error leak and access is rejected"):
            page_content = self.driver.page_source.lower()
            assert "sql syntax" not in page_content
            assert "database error" not in page_content
            assert "Tài khoản hoặc mật khẩu không đúng." in login_page.get_error_message()

    @allure.story("Security - SQL Injection Prevention")
    @allure.title("TC_SEC_02: Verify SQL injection prevention on password field")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_TC_SEC_02_sql_injection_in_password(self):
        login_page = LoginPage(self.driver).open()
        sqli_payload = "' OR '1'='1"

        with allure.step(f"1. Input SQL injection payload in password: {sqli_payload}"):
            login_page.login_as("admin", sqli_payload)

        with allure.step("2. Confirm system handles input securely"):
            assert "Tài khoản hoặc mật khẩu không đúng." in login_page.get_error_message()

    @allure.story("Security - Cross-Site Scripting (XSS)")
    @allure.title("TC_SEC_03: Verify cross-site scripting XSS prevention")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC_SEC_03_xss_protection(self):
        login_page = LoginPage(self.driver).open()
        xss_payload = "<script>alert('XSS_ATTACK')</script>"

        with allure.step(f"1. Inject script payload into form: {xss_payload}"):
            login_page.login_as(xss_payload, "password123")

        with allure.step("2. Confirm script is not executed as browser alert dialog"):
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.dismiss()
                pytest.fail(f"XSS vulnerability detected! Alert dialog was executed: {alert_text}")
            except UnexpectedAlertPresentException:
                pytest.fail("Unexpected XSS alert detected!")
            except Exception:
                # No alert was triggered => Secure
                assert True

    @allure.story("Security - Session Access Control")
    @allure.title("TC_SEC_05: Verify unauthorized direct access prevention to internal url")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC_SEC_05_auth_guard_redirect(self):
        with allure.step("1. Navigate directly to root internal URL"):
            self.driver.get("https://vanphongdientu.utc.edu.vn/")

        with allure.step("2. Confirm system automatically redirects to /Login"):
            assert "/Login" in self.driver.current_url

    @allure.story("Security - Transport Layer Security")
    @allure.title("TC_SEC_06: Verify HTTPS protocol and secure connection")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_SEC_06_https_security(self):
        with allure.step("1. Verify website enforces HTTPS protocol"):
            self.driver.get("https://vanphongdientu.utc.edu.vn/Login")
            assert self.driver.current_url.startswith("https://")

    @allure.story("User Interface (UI)")
    @allure.title("TC_UI_01: Verify ui banner slogan and footer copyright display")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_UI_01_banner_slogan_and_copyright(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Check primary banner header and subtitle"):
            assert "Không chỉ là một giải pháp quản lý" in login_page.get_banner_title()
            assert "Làm việc mọi lúc mọi nơi" in login_page.get_banner_subtitle()
        with allure.step("2. Check footer copyright text"):
            assert "Trường ĐH Giao Thông Vận Tải" in login_page.get_copyright_text()

    @allure.story("User Interface (UI)")
    @allure.title("TC_UI_02: Verify help center link opens in new tab")
    @allure.severity(allure.severity_level.MINOR)
    def test_TC_UI_02_help_center_link(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Verify help center href and target attributes"):
            assert "hotrokythuat.utc.edu.vn" in login_page.get_help_link_href()
            assert login_page.get_help_link_target() == "_blank"

