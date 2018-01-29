import pandas as pd
from io import StringIO

from sklearn import linear_model
import numpy as np

import matplotlib.pyplot as plt

# 房屋面积与价格历史数据(csv文件)
csv_data = 'square_feet,price\n150,6450\n200,7450\n250,8450\n300,9450\n350,11450\n400,15450\n600,18450\n'
raw_data='''1200000,261.4E+00
1300000,262.7E+00
1400000,264.03E+00
1500000,265.38E+00
1600000,268.98E+00
1700000,270.38E+00
1800000,272.17E+00
1900000,273.13E+00
2000000,274.53E+00
2100000,275.51E+00
2200000,278.68E+00'''

data1=[
1200000,261.93E+00,
1300000,263.04E+00,
1400000,264.48E+00,
1500000,265.86E+00,
1600000,269.45E+00,
1700000,271.01E+00,
1800000,272.43E+00,
1900000,273.3E+00,
2000000,274.89E+00,
2100000,276.1E+00,
2200000,278.98E+00,
]

data2=[
1200000,277.06E+00,
1300000,279.19E+00,
1400000,281.2E+00,
1500000,283.18E+00,
1600000,286.14E+00,
1700000,290.04E+00,
1800000,292.33E+00,
1900000,294.42E+00,
2000000,296.68E+00,
2100000,299.63E+00,
2200000,309.3E+00,
]

data2_2=[
1200000,157.41E+00,
1300000,158.94E+00,
1400000,160.28E+00,
1500000,161.61E+00,
1600000,164.24E+00,
1700000,167.33E+00,
1800000,169.2E+00,
1900000,170.48E+00,
2000000,171.77E+00,
2100000,173.18E+00,
2200000,176.54E+00,
]
data2_40core=[
1200000,160.03E+00,
1300000,161.73E+00,
1400000,163.46E+00,
1500000,165.33E+00,
1600000,167.84E+00,
1700000,171.4E+00,
1800000,174.4E+00,
1900000,175.52E+00,
2000000,177.19E+00,
2100000,178.89E+00,
2200000,182.7E+00,
]
# 读入dataframe
#df = pd.read_csv(StringIO(csv_data))
#print(df)

def data_process(data):
	# 建立线性回归模型
	regr = linear_model.LinearRegression()
	x = data[::2]
	y = data[1::2]
	# 拟合
	x=np.array(x).reshape(-1,1)
	#regr.fit(df['square_feet'].reshape(-1, 1), df['price'])  # 注意此处.reshape(-1, 1)，因为X是一维的！
	regr.fit(x,y)
	# 不难得到直线的斜率、截距
	a, b = regr.coef_, regr.intercept_
	print("%f*x+%f"%(a,b))
	# 方式2：根据predict方法预测的价格
	yy=(regr.predict(x))
	# 画图
	# 1.真实的点
	plt.scatter(x, y, color='blue')
	# 2.拟合的直线
	plt.plot(x, yy, color='red', linewidth=4)
	plt.title("%f*x+%f"%(a,b))
	plt.show()
	return a[0],b



a,b=data_process(data2_40core)
#data_process(data2)
print(a,b)

#target_power =