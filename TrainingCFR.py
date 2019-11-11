from config import dataPath,handRanks,hands
from games.gameRules import RootChanceGameState
from games.algorithms import ChanceSamplingCFR, VanillaCFR
import numpy as np

#載入牌型所有組合
CARDS_DEALINGS=[]
with open(dataPath+"CARDS_DEALINGS num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "r") as f:
    for line in f:
        CARDS_DEALINGS.append(str(line.strip()))

iterations = 10000
root = RootChanceGameState(CARDS_DEALINGS)
chance_sampling_cfr = ChanceSamplingCFR(root)
chance_sampling_cfr.run(iterations = iterations)

result = chance_sampling_cfr.sigma 
np.save('iter/sampling_cfr_iter'+str(iterations)+'final.npy', result) 

