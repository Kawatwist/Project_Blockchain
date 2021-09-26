# Blockchain
### The blockchain is split in differents parts :
1. Nodes
    * [Genesis (Master/MainNode)](#Genesis_FullNode)
    * Full Node (SubMaster/Full)
    * [Light (Validator/Slave)](#Light)
    * Archive
    * Lightweight
2. Inter-connection
3. Package
4. Validation
5. Block Insertion
6. What the fork ?!
7. Centralized or Not
8. Data type saved ?
9. With Contract
10. Minning ? Fuel ? What's thats
11. Proof of work Vs Proof of Stake
***

> A lot of differents node exist but for a basic blockchain we will take only this

|Name|Create Block|Validation|Add Block|Have is own blockchain|User Connection|Mempool|
|----| :----:     | :----:   | :----:  | :----:               | :----:        | :----: |
|Genesis|X|X|X|X|X|X|
|Full|X|X|X|X|X|X|
|Light|X|X|||X||
|Archive|||X|X||X|
|Lightweight|X||||X||
***
## Genesis_FullNode
>### **Genesis or Full node ? What's the difference ?**
>Basicly they are the same at one exception, the genesis is the original node create
>
>### **Why separate them in 2 node if they are the same ?**
>i don't know... Maybe its easier to differenciate them

---
## Light
>### **Why use Light node if it need an blockchain on side to work ?**
>The advantage to have light node is to not support a full blockchain,
>it's the better choice if you have a quite big blockchain without a lot of memory
>### **Why use Full node if you have the same memoryless?**
>Full node dosnt have the same Job, the Fullnode have he's own blockchain, validation block and mempool
>The lightnode is not used to mine, it's more like a checker
