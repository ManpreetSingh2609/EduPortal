from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import threading
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)

@app.route('/credits_summary/<username>', methods=['GET'])
def fetch_credits_summary(username, service= Service('chromedriver.exe') , url=os.getenv("URL")):
    summaryObj={};
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service,options=options)
        driver.get(url)
        search_box = driver.find_element(By.ID, 'txtUserName')
        search_box.send_keys(username)
        search_box.send_keys(Keys.RETURN)
        nav = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'nav')))
        resultsButton = nav.find_element(By.XPATH, "//*[@id='nav']/li[5]")
        resultsButton.click()
        creditsButton = resultsButton.find_element(By.XPATH, "//ul/li[6]")
        link = WebDriverWait(creditsButton, 60).until(EC.element_to_be_clickable((By.TAG_NAME, 'a')))
        link.click()
        creditsTable = driver.find_element(By.ID, 'ContentPlaceHolder1_gvCredits')
        rows = creditsTable.find_elements(By.TAG_NAME, 'tr')
        subjectList = {}
        registeredCredits = 0
        earnedCredits = 0
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) == 4:
                row_data = [cell.text for cell in cells]
                data = {
                    "Courses Name": row_data[1],
                    'Credit': int(row_data[-2]),
                    'Earned': int(row_data[-1])
                }
                registeredCredits += data['Credit']
                earnedCredits += data['Earned']
                subjectList[row_data[0]] = data
        summaryObj["subjectList"] : subjectList
        summaryObj["registeredCredits"] : registeredCredits
        summaryObj["earnedCredits"] : earnedCredits
        return(summaryObj)

    finally:
        driver.quit()


@app.route('/results/<username>', methods=['GET'])
def fetch_results(username, service= Service('chromedriver.exe') , url=os.getenv("URL")):
    resultsObj={};
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
    
        search_box = driver.find_element(By.ID, 'txtUserName')
        search_box.send_keys(username)
        search_box.send_keys(Keys.RETURN)
    
        currentSemester = int(driver.find_element(By.XPATH, '//*[@id="divlogin-table"]/table[1]/tbody/tr[7]/td[2]').text)
        
        nav = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'nav')))
        resultsButton = nav.find_element(By.XPATH, "//*[@id='nav']/li[5]")
        resultsButton.click()
        results = resultsButton.find_element(By.XPATH, "//*[@id='nav']/li[5]/ul/li[1]")
        link = WebDriverWait(results, 60).until(EC.element_to_be_clickable((By.TAG_NAME, 'a')))
        link.click()
    
        gradeSheet = {}
        scoreCard = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6}
    
        for sem in range(1, currentSemester + 1):
            if sem == 1:
                creditsTable = driver.find_element(By.ID, 'ContentPlaceHolder1_gvExamResult2013')
                rows = creditsTable.find_elements(By.TAG_NAME, 'tr')
                rows.pop(0)
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    row_data = [cell.text for cell in cells]
                    gradeSheet[row_data[2]] = scoreCard[row_data[4]] if row_data[4] in scoreCard else 0
            else:
                semButton = driver.find_element(By.ID, "ContentPlaceHolder1_ddlSemester")
                semButton.click()
                selectedSem = semButton.find_element(By.XPATH, f"//*[@id='ContentPlaceHolder1_ddlSemester']/option[{sem}]")
                selectedSem.click()
                creditsTable = driver.find_element(By.ID, 'ContentPlaceHolder1_gvExamResult2013')
                rows = creditsTable.find_elements(By.TAG_NAME, 'tr')
                rows.pop(0)
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    row_data = [cell.text for cell in cells]
                    gradeSheet[row_data[2]] = scoreCard[row_data[4]] if row_data[4] in scoreCard else 0
        
        resultsObj["grades"] = gradeSheet
        return(resultsObj)
    finally:
        driver.quit()

# @app.route('/credits_summary/<username>', methods=['GET'])
# def credits_summary(username):
#     result = {"summary" : {} }
#     url = os.getenv("URL")
#     service = Service('chromedriver.exe')
#     thread = threading.Thread(target=fetch_credits_summary, args=(username, result, url, service))
#     thread.start()
#     thread.join()
#     return jsonify(result["summary"])

# @app.route('/results/<username>', methods=['GET'])
# def results(username):
#     result = {'grades': {} }
#     url = os.getenv("URL")
#     service = Service('chromedriver.exe')
#     thread = threading.Thread(target=fetch_results, args=(username, result, url, service ))
#     thread.start()
#     thread.join()
#     return jsonify(result["grades"])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port= 1011)
