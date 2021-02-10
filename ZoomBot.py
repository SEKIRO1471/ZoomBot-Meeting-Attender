from selenium.webdriver import Chrome
from chromedriver_autoinstaller import install  # This module will automatically download chromedriver.exe
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self):
        self.headless = False
        options = Options()
        options.headless = self.headless  # To make browser visible set it to False
        path = install()  # Path of the chromedriver.exe
        self.driver = Chrome(executable_path=path, options=options)

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

    def join_via_pass_id(self):
        self.meeting_id = input("Enter Meeting ID: ")
        self.meeting_password = input("Enter Meeting Password: ")
        self.driver.get("https://zoom.us/wc/join/" + self.meeting_id)
        self.meeting_id_in()
        self.meeting_password_in()
        print("Done!")
        while True:
            pass

    def join_via_link(self, link_src):
        self.driver.get(link_src)
        self.join_btn_clicker()


class GmailLogin:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://zoom.us/signin")
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


class WhatsappGetLink:
    def __init__(self, driver):
        self.driver = driver
        self.group_name = input('Enter whatsapp group/contact name: ')
        self.driver.get(r'https://web.whatsapp.com/')
        sleep(10)
        self.open_links()
        self.find_link()

    def open_links(self):
        group = self.driver.find_element_by_xpath(r'//*[@title="' + self.group_name + '"]')
        group.click()
        sleep(0.5)
        menu_bar = self.driver.find_element_by_xpath(r'//header/div/div/div/*[@title="' + self.group_name + '"]')
        menu_bar.click()
        sleep(0.5)
        group_data = self.driver.find_elements_by_xpath(r'//*[@data-testid="chevron-right-alt"]')[0]
        group_data.click()
        sleep(0.5)
        links_tab = self.driver.find_element_by_xpath(r'//*[@title="Links"]')
        links_tab.click()
        sleep(5)

    def find_link(self):
        date = input('Enter date in d/mm/yyyy: ')
        found = False
        while not found:
            try:
                links = self.driver.find_elements_by_xpath(
                    r'//*[contains(@data-pre-plain-text, "' + date + '")]//*[@title="Join our '
                    r'Cloud HD Video Meeting"]')
                try:
                    self.link = links[0]
                except IndexError:
                    continue
                found = True
            except NoSuchElementException:
                pass

    def get_link(self):
        self.link.click()
        sleep(5)

        self.driver.switch_to.window(self.driver.window_handles[-1])
        url = self.driver.current_url
        url = url.replace('/j/', '/wc/join/')
        return url


if __name__ == '__main__':
    browser = Browser()
    print("Welcome to Meeting Attender\n")

    method = input("Do you want join via Link or Id?\n").lower()

    if method == 'link':
        print("Select a link source from the following:")
        link_getter = {'Whatsapp': WhatsappGetLink}

        for key in link_getter.keys():
            print(key)

        choice = input("Enter Choice: ").capitalize()
        src = link_getter[choice](browser.driver)
        link = src.get_link()

    print("Select a login method from the following:")
    login_methods = {'Gmail': GmailLogin}

    for key in login_methods.keys():
        print(key)

    choice = input("Enter Choice: ").capitalize()
    if method == 'link':
        login_methods[choice](browser.driver)
        browser.join_via_link(link)
    elif method == 'id':
        login_methods[choice](browser.driver)
        browser.join_via_pass_id()
