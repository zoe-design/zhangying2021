from bs4 import BeautifulSoup
import pandas as pd
import requests


#主函数：对每个网页数据，进行1）提取html，2）生成数据df，3）清洗数据，4）存入已有之前网页信息的excel；四项工作
def main():
    #基础信息
    base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'
    page_input = input('需要采集到多少页？')
    fpath:str = input('数据表格存储地址：')

    #空df文件建立
    df_total=pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])

    for i in range(int(page_input)):
        #得到网址
        request_url = base_url + str(i+1) + '.shtml'
        #1）提取html
        soup_url=get_page_content(request_url)
        #2）从html提取数据并生成df文件
        df_get=analysis(soup_url)
        df_total=df_total.append(df_get)

    #3）数据清洗
    df_clean = data_clean(df_total)
    #4）存入excel
    df_clean.to_excel(fpath,index=False)


#提取html
def  get_page_content(request_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=headers, timeout=10)
    content = html.text
    soup_url = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup_url


#从html提取数据并生成df文件
def analysis(soup):
    df_get = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type','desc', 'problem', 'datetime','status'])
    temp = soup.find('div', class_='tslb_b')
    tr_list = temp.find_all('tr')
    for tr in tr_list:
        td_list = tr.find_all('td')
        if len(td_list) > 0:
            id, brand, car_model, type, desc, problem, datetime, status = \
                td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, \
                td_list[6].text, td_list[7].text
            # print(id,brand,car_model,type,desc,problem,datetime,status)
            temp = {}
            temp['id'] = id
            temp['brand'] = brand
            temp['car_model'] = car_model
            temp['type'] = type
            temp['desc'] = desc
            temp['problem'] = problem
            temp['datetime'] = datetime
            temp['status'] = status
            df_get = df_get.append(temp, ignore_index=True)
    return df_get


#df数据下的数据清洗
def data_clean(df_total):
    #type列数据清洗
    df_total['type_year']=''
    df_total['type_engine'] =''
    df_total['type_transmission'] = ''
    df_total['type_other'] = ''

    for i,row in df_total.iterrows():
        year, engine, transmission, other = type_analysis(row['type'].split(' '))
        df_total.loc[i, 'type_year'] = year
        df_total.loc[i, 'type_engine'] = engine
        df_total.loc[i, 'type_transmission'] = transmission
        df_total.loc[i, 'type_other'] = other
    df_total=df_total.drop(columns=['type'])

    #problem列数据清洗
    problem_data=df_total.problem.str.get_dummies(sep=',')
    df_total=df_total.drop(columns=['problem']).join(problem_data)
    return df_total


#type列数据清洗具体函数
def type_analysis(type):
    year, engine, transmission, other = '', '', '', ''
    engine_list = ['1.2T', '1.4T', '1.4L', '1.4TSI', '1.5L', '1.5T', '1.5TD', '1.6L', '1.6T', '1.6THP', '1.8L', '1.8T',
                   '1.8TD', '1.8TSI', '2.0L', '2.0T', '2.4L', '2.5L', '2.5T', '14T', '20T', '30T', '230TSI', '350T',
                   '280TSI', '260T', '300T', '300TGI', '330TSI', '350THP', '350T', 'TSI280', '400TGI']
    for i in type:
        if type.index(i) == 0 and i[-1:] == '款':
            year = i[:-1]
            continue
        if i == '手动' or i == '自动':
            transmission = i
            continue
        if i in engine_list:
            engine = i
            continue
        other = other + ' ' + i
    return year, engine, transmission, other


if __name__ == '__main__':
    main()
