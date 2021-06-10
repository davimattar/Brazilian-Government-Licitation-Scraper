#%%
# This a training code scraper with studies porposese, using scrapy lib. The tutorial used https://oxylabs.io/blog/python-web-scraping
# We are going to scrape some brazilian government licitation from http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Filtro.asp
# You can find some documentation on http://compras.dados.gov.br/licitacoes/v1/licitacoes.html?

# You need to install the right version of ChromeDriver according to your current browser. Link: https://chromedriver.chromium.org/downloads

# Importing libraries.

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#%%
# Defining the objects where our data is going to be saved.
title_licitation = []
content_licitation = []

# Insert the web address where the data is storaged inside the url object.
url = "http://comprasnet.gov.br/ConsultaLicitacoes/ConsLicitacao_Filtro.asp"

# Starting the webdriver. Insert the correct path to the executable chromedriver file installed in your pc.
driver = webdriver.Chrome(executable_path="c:\windows\webdriver\chromedriver.exe")

# Passing to the webdriver the defined url.
driver.get(url)

# The list_publ_ini is an object where we insert the pairs of initial date and ending date of our licitation search.
# Its a dictionary. You can change the dates according to your desire and right now it is set from 01/01/2021 to 30/04/2021.
list_publ_ini = {"01012021":"15012021","16012021":"31012021","01022021":"15022021","16022021":"28022021","01032021":"15032021","16032021":"31032021","01042021":"15042021","16042021":"30042021"}

#%%

# FOR LOOP
# This is a loop where all the magic happens.
# First we are cleaning all information from the search form because it will work as a loop passing the dates pairs one by one.
# If we do not clean it first, all the old searching arguments will be displayed there.
# It was made like that because the government website just allows us to search with the maximum gap of 15 days.
# The second xpath argument is the initial date imputation.
# The third xpath argument is the final date imputation, passed as the key from our dictionary.
# The forth xpath argument is the selection of all licitation modalities. If you are interested in just a specific modality, just change the xpath here.
# The last xpath argument is the final click to initialize the licitation search.

# WHILE INSIDE THE FOR
# Using BeautifulSoup we can handle the HTML.
# In the first for loop we are looking after the title of the licitation.
# In the second for loop we are looking after all the content from that licitation.
# The try argument is checking if there is more results listed on another page looking for the "Próximo" buttom.
# The government website only display 10 licitation at once.
# The except argument will be actioned when there is not a "Próximo" buttom and will click on the "Nova Pesquisa" buttom to initialize a new search.

for key in list_publ_ini:

    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Limpar']"))).click()
    driver.find_element_by_xpath("//input[@name='dt_publ_ini']").send_keys(key)
    driver.find_element_by_xpath("//input[@name='dt_publ_fim']").send_keys(list_publ_ini[key])
    driver.find_element_by_xpath("//input[@name='chkTodos']").click()
    driver.find_element_by_xpath("//input[@name='ok']").click()

    while True:
        content = driver.page_source
        soup = BeautifulSoup(content, features="lxml")

        for a in soup.findAll(attrs={'class':'td_titulo_campo', 'align':'center'}):
            title_licitation.append(a.text.strip())

        for b in soup.findAll(attrs={'style':'padding:10px'}):
            content_licitation.append(b.text.strip())

        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='btn_proximo']"))).click()
        except:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='Pesquisa']"))).click()
            break
driver.quit()

# Now we have to clean the database saved in futures code updates.