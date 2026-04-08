## 能量距離 (Energy Distance)

一種衡量統計分佈變化的無參數方式。

常見的線性建模非常依賴全樣本數據，而且參數敏感，換了不同樣本就會擬和出不同參數，這時就會陷入子我懷疑的漩渦，我是要每天每周還是每月更新一次模型? 這時的背離要等待它均值回歸還是現在更新參數? 更不要提參數敏感的統計套利，相關性只要開始不穩定，交易就會開始各種虧損直接是一場災難。


因此，非線性統計建模還是很有研究價值的。
##  數學定義

$$
\mathcal{E}(X,Y) = 2E\|X - Y\| - E\|X - X'\| - E\|Y - Y'\|
$$

<p align="center">或</p>

$$
\hat{D}^2 = \frac{2}{nm} \sum_{i=1}^{n} \sum_{j=1}^{m} |x_i - y_j| - \frac{1}{n^2} \sum_{i=1}^{n} \sum_{j=1}^{n} |x_i - x_j| - \frac{1}{m^2} \sum_{i=1}^{m} \sum_{j=1}^{m} |y_i - y_j|
$$

### 公式項解構：
1. **第一項 (Cross Distance)：** 衡量兩樣本集 $X$ 與 $Y$ 之間的平均絕對距離。
2. **第二、三項 (Internal Distance)：** 衡量樣本集內部點與點之間的平均絕對距離。

### 為什麼選擇 Energy Distance？
數據結構分佈的轉換需要直觀的觀察，無論是**偏態 (Skewness)**、**峰度 (Kurtosis)** 或**任何形狀**改變，能量化都能精準捕捉。

### 一些範例

> 單資產 (美光 MU)
<img width="1798" height="523" alt="image" src="https://github.com/user-attachments/assets/62245540-ff26-45da-ba3c-53dbe44229da" />

> 多資產 (標普500, 羅素2000, 那指, 道指)
<img width="1834" height="799" alt="image" src="https://github.com/user-attachments/assets/86404a33-6032-4ce8-9591-bd06d77e5753" />
