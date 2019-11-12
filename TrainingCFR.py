from config import dataPath,handRanks,hands
from games.gameRules import RootChanceGameState
from games.algorithms import ChanceSamplingCFR, VanillaCFR
from lib.common import createFolder
import numpy as np

#載入牌型所有組合
CARDS_DEALINGS=[]
with open(dataPath+"CARDS_DEALINGS num"+str(len(hands))+",rank"+str(len(handRanks))+".txt", "r") as f:
    for line in f:
        CARDS_DEALINGS.append(str(line.strip()))
#存取CFR的資料夾位至
save_CFR_folder = 'iters/'
createFolder(save_CFR_folder)
iterations = 10000
root = RootChanceGameState(CARDS_DEALINGS)
chance_sampling_cfr = ChanceSamplingCFR(root)
chance_sampling_cfr.run(iterations = iterations,save_path = save_CFR_folder)

result = chance_sampling_cfr.sigma 
np.save(save_CFR_folder + '/sampling_cfr_iter'+str(iterations)+'final.npy', result) 

