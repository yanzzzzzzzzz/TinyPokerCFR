import numpy as np
from config import dataPath,handRanks,hands
from lib.SimulateRound import evaluateHandsRank
import random
#載入手牌+公共牌所有組合
CARDS_DEALINGS=[]
with open(dataPath+"CARDS_DEALINGS num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "r") as f:
    for line in f:
        CARDS_DEALINGS.append(str(line.strip()))

#load cfr strategy
CFRFilePath = 'iters'
#預設P1為經過數次訓練的Bot
#P2完全隨機決策的bot
P1CFR_fileName = CFRFilePath + '/sampling_cfr_iter10000final.npy'
P2CFR_fileName = CFRFilePath + '/sampling_cfr_iter0.npy'
P1CFRStrategy = np.load(P1CFR_fileName).item()
P2CFRStrategy = np.load(P2CFR_fileName).item()
#紀錄最終勝負,起始手牌勝負
totalMoney = {'P1':100000,'P2':100000}
handWL = {'P1Win':0,'P1Lose':0,'tie':0}
handfinalWL = {'P1Win':0,'P1Lose':0,'tie':0}
show = False
#模擬牌局
for g in range(0,10000):
    print('模擬局數:'+ str(g+1))
    rndNum = random.randint(0,len(CARDS_DEALINGS)-1)
    
    r = CARDS_DEALINGS[rndNum]
    #發牌給P1,P2玩家
    P1Cards = [r[0:2],r[2:4]]
    P2Cards = [r[4:6],r[6:8]]
    PublicCards = [r[8:10],r[10:12],r[12:14]]
    P1 = r[0:4] + r[8:14]
    P2 = r[4:8] + r[8:14]
    if show:
        print("=============",str(g+1),"=============")
        print(P1)
        print(P2)
    #先計算結果
    result = 0
    CardTransferP1,globalmaxCardP1,rankP1,outputStrP1 = evaluateHandsRank(P1Cards,PublicCards)
    CardTransferP2,globalmaxCardP2,rankP2,outputStrP2 = evaluateHandsRank(P2Cards,PublicCards)
    if rankP1>rankP2:
        result = 1
    elif rankP1<rankP2:
        result = -1
    else:
        if globalmaxCardP1 == globalmaxCardP2:
            result = 0
        elif((globalmaxCardP1[0]>globalmaxCardP2[0]) or (globalmaxCardP1[0]==globalmaxCardP2[0] and globalmaxCardP1[1]>globalmaxCardP2[1])):
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
    allSelectStrategy=''
    winMoney = 1
    foldevent = False
    strategy = P1CFRStrategy
    for i in range(0,100):
    #這回合行動的玩家
        if i%2 ==0:
            
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
                totalMoney['P1']=totalMoney['P1']-1
                totalMoney['P2']=totalMoney['P2']+1
                handfinalWL['P1Lose'] = handfinalWL['P1Lose']+1
            else:
                #print('P1獲勝,P1+1')
                totalMoney['P1']=totalMoney['P1']+1
                totalMoney['P2']=totalMoney['P2']-1
                handfinalWL['P1Win'] = handfinalWL['P1Win']+1
            foldevent = True
            break  
        if selectStrategy=='BET':
            winMoney=2
    #結算
    if not foldevent:
        if result==1:
            #print('P1獲勝,P1+',str(winMoney))
            totalMoney['P1']=totalMoney['P1']+winMoney
            totalMoney['P2']=totalMoney['P2']-winMoney
            handfinalWL['P1Win'] = handfinalWL['P1Win']+1
        elif result==-1:
            #print('P2獲勝,P2+',str(winMoney))
            totalMoney['P1']=totalMoney['P1']-winMoney
            totalMoney['P2']=totalMoney['P2']+winMoney
            handfinalWL['P1Lose'] = handfinalWL['P1Lose']+1
        elif result ==0:
            handfinalWL['tie'] = handfinalWL['tie']+1
print('最終金錢結算')
print(totalMoney)
print('最終勝負局數')
print(handfinalWL)
print('發牌傾向紀錄')
print(handWL)