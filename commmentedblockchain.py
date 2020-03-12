import hashlib
import datetime

#for a simple blockchain, we require only two classes: block and blockchain


class Block:
    blkno=0    
    blkdata=None 
    hash=None               
    next=None           #pointer to the next block
    nonce=0   #it is a 32-bit number, which miners need to adjust so that the encrypted hash of the block is lesser than the current target of the network
    previous_hash=0x0  #hash of the previous block
    timestamp=datetime.datetime.now()  #measures the time when the block was created, if its a valid block, it will be added to the blockchain


    #next, we use some constructors(functions) which give values to the above class attributes when an object is instantiated


    def __init__(self,data):
        self.blkdata=data

    def hash(self):                             #all these class attrributes are encrypted using utf-8 algo, and the net string is encrypted using sha 256
        h=hashlib.sha256()                  
        h.update(
        str(self.nonce).encode('utf-8')+
        str(self.blkdata).encode('utf-8')+
        str(self.previous_hash).encode('utf-8')+
        str(self.timestamp).encode('utf-8')+
        str(self.blkno).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: "+ str(self.hash()) + "\nBlockNo:" + str(self.blkno) + "\nBlockdata:" + str(self.blkdata)+"\nTimestamp:"+str(self.timestamp) +"\nHashes:"+str(self.nonce) +"\n----------"
    


class Blockchain:
    
    decider=15
    target=2**(256-decider)     #smaller the target, more robust is the process of generating a valid hash
    max_nonce=2**32 -1            #since nonce is a 32 bit no, the max_nonce is the max value of nonce that miners could try

    block=Block("Genesis")        #block represents the last block of the blockchain
    head=block                  #it is the head of any blockchain until a block is added


    #we mine a block and then add it to the blockchain using the following constructors


    def add(self,block):
        block.previous_hash=self.block.hash()
        block.blkno=self.block.blkno+1
        self.block.next=block            #block is the last block of the blockchain, and newblock is the new block being added
        self.block=self.block.next          #now newblock will become block, i.e. the last block of the blockchain, so it took the value of the block that was just added

    def mine(self,block):
        for i in range(self.max_nonce):
            if int(block.hash(), 16) <= self.target:    #checks if the blockhash is less than the target specified for the blockchain
                self.add(block)
                #print(block)
                break
            else:
                block.nonce += 1                        #if the hash is invalid, try with a different value of nonce
    



#we create an instance of the blockchain class
myfirstblockchain=Blockchain()      #myfirstblockchain will be assigned its class attributes, i.e. the target, genesis block etc.

for j in range(15):
    myfirstblockchain.mine(Block("Block"+str(j+1)))    #everytime the mine function is called, it adds a block to the blockchain      

while myfirstblockchain.head!=None:                             #for our blkchain, initially, head is the genesis block
    print(myfirstblockchain.head)
    myfirstblockchain.head=myfirstblockchain.head.next
     

# print(myfirstblockchain.head.hash()) everytime we call hash() function for the genesis block, it creates a new hash
# print(myfirstblockchain.block.hash())


# print(myfirstblockchain.block.hash())             block.hash() will change only when the class attributes of block are changed
# myfirstblockchain.block.blkdata='new'
# print(myfirstblockchain.block.hash())