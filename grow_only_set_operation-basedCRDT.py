"""
The below code is a grow only set implemented using state-based conflict free replicated data type 
"""

import random
import re

# Simulate local state manipulation and communcation between replicas 
def main():
    # replicas r0, r1 which receive local state manipulations
    r0 = grow_only_set()
    r1 = grow_only_set()
    # Distributed system R comprised of r0, r1
    R = [r0, r1]

    actions = []
    for i in range(100):
        # choose an actor and action
        actor_id = random.choice([0, 1])
        actor = R[actor_id]
        element = random.choice(list(range(100)))
        actions.append((actor, element)) # mark that we are adding this
        actor.local_add(element)

        # 1/20th of the time we send local ushared actions to the other actor  
        # and check that actions are included correctly 
        if random.choice(list(range(20))) == 0:
            other_actor = R[1 - actor_id]
            local_unshared_actions = actor.unshared_actions
            other_actor.remote_add(local_unshared_actions)
            actor.unshared_actions = []
            assert actor.A.issubset(other_actor.A)
            print("operations are included in replica")
    
    # share unshared actions one last time at the end 
    # and check that the states are equal!
    r0_unshared_actions = r0.unshared_actions
    r1_unshared_actions = r1.unshared_actions
    r0.remote_add(r1_unshared_actions)
    r1.remote_add(r0_unshared_actions)
    assert r0.A == r1.A
    print("simulation complete and replica states are equivalent")

# grow only set CRDT
class grow_only_set():

    def __init__(self):
        self.A = set()
        self.unshared_actions = []

    def local_add(self, e):
        self.A.add(e)
        self.unshared_actions.append("add(e)")

    def remote_add(self, remote_actions):
        for action in remote_actions:
            element = re.split('()', action)[1]
            print(element)
            self.local_add(element)

    def lookup(self, e):
        return e in self.A

    def compare(self, x):
        return self.A.issubset(x.A)

main()