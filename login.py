import random
import string
from playwright.sync_api import Page


class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_button = page.locator("[data-testid='nav-login']").or_(
            page.locator("a.login-link")
        )

    def goto(self):
        self.page.goto("http://144.31.63.127:5000/")

    def click_login_button(self):
        self.login_button.click()
        self.page.wait_for_url("**/login", timeout=10000)


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_input = page.locator("[data-testid='login-username']")
        self.password_input = page.locator("[data-testid='login-password']")
        self.confirm_button = page.locator("[data-testid='login-submit']")
        self.error_message = page.locator("text = Invalid login or password.")

    def wait_for_open(self, timeout: int = 10000):
        self.login_input.wait_for(state="visible", timeout=timeout)

    def login(self, username: str, password: str):
        self.login_input.fill(username)
        self.password_input.fill(password)
        self.confirm_button.click()


def test_invalid_login(page: Page):
    main_page = MainPage(page)
    main_page.goto()

    main_page.click_login_button()

    login_page = LoginPage(page)
    login_page.wait_for_open()

    random_login = "".join(random.choices(string.ascii_lowercase, k=9))
    random_password = "".join(random.choices(string.ascii_lowercase, k=12))
    login_page.login(random_login, random_password)

    assert login_page.error_message.text_content() == "Invalid login or password."
