import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome WebDriver 경로 설정
# ...

def crawling_notebook_info():
# WebDriver 인스턴스 생성
driver = webdriver.Chrome()

# 웹 페이지 로드 대기 시간 (초)
wait_time = 5
wait = WebDriverWait(driver, wait_time)

# 사이트 접속
url = "https://prod.danawa.com/list/?cate=112758"
driver.get(url)

lst_name = []
lst_title = []
lst_price = []
lst_a3 = []
lst_spec = []

try:

    """
    셀레니움 크롤링을 위한 노트북 다나와 값 세팅
    """
    result_list = []

    # 페이지 요청
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    # select.qnt_selector 클릭하여 option 태그의 value="90" 선택
    select_selector = "select.qnt_selector"
    select_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, select_selector)))
    select_element.click()

    option_selector = 'option[value="90"]'
    option_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, option_selector)))
    option_element.click()

    time.sleep(2)

    for page_num in range(2, 12):
        # 페이지 HTML 파싱
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 10 페이지 데이터도 뽑기 위한 예외처리
        if page_num == 11:
            selector = f'a[onclick="javascript:movePage({page_num}); return false;"]'

            # a 태그 클릭
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            element.click()
            # 2초 대기
            time.sleep(2)

            # 페이지 이동 확인
            current_url = f"javascript:movePage({page_num})"
            print("다음 페이지로 이동:", current_url)

            # div.main_ad_prodlist 요소 제외하고 크롤링 (광고 부분 제거)
        target_elements = soup.find_all('div', class_='main_ad_prodlist')  # 제외할 요소 선택
        for element in target_elements:
            element.decompose()  # 요소 제거

        prod_main_info_divs = soup.select('div.prod_main_info')
        # div.prod_main_info 요소를 반복하여 처리
        for prod_main_info_div in prod_main_info_divs:

            # a 태그 중 name 속성이 "productName"인 요소를 찾습니다.
            title = prod_main_info_div.find("a", attrs={"name": "productName"})

            if title is not None:
                # a 태그 내용 출력
                lst_title.append(title.text.strip())

            # a 태그 중 class 속성이 "thumb_image"인 요소를 찾습니다.
            thumb_image = prod_main_info_div.find("div", class_="thumb_image")
            if thumb_image is not None:
                image_tag = thumb_image.find("img")

                if ("image_lazy" in image_tag.get("class", [])):
                    lst_name.append(image_tag["data-original"])
                else:
                    lst_name.append(image_tag["src"])

            # div.prod_pricelist 요소 추출
            prod_pricelist = prod_main_info_div.find("div", class_="prod_pricelist")
            if prod_pricelist is not None:
                # 가격 정보 추출
                price_list = []
                price_sect = prod_pricelist.find_all("p", class_="price_sect")
                for price in price_sect:
                    strong_tag = price.find("strong")
                    if strong_tag is not None:
                        price_list.append(strong_tag.text.strip())
                lst_price.append(price_list[0] if price_list else None)

            # div.spec_list 요소 추출
            spec_list_div = prod_main_info_div.find('div', class_='spec_list')
            if spec_list_div:
                # a 태그 내용 추출
                a_tags = spec_list_div.select('a')
                spec_dict = {}
                for a_tag in a_tags:
                    if a_tag.select_one('span.cm_mark') != None:
                        key = a_tag.select_one('span.cm_mark').text.strip()
                        value = a_tag.get_text(strip=True).replace(key, '').strip()
                        if key and value:
                            spec_dict[key] = value
                lst_a3.append(spec_dict)

                # span.cm_mark 태그 내용 추출
                cm_mark_tags = spec_list_div.select('span.cm_mark')
                spec_dict = {}
                for cm_mark_tag in cm_mark_tags:
                    next_texts = ""
                    next_element = cm_mark_tag.next_sibling
                    while next_element and not (
                            next_element.name == 'span' and 'cm_mark' in next_element.get('class', [])):
                        if next_element.name == 'a':
                            next_texts += next_element.get_text(strip=True)
                        elif isinstance(next_element, str) and next_element.strip():
                            next_texts += next_element.strip()
                        next_element = next_element.next_sibling

                    if next_texts:
                        spec_dict[cm_mark_tag.get_text(strip=True)] = next_texts
                lst_spec.append(spec_dict)

    # 크롤링 결과 리스트로 저장
    for i in range(len(lst_title)):
        result_dict = {
            '이미지 URL': lst_name[i],
            '노트북 이름': lst_title[i],
            '가격': lst_price[i],
            '노트북 유형': lst_a3[i]['노트북유형'] if '노트북유형' in lst_a3[i] else None,
            '운영체제': lst_a3[i]['운영체제'] if '운영체제' in lst_a3[i] else None,
        }
        result_dict.update(lst_spec[i])
        result_list.append(result_dict)

    # 결과 출력
    for result in result_list:
        print(result)

    print("result 개수", len(result_list))

finally:
    # WebDriver 종료
    time.sleep(2)
    driver.quit()
