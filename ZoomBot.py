from selenium.webdriver import Chrome
from chromedriver_autoinstaller import install  # This module will automatically download chromedriver.exe
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self):
        self.meeting_id = input("Enter Meeting ID: ")
        self.meeting_password = input("Enter Meeting Password: ")
        self.headless = False
        options = Options()
        options.headless = self.headless  # To make browser visible set it to False
        path = install()  # Path of the chromedriver.exe
        self.driver = Chrome(executable_path=path, options=options)
        self.driver.get("https://zoom.us/signin")

    def join_btn_clicker(self):
        join_btn = self.driver.find_element_by_xpath("""//*[@id="joinBtn"]""")
        join_btn.click()

    def meeting_id_in(self):
        id_join = True
        while id_join:
            try:
                self.join_btn_clicker()
                id_join = False
            except NoSuchElementException:
                pass
        sleep(2)

    def meeting_password_in(self):
        password_box = self.driver.find_element_by_xpath('''//*[@type="password"]''')
        password_box.send_keys(self.meeting_password)
        pass_join = True
        while pass_join:
            try:
                self.join_btn_clicker()
                pass_join = False
            except NoSuchElementException:
                pass

    def join_meeting(self):
        self.driver.get("https://zoom.us/wc/join/" + self.meeting_id)
        self.meeting_id_in()
        self.meeting_password_in()
        print("Done!")
        while True:
            pass


class GmailLogin(Browser):
    def __init__(self):
        super().__init__()
        print("Provide your Gmail Credentials:")
        self.gmail_id = input("Enter Email Id: ")
        self.gmail_password = input("Enter password: ")
        self.driver.find_element_by_xpath('''//*[@id="login"]/div/div[3]/div/div[4]/a[2]''').click()
        self.gmail_login()

    # Login via Gmail
    def gmail_login(self):
        email_box = self.driver.find_element_by_xpath('''//*[@type="email"]''')
        email_box.send_keys(self.gmail_id)  # Your Gmail Email-id for login
        self.driver.find_element_by_xpath('''//*[@id="identifierNext"]''').click()  # Next button
        sleep(3)
        password_box = self.driver.find_element_by_xpath('''//*[@type="password"]''')
        password_box.send_keys(self.gmail_password)  # Your Gmail Password for login
        self.driver.find_element_by_xpath('''//*[@id="passwordNext"]''').click()  # Next button
        print("Please confirm it's you...")
        sleep(40)


if __name__ == '__main__':
    login_methods = {'Gmail': GmailLogin}
    print("Welcome to Meeting Attender")
    print("Select a login method from the following:")

    for key in login_methods.keys():
        print(key)

    choice = input("Enter Choice: ").capitalize()
    login_methods[choice]().join_meeting()
