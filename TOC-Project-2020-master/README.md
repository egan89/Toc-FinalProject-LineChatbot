**Line Chatbot**

**想法：**

出國前換外幣或是出國買東西的時候如果沒有考慮好匯率會很虧，為了方便使用者查詢各種外幣的比率，才決定讓自己的line
chatbot做這個功能。

**功能介紹：**

1.一開始先輸入兩種貨幣，英文大小寫都可以 用空格分開：TWD JPY

第二步，輸入要查看兌換比率還是進入金額換算：check or calculate

第三步，如果是calculate就再輸入一個數字來換算

2.如果在user State輸入fsm會show出fsm架構圖

**使用畫面：**

正常使用畫面：

![image](https://imgur.com/04YnMU0.png)

防呆：

![image](https://imgur.com/bLRdaBF.png)

![image](https://imgur.com/IRqlPAQ.png)

**Fsm State 說明：**

user:初始State

input_2currency:輸入兩種貨幣

check:單純查看比率

calculate:進入金額換算

input_number:輸入一個金額做換算

**程式語言：python 3.6.7**

**參考資料：https://tw.rter.info/howto_currencyapi.php**

2020/12/26 by 陳竑曄
