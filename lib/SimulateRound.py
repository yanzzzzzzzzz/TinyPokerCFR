import random

def createPokers(hands,handRanks):
    PokerIndex = {}
    index = 0
    allPoker =[]
    for hand in hands:
        for handRank in handRanks: 
            handAndRank = hand+handRank
            allPoker.append(handAndRank)
            PokerIndex[str(handAndRank)] = index
            index = index + 1
    return allPoker,PokerIndex

def handsSort(cards):
    for i in range(0,len(cards)):
        for j in range(i+1,len(cards)):
            cardsI = PokerIndex[cards[i]]
            cardsJ = PokerIndex[cards[j]]
            
            if cardsI>cardsJ:
                tmp =cards[i]
                cards[i] = cards[j]
                cards[j] = tmp   
    return cards
def compareCardStrength(card1,card2):
    if card1[0]>card2[0]:
        return card1
    if card1[0]==card2[0] and card1[1]>card2[1]:
        return card1
    return card2
    
def evaluateHandsRank(hands,PublicCards):
    Cards = []
    for hand in hands:
        Cards.append(hand)
    for card in PublicCards:
        Cards.append(card)
    
    #print('排序前:',Cards)
    CardsSort = handsSort(Cards)
    #print('排序後:',CardsSort)
    cardLen = len(CardsSort)
    CardTransfer = []
    for i in range(0,cardLen):
        num = CardsSort[i][0]
        if num =='T':
            num = 9
        elif num =='J':
            num = 10
        elif num =='Q':
            num = 11
        elif num =='K':
            num = 12
        elif num =='A':
            num=13
        else:
            num=int(num)-1
            
        flower = CardsSort[i][1]
        if flower == 'C':
            flower = 1
        elif flower == 'D':
            flower = 2
        elif flower == 'H':
            flower = 3
        elif flower == 'S':
            flower = 4
        CardTransfer.append([num,flower])
    rank = 1
    maxCard = [0,0]
    globalmaxCard = [0,0]
    outputStr = ''
    rankChange = False
    for i in range(0,cardLen-4):
        for j in range(i+1,cardLen-3):
            for k in range(j+1,cardLen-2):
                for l in range(k+1,cardLen-1):
                    for m in range(l+1,cardLen):
                        
                        selectC = [CardTransfer[i],CardTransfer[j],CardTransfer[k],CardTransfer[l],CardTransfer[m]]
                        
                        #c[i][0]數字 c[i][1]花色
                       # print('可能組合:',selectC)
                        if rank<=9:
                            if selectC[0][0] == selectC[1][0]-1 == selectC[2][0]-2 == selectC[3][0]-3 == selectC[4][0]-4 and selectC[0][1] == selectC[1][1] ==selectC[2][1] == selectC[3][1] == selectC[4][1]:
                                if rank!=9:
                                    rankChange = True
                                maxCard = selectC[4]
                                outputStr = '同花順'
                                rank = 9
                            if rank<=8:
                                if selectC[0][0] == selectC[1][0] == selectC[2][0] == selectC[3][0]:
                                    if rank!=8:
                                        rankChange = True
                                    maxCard = selectC[3]
                                    outputStr = '四條'
                                    rank = 8
                        
                                elif selectC[1][0] == selectC[2][0] == selectC[3][0] == selectC[4][0]:
                                    if rank!=8:
                                        rankChange = True
                                    maxCard = selectC[4]
                                    outputStr = '四條'
                                    rank = 8
                                if rank<=7:
                                   if selectC[0][0] == selectC[1][0] and selectC[2][0] == selectC[3][0] == selectC[4][0]:
                                       if rank!=7:
                                           rankChange = True
                                       maxCard = selectC[4]
                                       outputStr = '葫蘆'
                                       rank = 7
                                
                                   elif selectC[0][0] == selectC[1][0] == selectC[2][0] and selectC[3][0] == selectC[4][0]:
                                       if rank!=7:
                                           rankChange = True
                                       maxCard = selectC[2]
                                       outputStr = '葫蘆'
                                       rank = 7
                                       
                                   if rank<=6:
                                       if selectC[0][1] == selectC[1][1] ==selectC[2][1] == selectC[3][1] == selectC[4][1]:
                                           if rank!=6:
                                               rankChange = True
                                           maxCard = selectC[4]
                                           outputStr = '同花色'
                                           rank = 6
                                           
                                       if rank<=5:  
                                           if selectC[0][0] == selectC[1][0]-1 == selectC[2][0]-2 == selectC[3][0]-3 == selectC[4][0]-4 :
                                               if rank!=5:
                                                   rankChange = True
                                               maxCard = selectC[4]
                                               outputStr = '順子'
                                               rank = 5
                                               
                                           if rank<=4:
                                               if selectC[0][0] == selectC[1][0] == selectC[2][0]:
                                                   if rank!=4:
                                                       rankChange = True
                                                   maxCard = selectC[2]
                                                   outputStr = '三條'
                                                   rank = 4
                                               elif selectC[1][0] == selectC[2][0] == selectC[3][0]:
                                                   if rank!=4:
                                                       rankChange = True
                                                   maxCard = selectC[3]
                                                   outputStr = '三條'
                                                   rank = 4
                                               elif selectC[2][0] == selectC[3][0] == selectC[4][0]:
                                                   if rank!=4:
                                                       rankChange = True
                                                   maxCard = selectC[4]
                                                   outputStr = '三條'
                                                   rank = 4
                                                   
                                               if rank<=3:
                                                   if selectC[0][0] == selectC[1][0] and selectC[2][0] == selectC[3][0]:
                                                       if rank!=3:
                                                           rankChange = True
                                                       maxCard = selectC[3]
                                                       outputStr = '兩對'
                                                       rank = 3
                                                   elif selectC[1][0] == selectC[2][0] and selectC[3][0] == selectC[4][0]:
                                                       if rank!=3:
                                                           rankChange = True
                                                       maxCard = selectC[4]
                                                       outputStr = '兩對'
                                                       rank = 3
                                                   elif selectC[0][0] == selectC[1][0] and selectC[3][0] == selectC[4][0]:
                                                       if rank!=3:
                                                           rankChange = True
                                                       maxCard = selectC[4]
                                                       outputStr = '兩對'
                                                       rank = 3
                                                       
                                                   if rank<=2:  
                                                       if selectC[0][0] == selectC[1][0]:
                                                           if rank!=2:
                                                               rankChange = True
                                                           maxCard = selectC[1]
                                                           outputStr = '一對'
                                                           rank = 2
                                                        
                                                       elif selectC[1][0] == selectC[2][0]:
                                                           if rank!=2:
                                                               rankChange = True
                                                           maxCard = selectC[2]
                                                           outputStr = '一對'
                                                           rank = 2
                                                        
                                                       elif selectC[2][0] == selectC[3][0]:
                                                           if rank!=2:
                                                               rankChange = True
                                                           maxCard = selectC[3]
                                                           outputStr = '一對'
                                                           rank = 2
                                                        
                                                       elif selectC[3][0] == selectC[4][0]:
                                                           if rank!=2:
                                                               rankChange = True
                                                           maxCard = selectC[4]
                                                           outputStr = '一對'
                                                           rank = 2
                                                           
                                                       if rank==1:
                                                           if rank!=1:
                                                               rankChange = True 
                                                           maxCard = selectC[4]
                                                           outputStr = '單張'                                                            
                                                           rank = 1
                                                               
                        if rankChange:
                            rankChange=False
                            globalmaxCard = maxCard
                            #print(outputStr,'最大牌為',maxCard)
                        else:
                            if globalmaxCard!=maxCard:
                                globalmaxCard = compareCardStrength(globalmaxCard,maxCard)
                                #print(outputStr,'最大牌為',maxCard)
                        #print(' ')
    return CardTransfer,globalmaxCard,rank,outputStr

global PokerIndex
hands = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
handsValue = {'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'T':9,'J':10,'Q':11,'K':12,'A':13}
handRanks =['C','D','H','S']
allPoker_,PokerIndex =createPokers(hands,handRanks)

#random.shuffle(allPoker_)
#print(allPoker_)

#P1hands = allPoker_[0:2]
#P2hands = allPoker_[2:4]

#PublicCards = allPoker_[4:9]
#CardsSort,maxCard,rank,outputStr = evaluateHandsRank(['3S','3D'],['3H','5S','5C'])
#CardsSort,maxCard,rank,outputStr = evaluateHandsRank(['2D', '3D'],[ '4D', '5D', '6D', '7D', '8D'])
#CardsSort,maxCard,rank,outputStr = evaluateHandsRank(P1hands,PublicCards)
#print('排序後:',CardsSort,' 牌力:',outputStr,' 最大牌:',maxCard)
