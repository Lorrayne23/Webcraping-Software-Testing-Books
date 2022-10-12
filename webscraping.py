import pdfkit
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



class Crawler_ANAC:
    def __init__(self):
        self.browser = self.define_browser()
        self.list_titles = []
        self.list_references = []

    def save_directory(self):
        # change chrome settings about file save location, adding the path of the directory
        options = webdriver.ChromeOptions()
        #options.add_argument("download.default_directory=C:/web-crawler") # Set the download Path
        path = os.getcwd()
        print(os.getcwd())
        prefs = {"download.default_directory": path}
        options.add_experimental_option("prefs", prefs)
        #options.add_argument("--headless")
        return options


    def define_browser(self):
        #defines the url to which the crawler will be performed
        #browser = webdriver.Remote("http://selenium:4444/wd/hub",options=self.save_directory(),desired_capabilities=DesiredCapabilities.CHROME)
        browser = webdriver.Chrome(ChromeDriverManager().install(),options=self.save_directory(),desired_capabilities=DesiredCapabilities.CHROME)
        browser.get("http://portal.pucminas.br/biblioteca/index_padrao.php?_ga=2.173431267.175448131.1665336537-1104017533.1641577896")
        browser.save_screenshot('screenshot.png')
        return browser


    def define_search(self):
        # defines the theme of the search
        search = self.browser.find_element(By.ID, "searchboxholdingsid")
        search.send_keys("Teste de Software")
        self.browser.save_screenshot('screenshot3.png')
        sleep(2)


    def click_button(self):
        # click in the button of next page
        window_before = self.browser.window_handles[0]
        sleep(5)
        # defines timezone in the field
        click_button = self.browser.find_element(By.CSS_SELECTOR, 'button.botao-padrao').click()
        self.window_handle()


    def window_handle(self):
        # changes the main url in use
        window_after = self.browser.window_handles[1]
        new_windown = self.browser.switch_to.window(window_after)
        self.browser.implicitly_wait(20)
        print(self.browser.current_url)



    def collect_content(self):
        # save the elements title and reference of the books in separate  list's

        for element in self.browser.find_elements(By.XPATH,'//a[@class="title-link color-p4"]'):
            sleep(2)
            title = str(element.get_attribute('title'))
            self.list_titles.append(title)

        for ref in self.browser.find_elements(By.CLASS_NAME,'display-info'):
            self.list_references.append(ref.text)

        #print(len(self.list_titles))
        #print(len(self.list_references))

    def page_2(self):
        # goes for page 2
        window_before = self.browser.window_handles[0]
        click_button = self.browser.find_element(By.ID, 'ctl00_ctl00_MainContentArea_MainContentArea_bottomMultiPage_rptPageLinks_ctl01_lnkPageLink').click()
        self.window_handle()

    def page_3(self):
        # goes for page 3
        window_before = self.browser.window_handles[0]
        click_button = self.browser.find_element(By.ID, 'ctl00_ctl00_MainContentArea_MainContentArea_bottomMultiPage_rptPageLinks_ctl02_lnkPageLink').click()
        self.window_handle()

    def page_4(self):
        # goes for page 4
        window_before = self.browser.window_handles[0]
        click_button = self.browser.find_element(By.ID,'ctl00_ctl00_MainContentArea_MainContentArea_bottomMultiPage_rptPageLinks_ctl03_lnkPageLink').click()
        self.window_handle()

    def page_5(self):
        # goes for page 5
        window_before = self.browser.window_handles[0]
        click_button = self.browser.find_element(By.ID,'ctl00_ctl00_MainContentArea_MainContentArea_bottomMultiPage_rptPageLinks_ctl04_lnkPageLink').click()
        self.window_handle()

    def creating_data_frame(self):
        # creates a data frame to join the two lists
        data = {
            'Title': [],
            'Reference': []
        }
        dataframe = pd.DataFrame(data)
        dataframe['Title'] = self.list_titles
        dataframe['Reference'] = self.list_references
        return dataframe

    def convert_df_to_pdf(self):
        # convert the dataframe in to a pdf file
        f = open('books_software_test.html', 'w')
        a = self.creating_data_frame().to_html()
        f.write(a)
        f.close()
        pdfkit.from_file('books_software_test.html', 'books_software_test.pdf')



if __name__ == "__main__":
    crawler = Crawler_ANAC()
    crawler.define_search()
    crawler.click_button()
    crawler.collect_content()
    crawler.page_2()
    crawler.collect_content()
    crawler.page_3()
    crawler.collect_content()
    crawler.page_4()
    crawler.collect_content()
    crawler.page_5()
    crawler.collect_content()
    crawler.creating_data_frame()
    crawler.convert_df_to_pdf()


