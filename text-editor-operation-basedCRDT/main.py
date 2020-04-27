import string
import random
from client import client

def main():
    
    # replicas r0, r1 which receive local state manipulations
    r0 = client("site 0")
    r1 = client("site 1")
    
    # Distributed system R comprised of r0, r1
    R = [r0, r1]

    #Start each client on the same document
    r0.local_insert("A", "0")
    r1.local_insert("A", "0")

    actions = []

    for i in range(100):
        # choose an actor
        actor_id = random.choice([0, 1])
        actor = R[actor_id]
        # choose an action, element and location 
        action = random.uniform(0, 1)
        if action < .8:
            # insert action
            element = random.choice(string.ascii_letters)
            # choose the id of the node to insert after
            if len(actor.element_mapping) == 0:
                id = "0"
            else:
                id = random.choice(actor.element_mapping)[1]
            # insert locally
            actor.local_insert(element, id)
        else: 
            # delete action
            if not len(actor.element_mapping) == 0:
                (element, id) = random.choice(actor.element_mapping)
                actor.local_delete(element, id)

        actions.append((actor.site_id, action, element, id)) # mark that we are adding this
        

        # 1/20th of the time we send local ushared actions to the other actor  
        # and check that actions are included correctly 
        if random.choice(list(range(20))) == 0:
            other_actor = R[1 - actor_id]
            local_unshared_actions = actor.unshared_operations
            other_actor.remote_operations(local_unshared_actions)
            actor.unshared_operations = []
            print("merged the actions of: " + actor.site_id + " into: " + other_actor.site_id)
        
    
    # share unshared actions one last time at the end 
    # and check that the states are equal!
    r0_unshared_actions = r0.unshared_operations
    r1_unshared_actions = r1.unshared_operations
    r0.remote_operations(r1_unshared_actions)
    r1.remote_operations(r0_unshared_actions)

    assert r0.compare(r1)
    print("simulation complete and replica states are equivalent")

main()