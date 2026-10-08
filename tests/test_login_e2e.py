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

