from selenium import webdriver
from lib import config
import requests
import json
from cache import mongodb
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# boss 爬虫
def run_boss_task():
    search_name = get_category_name()
    driver_path = config.get_config("selenium", "web_driver")
    driver = webdriver.Chrome(driver_path)
    driver.get("https://www.zhipin.com/shenzhen/")
    try:
        # 等待页面搜索input的载入
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="ipt-wrap"]/input'))
        )
        for i in search_name:
            search_input = driver.find_element_by_xpath('//*[@class="ipt-wrap"]/input')
            search_input.clear()
            search_input.send_keys(i)
            driver.find_element_by_xpath('//button[@class="btn btn-search"]').click()

            # 获取数据，数据清洗 =》入库 =》 循环点击下一页
            while True:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@class="ipt-wrap"]/input'))
                )
                extract_params(driver, i)
                try:
                    print("点击-----")
                    href = driver.find_element_by_xpath('//div[@class="page"]/a[@ka="page-next"]').get_attribute("href")
                    if href == "javascript:;":
                        raise Exception("没有下一页了")
                    driver.find_element_by_xpath('//div[@class="page"]/a[@ka="page-next"]').click()
                except Exception as e:
                    print("没有下一页了")
                    break

    except Exception as e:
        print(e)
    finally:
        print("退出操作")
        # driver.quit()


def extract_params(driver, search_name):
    ul = driver.find_elements_by_xpath('//div[@class="job-list"]/ul/li')
    for li in ul:
        # 工作名称
        job_name = li.find_element_by_xpath('.//span[@class="job-name"]').text
        # 工作地点
        job_area = li.find_element_by_xpath(".//span[@class='job-area-wrapper']/span").text
        # 薪资
        salary = li.find_element_by_xpath('.//div[@class="job-limit clearfix"]/span[@class="red"]').text
        # 公司名称
        company = li.find_element_by_xpath('.//div[@class="company-text"]/h3/a').text
        # 学历
        education = li.find_element_by_xpath('.//div[@class="job-limit clearfix"]/p/em').text
        # 经验
        experience = li.find_element_by_xpath('.//div[@class="job-limit clearfix"]/p').text
        # 人数
        # people_num = 0
        try:
            people_num = li.find_element_by_xpath('.//div[@class="company-text"]/p/em[2]').text
        except Exception as e:
            people_num = 0

        tags = li.find_elements_by_xpath('.//div[@class="info-append clearfix"]/div/span')

        tags_tmp = []
        for tags in tags:
            tags_tmp.append(tags.text)
        job_info = {
            "job_name": job_name,
            "job_area": job_area,
            "salary": salary,
            "company": company,
            "education": education,
            "experience": experience,
            "people_num": people_num,
            "tags": tags_tmp,
            "search_name": search_name,
        }
        # 数据入库
        mongodb.insert_info("job_info", job_info)
    return


def get_category_name():
    #
    url = "https://www.zhipin.com/wapi/zpCommon/data/position.json"
    req = requests.get(url)
    if req.status_code != 200:
        raise Exception("获取分类名称有误")
    result = json.loads(req.text)
    req.close()
    search_name = []
    for i in result["zpData"]:
        if i["code"] == 100000:
            for v in i["subLevelModelList"]:
                search_name.append(str(v["name"]))
                for sub in v["subLevelModelList"]:
                    search_name.append(str(sub["name"]))

    print(search_name)
    return search_name


