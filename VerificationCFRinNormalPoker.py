#對CFR策略進行驗證,與隨機策略機器人對打
#每位玩家各發2張手牌,翻出三張公共牌
#策略樹                    root
#                 /                  \
#P2            CHECK                BET
#             /     \              /  \
#P1        CHECK    BET         CALL  FOLD
#           /      /   \       P1下$2  P1下$1
#P2      P1下$1  CALL  FOLD    P2下$2  P2下$2
#        P2下$1  /      \
#             P1下$2   P1下$2
#             P2下$2   P2下$1
import numpy as np
from config import dataPath,handRanks,hands
from lib.SimulateRound import evaluateHandsRank
import random

#手牌索引   手牌string
# 1~13  梅花 2~A C
# 14~26 菱形 2~A D
# 27~39 愛心 2~A H 
# 40~52 黑桃 2~A S
#將手牌索引轉換成字串 e.g. 1 = 2C 14 =2D
def cardIdxToCardStr(cardIdxArray):
    CardsStr = ""
    for card in cardIdxArray:
        cardRank = ""
        cardNum = ""
        if card >=1 and card <=13:
            cardRank = "C"
        elif card >=14 and card <=26:
            cardRank = "D"
        elif card >=27 and card <=39:
            cardRank = "H"
        elif card >=40 and card <=52:
            cardRank = "S"
        else:
            print("outOfRange")
        if card%13==0:
            cardNum ="A"
        elif card%13==9:
            cardNum ="T"
        elif card%13==10:
            cardNum ="J"
        elif card%13==11:
            cardNum ="Q"
        elif card%13==12:
            cardNum ="K"
        else:
            cardNum = str(card%13+1)
        CardsStr = CardsStr+cardNum + cardRank
    return CardsStr
#模擬牌局,輸入牌型等級與該牌型最大的牌
#對所有牌型組合隨機抽樣10000次計算勝率
def simulateWinRate(HandsMaxCard,HandsRank):
    winCount = 0
    iteration = 5000
    for _ in range(0,iteration):
        rndSimulateCardIdx = random.sample(range(1,53), 5) 
        sHandsStr = cardIdxToCardStr(rndSimulateCardIdx)
        _,globalmaxCardS1,rankS1,_ = evaluateHandsRank \
        ([sHandsStr[0:2],sHandsStr[2:4]],[sHandsStr[4:6],sHandsStr[6:8],sHandsStr[8:10]])
        
        if HandsRank>rankS1:
            winCount = winCount + 1 
        elif HandsRank==rankS1:
            if HandsMaxCard == globalmaxCardS1:
                winCount = winCount + 0.5 
            elif((HandsMaxCard[0]>globalmaxCardS1[0]) or (HandsMaxCard[0]==globalmaxCardS1[0] and HandsMaxCard[1]>globalmaxCardS1[1])):
                winCount = winCount + 1 
    return winCount/iteration
sort_rank=[]
with open(dataPath+"rankingData,num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "r") as f:
    for line in f:
        sort_rank.append(str(line.strip()))
#載入手牌+公共牌所有組合
CARDS_DEALINGS=[]
with open(dataPath+"CARDS_DEALINGS num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "r") as f:
    for line in f:
        CARDS_DEALINGS.append(str(line.strip()))

#載入CFR策略
P1CFR_fileName = 'iter/sampling_cfr_iter10000final.npy'
P2CFR_fileName = 'iter/sampling_cfr_iter0.npy'
P1CFRStrategy = np.load(P1CFR_fileName).item()
P2CFRStrategy = np.load(P2CFR_fileName).item()
#紀錄玩家金錢量,起始手牌勝負,最終勝負
totalMoney = {'P1':100000,'P2':100000}
handWL = {'P1Win':0,'P1Lose':0,'tie':0}
handfinalWL = {'P1Win':0,'P1Lose':0,'tie':0}

show = False
#模擬次數
iterations = 20
#模擬牌局
for g in range(0,iterations):
    print(g+1)
    #發牌給P1,P2玩家
    #先隨機取出1~52張牌中的7張牌,2張給P1,2張給P2,3張公共牌
    Cards = random.sample(range(1,53), 7) 
    #把poker的索引值轉換為string手牌
    CardsStr = cardIdxToCardStr(Cards)

    P1Cards = [CardsStr[0:2],CardsStr[2:4]]
    P2Cards = [CardsStr[4:6],CardsStr[6:8]]
    PublicCards = [CardsStr[8:10],CardsStr[10:12],CardsStr[12:14]]

    
    #先計算結果
    result = 0
    _,maxCardP1,rankP1,outputStrP1 = evaluateHandsRank(P1Cards,PublicCards)
    _,maxCardP2,rankP2,outputStrP2 = evaluateHandsRank(P2Cards,PublicCards)
    if rankP1>rankP2:
        result = 1
    elif rankP1<rankP2:
        result = -1
    else:
        if maxCardP1 == maxCardP2:
            result = 0
        elif((maxCardP1[0]>maxCardP2[0]) or (maxCardP1[0]==maxCardP2[0] and maxCardP1[1]>maxCardP2[1])):
            result = 1
        else:
            result = -1
    #紀錄發好壞牌歷史
    if result==1:
        handWL['P1Win']=handWL['P1Win']+1
    elif result==-1:
        handWL['P1Lose']=handWL['P1Lose']+1
    else:
        handWL['tie']=handWL['tie']+1


    #模擬P1最大牌型的勝率
    winRate = simulateWinRate(maxCardP1,rankP1)
    #依照勝率選擇對應的tiny CFR策略
    tinyLen = len(sort_rank)  
    rr = round(winRate*tinyLen)
    if rr>=tinyLen : rr=tinyLen-1      
    P1 = sort_rank[rr]
    #P2策略隨機選一個
    P2 = "2C2D4C4D5C"

    if show:
        print("=============",str(g+1),"=============")
        print(P1)
        print(P2)
    allSelectStrategy=''
    winMoney = 1
    foldevent = False
    strategy = P1CFRStrategy
    for i in range(0,100):
    #這回合行動的玩家
        if i%2 ==1:
            
            nowPlayer = P2
            strategy = P2CFRStrategy
        else:
            nowPlayer = P1
            strategy = P1CFRStrategy

        if i==0:
            nowStrategy = '.'+nowPlayer+'.'
        else:
            nowStrategy = '.'+nowPlayer
        subStrategy = strategy[nowStrategy+allSelectStrategy]
        subStrategyKey = [] 
        subStrategyProb = []
        for key in subStrategy:
            value = subStrategy[key]
            subStrategyProb.append(value)
            subStrategyKey.append(key)
        #策略走到null代表遊戲結束
        if subStrategyKey==[]:
            #print('Game End')
            break
        #依照CFR策略機率選取策略
        selectStrategy=np.random.choice(subStrategyKey, 1, p=subStrategyProb)[0]
        allSelectStrategy = allSelectStrategy+'.'+selectStrategy
        
        #imshow 
        if show:
            print('player2回合:') if i%2 == 0 else print('player1回合:')
            print('選擇策略:',selectStrategy)

        if selectStrategy=='FOLD':
            if nowPlayer==P1:
                #print('P2獲勝,P2+1')
                handfinalWL['P1Lose'] = handfinalWL['P1Lose']+1
                totalMoney['P1'] = totalMoney['P1'] - 1 
                totalMoney['P2'] = totalMoney['P2'] + 1 
            else:
                #print('P1獲勝,P1+1')
                handfinalWL['P1Win'] = handfinalWL['P1Win']+1
                totalMoney['P2'] = totalMoney['P2'] - 1 
                totalMoney['P1'] = totalMoney['P1'] + 1 
            foldevent = True
            break  
        if selectStrategy=='BET':
            winMoney=2
    #結算
    if not foldevent:
        if result == 1:
            #print('P1獲勝,P1+',str(winMoney))
            handfinalWL['P1Win'] = handfinalWL['P1Win']+1
            totalMoney['P1'] = totalMoney['P1'] + winMoney
            totalMoney['P2'] = totalMoney['P2'] - winMoney
        elif result == -1:
            #print('P2獲勝,P2+',str(winMoney))
            handfinalWL['P1Lose'] = handfinalWL['P1Lose']+1
            totalMoney['P1'] = totalMoney['P1'] - winMoney
            totalMoney['P2'] = totalMoney['P2'] + winMoney
        elif result == 0:
            #print('平手')
            handfinalWL['tie'] = handfinalWL['tie']+1

print('最終金錢結算')
print(totalMoney)
print('最終勝負局數')
print(handfinalWL)
print('發牌傾向紀錄')
print(handWL)