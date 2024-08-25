import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from multiprocessing import Process, Manager

app = Flask(__name__)

# Construct the path to the chromedriver
# base_dir = os.path.dirname(os.path.abspath(__file__))
# driver_path = os.path.join(base_dir, 'drivers', 'chromedriver.exe')

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the EduPortal API"

@app.route('/results/<username>', methods=['GET'])
def fetch_results_route(username):
    with Manager() as manager:
        summaryObj = manager.dict()
        resObj = manager.dict()

        credits_process = Process(target=fetch_credits, args=(username, summaryObj))
        results_process = Process(target=fetch_results, args=(username, resObj))

        credits_process.start()
        results_process.start()

        credits_process.join()
        results_process.join()

        if "error" in summaryObj or "error" in resObj:
            return jsonify({'error': summaryObj.get("error", resObj.get("error"))}), 500

        return jsonify({
            'registeredCredits': summaryObj.get('registeredCredits', 0),
            'earnedCredits': summaryObj.get('earnedCredits', 0),
            'subjectList': summaryObj.get('subjectList', {}),
            'grades': resObj.get('grades', {})
        })

def fetch_credits(username, summaryObj):
    service = Service("/usr/local/bin/chromedriver")
    url = 'http://results.veltech.edu.in/Stulogin/parentlogin.aspx'

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        search_box = driver.find_element(By.ID, 'txtUserName')
        search_box.send_keys(username)
        search_box.send_keys(Keys.RETURN)

        nav = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'nav')))
        resultsButton = nav.find_element(By.XPATH, "//*[@id='nav']/li[5]")
        resultsButton.click()
        creditsButton = resultsButton.find_element(By.XPATH, "//*[@id='nav']/li[5]/ul/li[6]")
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
        summaryObj["subjectList"] = subjectList
        summaryObj["registeredCredits"] = registeredCredits
        summaryObj["earnedCredits"] = earnedCredits

    except Exception as e:
        summaryObj["error"] = str(e)

    finally:
        driver.quit()
    
def fetch_results(username, resultsObj):
    service = Service("/usr/local/bin/chromedriver")
    url = 'http://results.veltech.edu.in/Stulogin/parentlogin.aspx'

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)

    try:
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
        semWiseSep = {}
        scoreCard = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6}

        for sem in range(1, currentSemester + 1):
            gradeSheet = {}
            if sem == 1:
                creditsTable = driver.find_element(By.ID, 'ContentPlaceHolder1_gvExamResult2013')
            else:
                semButton = driver.find_element(By.ID, "ContentPlaceHolder1_ddlSemester")
                semButton.click()
                selectedSem = semButton.find_element(By.XPATH, f"//*[@id='ContentPlaceHolder1_ddlSemester']/option[{sem}]")
                selectedSem.click()
                creditsTable = driver.find_element(By.ID, 'ContentPlaceHolder1_gvExamResult2013')

            rows = creditsTable.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip the header row

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                row_data = [cell.text for cell in cells]
                course_code = row_data[2]
                grade = row_data[4]
                gradeSheet[course_code] = scoreCard.get(grade, 0)
            semWiseSep[sem] = gradeSheet

        resultsObj["grades"] = semWiseSep

    except Exception as e:
        resultsObj["error"] = str(e)

    finally:
        driver.quit()
        
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=1011)