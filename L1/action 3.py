from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd


def main():
    fpath = 'car_data.csv'
    data = pd.read_csv(fpath,encoding='gbk')
    data_preprocess(data)
    define_k(data)
    n = int(input('根据可视化图表确定k值为：'))
    data_KMeans(data,n)

'''数据均一化'''
def data_preprocess(data):
    train_x = data[['人均GDP','城镇人口比重','交通工具消费价格指数','百户拥有汽车量']]
    min_max_scaler = preprocessing.MinMaxScaler()
    train_x = min_max_scaler.fit_transform(train_x)
    pd.DataFrame(train_x).to_csv('temp.csv', index=False)

'''K-Means手肘法，确定k'''
def define_k(data):
    train_x = data[['人均GDP', '城镇人口比重', '交通工具消费价格指数', '百户拥有汽车量']]
    import matplotlib.pyplot as plt
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(train_x)
        sse.append(kmeans.inertia_)
    x = range(1, 11)
    plt.xlabel('K')
    plt.ylabel('SSE')
    plt.plot(x, sse, 'o-')
    plt.show()

'''kmeans聚类'''
def data_KMeans(data,n):
    train_x = data[['人均GDP', '城镇人口比重', '交通工具消费价格指数', '百户拥有汽车量']]
    kmeans = KMeans(n_clusters=n)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
    result.rename({0: u'聚类结果'}, axis=1, inplace=True)
    result.to_csv("customer_cluster_result.csv", index=False)

if __name__ == '__main__':
    main()
