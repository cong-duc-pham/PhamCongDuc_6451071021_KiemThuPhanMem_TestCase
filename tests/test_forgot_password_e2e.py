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

    @allure.story("UI & Elements Rendering")
    @allure.title("TC_FP_08: Verify display of captcha image and university logo")
    @allure.severity(allure.severity_level.NORMAL)
    def test_TC_FP_08_captcha_image_and_logo(self):
        forgot_page = ForgotPasswordPage(self.driver).open()
        with allure.step("1. Verify university logo is displayed"):
            assert forgot_page.is_logo_displayed() is True
        with allure.step("2. Verify Captcha image is displayed with valid source URL"):
            assert forgot_page.is_captcha_image_displayed() is True
            assert "/login/index/captcha" in forgot_page.get_captcha_image_src()

    @allure.story("Form Validation")
    @allure.title("TC_FP_03: Verify reset password fails with invalid captcha")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_TC_FP_03_invalid_captcha(self):
        forgot_page = ForgotPasswordPage(self.driver).open()
        with allure.step("1. Enter incorrect Captcha and valid Email"):
            forgot_page.request_reset(captcha="000000", email="sinhvien01@utc.edu.vn")
        with allure.step("2. Verify Captcha error notification"):
            error_msg = forgot_page.get_error_message()
            allure.attach(error_msg, name="Error Message", attachment_type=allure.attachment_type.TEXT)
            assert "Mã bảo mật không chính xác" in error_msg

