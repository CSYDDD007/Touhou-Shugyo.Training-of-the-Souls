
import effect
import SoundManager
import background

from const import *
from global_var import *
        
class GameController():
    def __init__(self, node_lists):
        self.lastFrame = 0
        self.node_lists = node_lists
        self.idx = 0
        
    def update(self, enemies, bullets, effects, backgrounds, frame, screen):
        self.lastFrame += 1
        if self.lastFrame == 1:
            a = background.Layer()
            a.initial('Forest', 1, (0,0), (-1, -3))
            b = background.Background()
            b.layers.append(a)
            backgrounds.add(b)
            eff = effect.StageFadeInFadeOut()
            eff.lastFrame = 120
            effects.add(eff)
            SoundManager.BGM_Play("Stage_1_Mid", -1, 1)
        for i in get_value('effects'):
            if i.__class__.__name__ == 'StageFadeInFadeOut':
                return
        if self.idx >= len(self.node_lists):
            set_value('state', 'pause')
            set_value('finish', 1)
            print(1)
            return
        self.node_lists[self.idx].update({})
        if self.node_lists[self.idx].state == 'wait_to_do':
            effects.add(effect.StageFadeInFadeOut())
            self.idx += 1