from .Command import Command

from state import Bullet

class ShootCommand(Command):
    def __init__(self,state,unit):
        self.state = state
        self.unit = unit
    def run(self):
        if self.unit.status != "alive":
            return
        if self.state.epoch-self.unit.lastBulletEpoch < self.state.bulletDelay:
            return
        self.unit.lastBulletEpoch = self.state.epoch
        self.state.bullets.append(Bullet(self.state,self.unit))
        self.state.notifyBulletFired(self.unit)# -*- coding: utf-8 -*-

