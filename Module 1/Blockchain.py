# Module 1 - Create a Blockchain

# importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain :
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {
                    'index' : len(self.chain) +1 ,
                    'timestamp' : str(datetime.datetime.now()),
                    'proof' : proof,
                    'previous_hash' : previous_hash
                }
        
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False :
            hash_operations = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operations[:4] == '0000' :
                check_proof = True
            else :
                new_proof+=1
        
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain) :
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operations = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operations[:4] != '0000' :
                return False
            previous_block = block
            block_index += 1
        
        return True
        


# Part 2 - Mining our Blockchain


# Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new Block 
# http://127.0.0.1:5000/
@app.route('/mine_block', methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_prev_block() 
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
                'message' : 'Congratulations you just mined a block',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                }
    return jsonify(response) , 200

# Getting the full blockchain
@app.route('/get_chain', methods = ['GET'])

def get_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain),
        }
    return jsonify(response) , 200

# Verifying the blockchain
@app.route('/is_valid', methods = ['GET'])

def is_valid():
    value = blockchain.is_chain_valid(blockchain.chain)
    if value is True :
        response = {
            'message' : 'Congratulations the chain is valid'
            }
        return jsonify(response) , 200
    else :
        response = {
            'message' : 'Sorry the chain is not valid'
            }
        return jsonify(response) , 200


# Running the App

app.run(host = '0.0.0.0' , port = 5000)










