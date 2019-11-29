from hashlib import sha256
from math import *
consistent=[False,0]
class MerkleNode:
    """
    Stores the hash and the parent.
    """
    def __init__(self, hash,mes):
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.mes=mes


class MerkleTree:
    
    
    def __init__(self, data_chunks,flg,op):
        leaves = []

        for chunk in data_chunks:
            node = MerkleNode(self.compute_hash(chunk),1)
            leaves.append(node)

        self.root = self.build_merkle_tree(leaves,flg,op)
        self.leat=leaves
        

    def build_merkle_tree(self, leaves,flg,op):
        
        num_leaves = len(leaves)
        if num_leaves == 1:
            return leaves[0]

        parents = []

        i = 0
        while i < num_leaves:
            left_child = leaves[i]
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child

            parents.append(self.create_parent(left_child, right_child,flg,op))

            i += 2

        return self.build_merkle_tree(parents,flg,op)

    def create_parent(self, left_child, right_child,flg,op):
        """
        Creates the parent node from the children, and updates
        their parent field.
        """
        global comp
        
      
        if left_child==right_child:
           height=left_child.mes
        else :   
           height=left_child.mes+right_child.mes
        parent = MerkleNode(self.compute_hash(left_child.hash + right_child.hash),height)
        if (ceil(log2(parent.mes)) == floor(log2(parent.mes))) and parent.mes>consistent[1]:
           consistent[1]=log2(parent.mes) 
           comp=parent.hash  

        if flg:
            if op==parent.hash:
               consistent[0]= True   

        left_child.parent, right_child.parent = parent, parent
        parent.left_child=left_child
        parent.right_child=right_child
        if choice==1:
            print("\nLeft child: {}, Right child: {}, Parent: {} ".format(left_child.hash, right_child.hash, parent.hash))
        print("parent_height: ",end=" ")
        print(parent.mes)    
        return parent

    @staticmethod
    def compute_hash(data):
        data = data.encode('utf-8')
        return sha256(data).hexdigest()

   
    def get_audit_trail(self, chunk_hash):
        """
        Checks if the leaf exists, and returns the audit trail
        in case it does.
        """
        for leaf in self.leat:
            if leaf.hash == chunk_hash:
                print("Leaf exists")
                # p=[]
                return self.generate_audit_trail(leaf)
        return False

    def generate_audit_trail(self, merkle_node, trail=[]):
        
        if merkle_node == self.root:
            trail.append(merkle_node.hash)
            return trail

        # check if the merkle_node is the left child or the right child
        is_left = merkle_node.parent.left_child == merkle_node
        #print(is_left)
        #print(merkle_node.parent.left_child)
        if is_left:
            # since the current node is left child, right child is
            # needed for the audit trail. We'll need this info later
            # for audit proof.
            print('right childs hash: '+merkle_node.parent.right_child.hash)
            trail.append((merkle_node.parent.right_child.hash, "right"))
            return self.generate_audit_trail(merkle_node.parent, trail)
        else:
            print('left childs hash: '+merkle_node.parent.left_child.hash)
            trail.append((merkle_node.parent.left_child.hash, "left"))
            return self.generate_audit_trail(merkle_node.parent, trail)
        #else:
         #   print('nothing added ')  


    def verify_audit_trail(self,chunk_hash, audit_trail):
    
        proof_till_now = chunk_hash
        print('starting node:',end=" ")
        print(proof_till_now)
        for node in audit_trail[:-1]:
            hash = node[0]
            print("node: ",end=" ")
            print(hash)

            is_left = node[1]=='left'
            if is_left:
            # the order of hash concatenation depends on whether the
            # the node is a left child or right child of its parent
                 proof_till_now = MerkleTree.compute_hash(str(hash) + proof_till_now)
            else:
                 proof_till_now = MerkleTree.compute_hash(proof_till_now + str(hash))
            print('proof_till_now: ',end=" ")
            print(proof_till_now)
    
    # verifying the computed root hash against the actual root hash
        print("proof_cal: ",end=" ")
        print(proof_till_now)
        print("root_hash: ",end=" ")
        print(audit_trail[-1])
        return proof_till_now == audit_trail[-1]   

    def return_comp(self):
        return comp



def main():
    print('Enter file:')
    file = input()
    chunks = list(file)
    global choice
    print("Enter the choice: ")
    print("press 1 for printing merkle tree and 2 for not printing: ")

    choice=int(input())
    #print("press 1 for printing the tree\n 2.Not printing")


    merkle_tree = MerkleTree(chunks,0,0)
    print('Roothash is:')
    print(merkle_tree.root.hash)
    
    global choice2                      
    print("Enter the 1 for Audit proof")
    choice2 = int(input())

    if choice2==1:
        print("Enter the chunk which you want to verify:")
        ver_chunk=input()
        chunk_hash = MerkleTree.compute_hash(ver_chunk)

        audit_trail = merkle_tree.get_audit_trail(chunk_hash)
        print('hashes provided by server are: ')
        print(audit_trail)
        if audit_trail is not False:
                    k=merkle_tree.verify_audit_trail(chunk_hash,audit_trail)
                    if k==True:
                        print('Chunk is present')   
        else:
            print("chunk not found") 
    
    print("Enter  1 for demonstrating Consistency proof: ")
    choice2=int(input())


    if choice2==1:
        print("*****The tree with the following root hash should be present in the new tree****")
        hig_pow=merkle_tree.return_comp()  
        print(hig_pow)
        print("\n")
    
        print('Enter new file:')
        file = input()
        chunks = list(file)
        merkle_tree = MerkleTree(chunks,1,hig_pow)
    
        print(consistent[0])

        
    print('thank you')

if __name__ == '__main__':

    main()


  