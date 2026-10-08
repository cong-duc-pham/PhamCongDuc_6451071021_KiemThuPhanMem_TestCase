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

