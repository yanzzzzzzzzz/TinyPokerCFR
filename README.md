# TinyPokerCFR
使用自定義的德州撲克遊戲進行CFR訓練並驗證成果

## Running the tests
在`config.py`檔案中,可自行定義撲克牌數量與花色

* 例如:`hands = ['2','3','4','5']`,`handRanks =['C','D']`
* 代表撲克牌數字有2~5,花色有梅花(club)與菱形(diamond)
* 可以自行新增與修改手牌數量,但必須由小到大排序


產生CFR所需的資料
```
run CreateData.py
```
CFR訓練
```
run TrainingCFR.py
```
CFR驗證
```
run VerificationCFRinTinyPoker.py
```
或是在正常的撲克牌數量下透過勝率映射到`tiny poker`選擇決策
```
run VerificationCFRinNormalPoker.py
```
## Result 
CFR策略迭代次數:$10^6$
隨機策略:所有策略全部隨機
測試遊戲局數:100000局
### Tiny poker 下遊戲結果
#### 隨機策略先動作情況下
| BOT | RTP |
| :------: | :-----------: |
| CFR策略| 1.2036 |
| 隨機策略 | 0.7964 |

