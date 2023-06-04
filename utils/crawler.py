import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models import Product


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

        for page_num in range(2, 11):
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
                        if a_tag.select_one('span.cm_mark') is not None:
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
        result_list = []
        db_product_list = []
        for i in range(len(lst_title)):
            battery_info = 999999
            inch_info = ""
            ram_capacity = 999999
            storage_capacity = 999999
            weight_info = 999999
            weight = 999999
            extracted_capacity = 999999

            # '배터리:' 다음의 숫자부터 '/' 이전까지의 부분을 추출
            if lst_spec[i].get('파워') is not None:
                start_index = lst_spec[i].get('파워').find("배터리:")
                end_index = lst_spec[i].get('파워').find("/", start_index)
                battery_info = lst_spec[i].get('파워')[start_index + len("배터리:"):end_index]

            if lst_spec[i].get("화면정보") is not None:
                # '(' 다음의 숫자부터 '인치'까지의 부분을 추출
                start_index = lst_spec[i].get("화면정보").find("(")
                end_index = lst_spec[i].get("화면정보").find(")", start_index)
                inch_info = lst_spec[i].get("화면정보")[start_index + 1:end_index-2]

            # '램 용량:' 다음의 숫자부터 '/' 이전까지의 부분을 추출
            if lst_spec[i].get("램") is not None:
                start_index = lst_spec[i].get("램").find("램 용량:")
                end_index = lst_spec[i].get("램").find("/", start_index)
                ram_capacity = lst_spec[i].get("램")[start_index + len("램 용량:"):end_index-2]

            # '/' 이전의 부분을 추출
            if lst_spec[i].get("저장장치") is not None:
                end_index = lst_spec[i].get("저장장치").find("/", 2)
                storage_capacity = lst_spec[i].get("저장장치").split('/')[1]


                if storage_capacity.endswith("GB"):
                    extracted_capacity = storage_capacity.replace("GB", "")
                elif storage_capacity.endswith("TB"):
                    tb_capacity = int(storage_capacity.replace("TB", ""))
                    extracted_capacity = str(tb_capacity * 1000)

            if lst_spec[i].get('CPU') is not None:
                lst_spec[i]['CPU'] = lst_spec[i].get("CPU").replace("/", " ").strip()

            if lst_spec[i].get('주요제원') is not None:
                weight_info = None
                start_index = lst_spec[i].get('주요제원').find("무게:")
                if start_index != -1:
                    if lst_spec[i].get('주요제원').find("kg", start_index) != -1:
                        end_index = lst_spec[i].get('주요제원').find("kg", start_index)
                        weight_info = lst_spec[i].get('주요제원')[start_index + len("무게:"):end_index].strip()
                    elif lst_spec[i].get('주요제원').find("g", start_index) != -1:
                        end_index = lst_spec[i].get('주요제원').find("g", start_index)
                        weight_info = int(lst_spec[i].get('주요제원')[start_index + len("무게:"):end_index].strip()) / 1000
                        print(weight_info)


            db_product = Product(
                product_made_by= lst_title[i].split(' ')[0],
                product_name=" ".join(lst_title[i].split(' ')[1:]),
                product_battery=str(battery_info).replace("Wh", ""),
                product_image="https:" + lst_name[i],
                product_cpu=lst_spec[i].get('CPU'),
                product_ram_capacity=ram_capacity,
                product_ram_detail=lst_spec[i].get("램"),
                product_display_size=inch_info,
                product_display_detail=lst_spec[i].get("화면정보"),
                product_graphic=lst_spec[i].get("그래픽"),
                product_storage_capacity=extracted_capacity,
                product_storage_detail=lst_spec[i].get("저장장치"),
                product_weight=weight_info,
                product_price=lst_price[i].replace(',', ''),
            )

            db_product_list.append(db_product)

            result_dict = {
                '제조사': lst_title[i].split(' ')[0],
                '이미지 URL': "https:" + lst_name[i],
                '노트북 이름': " ".join(lst_title[i].split(' ')[1:]),
                '배터리': str(battery_info).replace("Wh", ""),
                '가격': lst_price[i].replace(',', ''),
                '화면크기': inch_info,
                '램 용량': ram_capacity,
                "저장용량": storage_capacity,
                "무게": weight_info
            }

            result_dict.update(lst_spec[i])
            result_list.append(result_dict)

        # 결과 출력

        for key, value in result_list[2].items():
            print(f"{key}: {value}")

        return db_product_list

    finally:
        # WebDriver 종료
        time.sleep(2)
        driver.quit()
