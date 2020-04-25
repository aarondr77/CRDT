"""
The below code is a grow only set implemented using state-based conflict free replicated data type 
"""

import random

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
        actor.add(element)

        # 1/20th of the time we merge and check that the actor's  
        # state is included in the other actor's state after merge
        if random.choice(list(range(20))) == 0:
            other_actor = R[1 - actor_id]
            other_actor.merge(actor)
            #print(f"{other_actor.A} : {actor.A}")
            assert actor.A.issubset(other_actor.A)
            print("merged state is included in replica")
    
    # Merge one last time at the end 
    # and check that the states are equal!
    r0.merge(r1)
    r1.merge(r0)
    assert r0.A == r1.A
    print("simulation complete and replica states are equivalent")

# grow only set CRDT
class grow_only_set():

    def __init__(self):
        self.A = set()

    def add(self, e):
        self.A.add(e)

    def lookup(self, e):
        return e in self.A

    def compare(self, x):
        return self.A.issubset(x.A)
    
    def merge(self, x):
        self.A = self.A.union(x.A)

main()