#模擬tiny poker版本,牌數字從2~7,只有兩種花色
#第一回合兩位玩家發兩張手牌
#第二回合翻三張公共牌
#公共牌經排序後不重複
from config import hands,handRanks,dataPath
import time
import os
def createHands(hands,handRanks):
    allPoker =[]
    for hand in hands:
        for handRank in handRanks: 
            handAndRank = hand+handRank
            allPoker.append(handAndRank)
    return allPoker
def createCardIndex(totalPoker):
    Card_t=[]
    for cardO in range(0,totalPoker):
        for cardT in range(cardO+1,totalPoker):
            Card_t.append([cardO,cardT])
    return Card_t
def reomveArrayValue(removeValueArray):
    arr = createHands(hands,handRanks)
    for rm in removeValueArray:
        arr.pop(arr.index(rm))
    return arr
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
       

def createData():
    # 產生data存放的資料夾
    createFolder('./data/')
    #2h,2s,3h,3s....由小排到大
    allPoker_ =createHands(hands,handRanks)
    pokerTotal = len(allPoker_)
    ###########################
    #模擬兩位玩家各自的兩張手牌  #
    #手牌第一張會比第二張小     #
    ###########################
    CardTwoPlayer = []            
    Card_t = createCardIndex(pokerTotal)
    for i in range(0,len(Card_t)):
        P1Cards = Card_t[i]
        P1hand_1 = P1Cards[0]#較小的牌
        P1hand_2 = P1Cards[1]#較大的牌
        CardsIndex = createCardIndex(pokerTotal)
        #把P1手上這兩張牌的所有可能組合去除
        for m in range(P1hand_1+1,pokerTotal):
            try:
                CardsIndex.pop(CardsIndex.index([P1hand_1,m]))
            except ValueError:  
                continue
        for m in range(P1hand_2+1,pokerTotal):
            try:
                CardsIndex.pop(CardsIndex.index([P1hand_2,m]))
            except ValueError:
                continue
    
        for n in range(0,P1hand_1):
            try:
                CardsIndex.pop(CardsIndex.index([n,P1hand_1]))
            except ValueError: 
                continue
        for n in range(0,P1hand_2):
            try:
                CardsIndex.pop(CardsIndex.index([n,P1hand_2]))
            except ValueError:
                continue
        #對這些不重複的牌進行組合
        for j in range(0,len(CardsIndex)):
            P2Cards = CardsIndex[j]
            P2hand_1 = P2Cards[0]
            P2hand_2 = P2Cards[1]
            arr = [P1hand_1, P1hand_2, P2hand_1, P2hand_2]
            CardTwoPlayer.append(arr)  
    CARDS_DEALINGS = []
    count=0
    for cards in CardTwoPlayer:
        #初始化
        allPoker =createHands(hands,handRanks)
        #玩家各兩張手牌
        P1_1 = allPoker[cards[0]]
        P1_2 = allPoker[cards[1]]
        P2_1 = allPoker[cards[2]]
        P2_2 = allPoker[cards[3]]
        #抽出P1,P2選擇的牌
        arr = [P1_1,P1_2,P2_1,P2_2]
        allPokerPreflop = reomveArrayValue(arr)
        for pub1 in range(0,len(allPokerPreflop)):
            #公共牌第1張牌
            pub1Str = allPokerPreflop[pub1]
            #抽出P1,P2,第一張公共牌 
            arr = [P1_1,P1_2,P2_1,P2_2,pub1Str]
            #將第1張公共牌去除
            allPokerFlop1 = reomveArrayValue(arr)
            
            for pub2 in range(0,len(allPokerFlop1)):
                #公共牌第2張牌
                pub2Str = allPokerFlop1[pub2]
                #抽出P1,P2,第1,2張公共牌 
                arr = [P1_1,P1_2,P2_1,P2_2,pub1Str,pub2Str]
                #將第2張公共牌去除
                allPokerFlop2 = reomveArrayValue(arr)
                
                for pub3 in range(0,len(allPokerFlop2)):
                    #公共牌第3張牌
                    pub3Str = allPokerFlop2[pub3]
                    #抽出P1,P2,第1,2,3張公共牌
                    sortArr = [pub1Str,pub2Str,pub3Str]
                    #將三張公共牌排序
                    sortArr.sort()
                    arr = [P1_1,P1_2,P2_1,P2_2,sortArr[0],sortArr[1],sortArr[2]]
                    thisRoundCard = arr[0] + arr[1] + arr[2] + arr[3] + arr[4] + arr[5] + arr[6] 
                    #檢查此組合有沒有存在
                    try:
                        CARDS_DEALINGS.index(thisRoundCard)
                    #不存在則儲存
                    except ValueError:   
                        CARDS_DEALINGS.append(thisRoundCard) 
                        count=count+1
                        print(count) 
    #把組合結果存起來
    with open(dataPath+"CARDS_DEALINGS num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "w") as file:
        for s in CARDS_DEALINGS:
            file.write(str(s) + '\n')

