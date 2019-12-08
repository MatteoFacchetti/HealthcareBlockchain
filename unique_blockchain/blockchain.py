import hashlib
import json
from time import time
import nacl.encoding
import nacl.signing
import base64


signing_key = nacl.signing.SigningKey.generate()
signed = signing_key.sign(b"Attack at Dawn")
verify_key = signing_key.verify_key
verify_key_hex = verify_key.encode(encoder=nacl.encoding.HexEncoder)


verify_key = nacl.signing.VerifyKey(verify_key_hex,
                                    encoder=nacl.encoding.HexEncoder)
verify_key.verify(signed)
verify_key.verify(signed.message, signed.signature)


class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block
        self.new_block(previous_hash=1, nounce=100)

        self.wallett = {}
        self.Minister = Minister()

    def new_block(self, nounce, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'nounce': nounce,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, illness, fee):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'type': 'diagnosis',
            'sender': sender,
            'recipient': recipient,
            'illness': illness,
            'fee': fee
        })

        return self.last_block['index'] + 1

    def new_authorization(self, sender, recipient, authorization, fee):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'type': 'authentication',
            'sender': sender,
            'recipient': recipient,
            'authorization': authorization,
            'fee': fee
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        nounce = 0
        while self.valid_proof(last_proof, nounce) is False:
            nounce += 1

        return nounce

    @staticmethod
    def valid_proof(last_proof, nounce):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{nounce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "00"

 #   def wallett(self, address):
 #       return {}

    def verify_authentications(self):
        c = 0
        for transaction in self.current_transactions:
            if transaction['type'] == 'authentication':
                try:
                    authentication = transaction['authorization']
                    self.Minister.public_key.verify(transaction['recipient'], authentication)
                except:
                    self.current_transactions.pop(c)
                c += 1


    def add_wallett(self, block):
        transactions = block['transactions']
        for transaction in transactions:
            if transaction['type'] == 'diagnosis':
                recipient = transaction['recipient']
                illness = transaction['illness']
                if recipient not in self.wallett:
                    self.wallett[recipient] = [illness]
                else:
                    self.wallett[recipient].append(illness)

    def mine(self):
        last_block = self.last_block
        last_proof = last_block['nounce']
        nounce = self.proof_of_work(last_proof)

        # Forge the new Block by adding it to the chain
        previous_hash = self.hash(last_block)
        self.verify_authentications()
        block = self.new_block(nounce, previous_hash)
        self.add_wallett(block)

        #for transaction in block['transactions']:
        #    transaction['signed_data']
        #    transaction['signature']

############################# Doctor and Patient ##############################

class Doctor:
    def __init__(self, name):
        self.name = name
        self.address = self.get_address(name)
        self.private_key = nacl.signing.SigningKey.generate()

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()

class Patient:
    def __init__(self, name):
        self.name = name
        self.address = self.get_address(name)

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()

class Minister:
    def __init__(self):
        self.name = 'Minister of Health'
        self.address = self.get_address(self.name)
        self.minister_key = nacl.signing.SigningKey.generate()
        public_key = self.minister_key.verify_key
        self.public_key = public_key.encode(encoder=nacl.encoding.HexEncoder)

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()

    def generate_autorization(self, doctor):
        assert isinstance(doctor, Doctor)
        signed = self.minister_key.sign(bytes(doctor.address, 'utf-8'))
        return signed.signature




doctor1 = Doctor('Doctor Muller')
patient1 = Patient('Mr. Black')
doctor2 = Doctor('Doctor Johannes')
patient2 = Patient('Mr. Green')

doctors = {doctor1.name: [doctor1.address, doctor1.private_key],
           doctor2.name: [doctor2.address, doctor2.private_key]}

Health_block = Blockchain()
Health_block.new_block
Health_block.new_transaction(doctor1.address, patient1.address, 'Celiachia', 0.20)
Health_block.new_transaction(doctor2.address, patient2.address, 'Miseales', 0.20)
Health_block.mine()
Health_block.new_transaction(doctor1.address, patient2.address, 'Insomnia', 0.20)
Health_block.new_authorization(Health_block.Minister.address, doctor1.address,
                               Health_block.Minister.generate_autorization(doctor1), 0.50)
Health_block.mine()
print(Health_block.chain)
print(Health_block.wallett)
print(type(doctor1.address))
