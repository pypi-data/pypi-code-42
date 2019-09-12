from functools import reduce
from operator import or_
import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.data import race_townhalls

import enum


class Hydralisk(sc2.BotAI):
    def select_target(self):
        if self.enemy_structures.exists:
            return random.choice(self.enemy_structures).position

        return self.enemy_start_locations[0]

    async def on_step(self, iteration):
        larvae = self.units(LARVA)
        forces = self.units(ZERGLING) | self.units(HYDRALISK)

        if self.units(HYDRALISK).amount > 10 and iteration % 50 == 0:
            for unit in forces.idle:
                self.do(unit.attack(self.select_target()))

        if self.supply_left < 2:
            if self.can_afford(OVERLORD) and larvae.exists:
                self.do(larvae.random.train(OVERLORD))
                return

        if self.structures(HYDRALISKDEN).ready.exists:
            if self.can_afford(HYDRALISK) and larvae.exists:
                self.do(larvae.random.train(HYDRALISK))
                return

        if not self.townhalls.exists:
            for unit in self.units(DRONE) | self.units(QUEEN) | forces:
                self.do(unit.attack(self.enemy_start_locations[0]))
            return
        else:
            hq = self.townhalls.first

        for queen in self.units(QUEEN).idle:
            abilities = await self.get_available_abilities(queen)
            if AbilityId.EFFECT_INJECTLARVA in abilities:
                self.do(queen(EFFECT_INJECTLARVA, hq))

        if not (self.structures(SPAWNINGPOOL).exists or self.already_pending(SPAWNINGPOOL)):
            if self.can_afford(SPAWNINGPOOL):
                await self.build(SPAWNINGPOOL, near=hq)

        if self.structures(SPAWNINGPOOL).ready.exists:
            if not self.townhalls(LAIR).exists and hq.is_idle:
                if self.can_afford(LAIR):
                    self.do(hq.build(LAIR))

        if self.townhalls(LAIR).ready.exists:
            if not (self.structures(HYDRALISKDEN).exists or self.already_pending(HYDRALISKDEN)):
                if self.can_afford(HYDRALISKDEN):
                    await self.build(HYDRALISKDEN, near=hq)

        if self.gas_buildings.amount < 2 and not self.already_pending(EXTRACTOR):
            if self.can_afford(EXTRACTOR):
                drone = self.workers.random
                target = self.vespene_geyser.closest_to(drone.position)
                err = self.do(drone.build(EXTRACTOR, target))

        if hq.assigned_harvesters < hq.ideal_harvesters:
            if self.can_afford(DRONE) and larvae.exists:
                larva = larvae.random
                self.do(larva.train(DRONE))
                return

        for a in self.gas_buildings:
            if a.assigned_harvesters < a.ideal_harvesters:
                w = self.workers.closer_than(20, a)
                if w.exists:
                    self.do(w.random.gather(a))

        if self.structures(SPAWNINGPOOL).ready.exists:
            if not self.units(QUEEN).exists and hq.is_ready and hq.is_idle:
                if self.can_afford(QUEEN):
                    self.do(hq.train(QUEEN))

        if self.units(ZERGLING).amount < 20 and self.minerals > 1000:
            if larvae.exists and self.can_afford(ZERGLING):
                self.do(larvae.random.train(ZERGLING))


def main():
    sc2.run_game(
        sc2.maps.get("(2)CatalystLE"),
        [Bot(Race.Zerg, Hydralisk()), Computer(Race.Terran, Difficulty.Medium)],
        realtime=False,
        save_replay_as="ZvT.SC2Replay",
    )


if __name__ == "__main__":
    main()
