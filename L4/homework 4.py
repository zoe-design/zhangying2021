import pandas as pd
import time
# 导入数据
data = pd.read_csv('Market_Basket_Optimisation.csv',header = None)
# 补全空值
data = data.fillna('')
# 显示所有列
pd.set_option('max_columns',None)


# 基于efficient_apriori判断关联规则
def rule1(s1,c1):
    from efficient_apriori import apriori
    # 计算时间
    start = time.time()

    # 数据格式转化
    transactions = []
    for i in range(data.shape[0]):
        temp_set = set()
        for j in data.columns:
            if data[j][i] != '':
                temp_set.add(data[j][i])
        transactions.append(temp_set)
    # print(transactions)

    # 挖掘频繁项集和关联规则
    itemsets ,rules = apriori(transactions, min_support = s1, min_confidence = c1)
    print('频繁项集：', itemsets)
    print('关联规则：', rules)
    end = time.time()
    print('用时1：',end-start)


# 基于mlxtend判断关联规则
def rule2(s2):
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules
    # 计算时间
    start = time.time()

    # 数据格式转化
    # 1)将每行数据都放入一列，并用'-'分隔
    data['total'] = data[data.columns[:]].apply(lambda x: '-'.join(x.dropna()),axis=1)
    # 2）利用get_dummies建立one-hot编码
    data_ = data.drop(data.columns[:21],axis=1).join(data.total.str.get_dummies(sep='-'))

    # 挖掘频繁项集
    frequent_itemsets = apriori(data_, min_support = s2, use_colnames=True)
    # 按支持度大小，降序排列
    frequent_itemsets = frequent_itemsets.sort_values(by = 'support',ascending=False)
    print("频繁项集：", frequent_itemsets)
    # 求关联规则，选取提升度为度量选项
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    # 按提升度大小，降序排序
    rules = rules.sort_values(by = 'lift',ascending=False)
    print("关联规则：",rules)

    end = time.time()
    print("用时2：", end - start)


def main():
    # 用户自定义支持度及置信度
    s1 = float(input('"rule1支持度"设定为：',))
    c1 = float(input('"rule1置信度"设定为：',))
    rule1(s1,c1)
    print('-' * 50)
    s2 = float(input('"rule2置信度"设定为：',))
    rule2(s2)

if __name__ == '__main__':
    main()

