import pytest
import allure
from base.base_test import BaseTest
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage


@allure.epic("UTC Electronic Office System")
@allure.feature("Password Recovery Module (/Login/GetPass)")
class TestForgotPasswordE2E(BaseTest):
    """
    Automated End-to-End Test Suite for Forgot Password Module:
    TC_FP_01 -> TC_FP_08.
    """

    @allure.story("Navigation")
    @allure.title("TC_FP_01: Verify navigation to forgot password page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC_FP_01_navigate_to_forgot_password(self):
        login_page = LoginPage(self.driver).open()
        with allure.step("1. Click on 'Forgot password?' link"):
            forgot_page = login_page.click_forgot_password()
        with allure.step("2. Confirm URL routes to /Login/GetPass"):
            assert "/Login/GetPass" in self.driver.current_url or "/Login/Getpass" in self.driver.current_url
            assert "Lấy lại mật khẩu" in self.driver.title

