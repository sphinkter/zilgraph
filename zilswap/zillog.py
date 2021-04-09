# -*- coding: utf-8 -*-

from pyzil.account import Account

from zilswap import zilswap

import time

import pymongo
import json

    
class zillog:
    def __init__(self, password=""):
        
        # Configure MongoDB
        self.mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mongodb = self.mongoclient["zillog"]
        
        # Load Zilgraph JSON 
        fp_json = open("zilgraph.json")
        self.tokens = json.load(fp_json)["tokens"]
        
        # Setup dictionaries
        self.token = {}
        for tok in self.tokens:
            self.token[tok]      = self.mongodb[tok]
        
        # Wallet address
        # addr = "zil1y7kr7nh28p5j3tv76jm5nkp2yq56j8xwsq5utr"
        addr = "zil1ekstgkgqdjh3k6xjtn0x47p49t7dlfentla8rs"
        
        # Load account from private key
        account = Account(address=addr)
        
        # Instantiate zilswap class
        self.zwap = zilswap(password)        
        
        
        
        
    def run(self, debug=False):
        
        for tok in self.token:
            # Get market data and insert in database
            try:    
                new_entry = self.zwap.get_market(tok)
                self.token[tok].insert_one(new_entry)
                print(new_entry)
            except:
                print("Error: MongoDB insert_one() " + tok)


            # Print database
            if debug:
                for x in self.token[tok].find():
                    print(x)
            
    def rund(self, tstep=10):
        while True:
            self.run(debug=False)
            time.sleep(1)
            while int(time.time())%tstep != 0:
                time.sleep(0.1)
    
    
    
    def mrproper(self):
        for tok in self.token:
            self.token[tok].delete_many({})
            
            
