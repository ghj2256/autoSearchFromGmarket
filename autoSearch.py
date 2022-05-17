import requests
from bs4 import BeautifulSoup as Bs
import re
import pandas as pd
import time


def search():
    base_url = 'http://minishop.gmarket.co.kr'
    market = '/organicmaru1004'
    res = requests.get(base_url + market)  # 기본화면 request
    soup = Bs(res.text, 'lxml')

    category_list = []  # 카테고리를 담을 list
    product_code = []  # 상품코드를 담을 list

    category = soup.find_all('li', attrs={'class': "splt_ico"})  # 카테고리 list화
    for c in category:
        category_product = []  # 카테고리별 상품코드 담을 list
        category_list.append(c.find('a').text)  # 카테고리 추가
        res = requests.get(base_url + c.find('a')['href'])  # 해당 카테고리로 이동
        soup = Bs(res.text, 'lxml')
        page = soup.find('div', 'paging')  # 페이지 검색
        max_page = re.sub(r'<.*?>|\D', '', str(page.find_all('a')))[-1]  # 최대 페이지
        for i in range(int(max_page)):  # 페이지 수만큼 반복
            res = requests.get(base_url + c.find('a')['href'] + '&Page=' + str(i + 1))  # 해당 페이지로 이동
            soup = Bs(res.text, 'lxml')
            product = soup.find_all('p', attrs={'class': 'prd_img'})  # 상품정보 list화(태그 포함된 상태)
            category_product.extend(
                [int(re.sub(r'\D', '', str(x.find('a')['href']))) for x in product])  # 해당 페이지에 있는 상품코드 리스트에 추가
        product_code.append(category_product)  # 상품코드 리스트에 카테고리별 상품 리스트 형식으로 추가(2차원 리스트)

    return dict(zip(category_list, product_code))  # 카테고리와 상품코드를 묶어 딕셔너리로 반환


def write_to_excel(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_excel('C:/Users/User/Documents/product_code.xlsx', index=False)


if __name__ == "__main__":
    start = time.time()
    write_to_excel(search())
    print("Working time: {} sec. ".format(time.time() - start))
