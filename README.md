# CRDT

This repository was created for my senior undergraduate thesis. 

## Introduction
As distributed systems have become a part of everyday life and the backbone for important infrastructure, the desired properties of them have evolved.  It is no longer our desire for these systems to behave as if it were one computer – preferring the system to become unavailable than to have differences in the state of replicas. Instead, we now prefer that systems are always available.  The CAP Theorem, proposed by Brewer, tells us we must sacrifice strong consistency  to have availability and partition tolerance.  As a result, the industry decided to tolerate temporary inconsistencies in the state of replicas in order to maximize availability. 

Eventual consistency dictates that once an operation is applied to one replica in the distributed system, it will eventually be applied to all replicas and that eventually the state of all replicas will converge.   Many eventual consistency models have complex conflict resolution processes which requires replicas to roll back state.  Strong eventual consistency is a subset of eventual consistency with the additional specification that any replicas that received the same updates have identical state.  In strong eventual consistent systems, replicas are immediately consistent “as soon as they have received all of the same transactions.”  

One way to achieve strong eventual consistency is through conflict free replicated data types (CRDTs).  CRDT’s are a specification of distributed datatypes that are designed to support the divergence of replica state, while guaranteeing that they will eventually converge by resolving conflicting updates in a deterministic manner.   Deterministic conflict resolution is possible due to metadata stored in the structure of the datatype.  There are two primary types of CRDT’s, state-based (convergent) replicated data types and operation-based (commutative) replicated data types. These types differ in how they store their metadata. State-based data types encapsulate the metadata within the state itself whereas operation-based data types rely on the replication protocol.  

Strong eventual convergence is a property applied to real-time collaborative editing systems.  Clients update their state locally to ensure an immediate response to the user’s input, and once other clients receive that input, the state of the receiving client should be updated as well.  Google Docs is implemented using operational transforms, a system of adapting the received operation to ensure that the intent of the operation is not affected during its application due to concurrent updates to the state by other clients.  In theory, operational transforms are intuitive, but in practice they are extremely difficult to implement.  

This paper proposes an operation based CRDT implementation of a real-time collaborative text editor. 

## Run the Code

```
git clone 
cd text-editor-operation-basedCRDT/
python3 main.py
```
