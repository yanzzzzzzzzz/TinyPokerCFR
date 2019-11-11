#載入計算手牌強度lib
from lib.SimulateRound import evaluateHandsRank
from config import NumDict,rankDict,hands,handRanks,dataPath
#將手牌排序
def handSort(handStr):
    dataLen = int(len(handStr)/2)
    handArr = []
    for i in range(0,dataLen):
        handArr.append(handStr[i*2:(i+1)*2])
    handIntArr=[]
    for h in handArr:
        Num = list(NumDict.keys())[list(NumDict.values()).index(h[0])]
        rank = list(rankDict.keys())[list(rankDict.values()).index(h[1])]
        handIntArr.append([Num,rank])
    for i in range(0,len(handArr)):
        for j in range(i+1,len(handArr)):
            Hi = handIntArr[i]
            Hj = handIntArr[j]
            if Hi[0]>Hj[0] or Hi[0]==Hj[0] and Hi[1]>Hj[1]:
                tmp = handIntArr[i]
                handIntArr[i] = handIntArr[j]
                handIntArr[j] = tmp
    result =""
    for h in handIntArr:
        Num = NumDict[h[0]]
        rank = rankDict[h[1]]
        result = result +Num+rank
    return result

def CreateHandsRank():
    #載入牌型所有組合
    CARDS_DEALINGS=[]
    with open(dataPath+"CARDS_DEALINGS num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "r") as f:
        for line in f:
            CARDS_DEALINGS.append(str(line.strip()))
    maxRank = 10
    save_data = []
    for findrank in range(1,maxRank):
        for i in range(0,len(hands)):
            for j in range(0,len(handRanks)):
                findMaxCard = hands[i] + handRanks[j]
                for c in CARDS_DEALINGS:
                    P1hands = [c[0:2],c[2:4]]
                    pubCards = [c[8:10],c[10:12],c[12:14]]
                    
                    _,globalmaxCard,rank,ss =  evaluateHandsRank(P1hands,pubCards)
                    Num = NumDict[globalmaxCard[0]]
                    ranking = rankDict[globalmaxCard[1]]
                    maxCardStr = Num+ranking
                    if rank==findrank and findMaxCard==maxCardStr:
                        outputStr = c[0:2]+c[2:4]+c[8:10]+c[10:12]+c[12:14]
                        sortStr = handSort(outputStr)
                        #pop
                        CARDS_DEALINGS.pop(CARDS_DEALINGS.index(c))
                        #存進arr中
                        try:
                            save_data.index(sortStr)
                        #不存在則儲存
                        except ValueError:   
                            save_data.append(sortStr) 
                            print(sortStr) 
                            
    with open(dataPath+"rankingData,num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "w") as file:
        for s in save_data:
            file.write(str(s) + '\n')