import re
import time

from bs4 import BeautifulSoup as Bs
from pandas import DataFrame
from requests import get

base_url = 'http://minishop.gmarket.co.kr'


def search_market(url):
    res = get(base_url + url)  # 기본화면 request
    soup = Bs(res.text, 'lxml')

    category_list = []  # 카테고리를 담을 list
    product_code = []  # 상품코드를 담을 list

    if len(soup.body['class']) == 1 or soup.body['class'][1] == 'header_extend':  # 카테고리 list화
        category = soup.select('#brandCategoryButton>ul>li')
    else:
        category = soup.find_all('li', attrs={'class': "splt_ico"})

    for c in category:
        category_product = []  # 카테고리별 상품코드 담을 list
        if c.find('a').text == '전체상품보기':
            continue
        category_list.append(''.join(c.find('a').text.split()[:-1]))
        res = get(base_url + c.find('a')['href'])  # 해당 카테고리로 이동
        soup = Bs(res.text, 'lxml')
        page = soup.find('span', 'last')  # 페이지 검색
        page_info = re.findall(r'Page=\d+', page.find('a')['href'])
        max_page = page_info[0].replace('Page=', '')  # 최대 페이지
        for i in range(int(max_page)):  # 페이지 수만큼 반복
            res = get(base_url + c.find('a')['href'] + '&Page=' + str(i + 1))  # 해당 페이지로 이동
            soup = Bs(res.text, 'lxml')
            product = soup.find_all('p', attrs={'class': 'prd_img'})  # 상품정보 list화(태그 포함된 상태)
            category_product.extend(
                [int(re.sub(r'\D', '', str(x.find('a')['href']))) for x in product])  # 해당 페이지에 있는 상품코드 리스트에 추가
        product_code.append(category_product)  # 상품코드 리스트에 카테고리별 상품 리스트 형식으로 추가(2차원 리스트)

    return dict(zip(category_list, product_code))


def write_to_excel(data):
    df = DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    filename = input("input file name: ")
    df.to_excel('C:/Users/User/Documents/{}.xlsx'.format(filename), index=False)

    return 0


if __name__ == "__main__":
    start = time.time()
    market = '/anotherd'
    write_to_excel(search_market(market))
    print("working time: {:.5f} sec.".format(time.time() - start))
