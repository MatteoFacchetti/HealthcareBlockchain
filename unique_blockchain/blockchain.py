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
    def __init__(self, Minister):
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

    def new_authorization(self, recipient, fee):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'type': 'authorization',
            'sender': self.Minister,
            'recipient': recipient,
            'authorization': self.Minister.generate_authorization(recipient),
            'fee': fee
        })

        return self.last_block['index'] + 1

    def new_prescription(self, sender, recipient, prescription, fee):

        self.current_transactions.append({
            'type': 'prescription',
            'sender': sender,
            'recipient': recipient,
            'prescription': prescription,
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
        data = [str(transaction) for transaction in block['transactions']]
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(data, sort_keys=True).encode()
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

    def verify_authorizations(self):
        c = 0
        to_be_deleted = []
        for transaction in self.current_transactions:
            if transaction['type'] == 'authorization':
                try:
                    authorization = transaction['authorization']
                    public_key = self.Minister.public_key
                    public_key = nacl.signing.VerifyKey(public_key, encoder=nacl.encoding.HexEncoder)
                    public_key.verify(authorization)

                except:
                    to_be_deleted.append(c)

            else:
                try:
                    authorization = transaction['sender'].authorization
                    public_key = self.Minister.public_key
                    public_key = nacl.signing.VerifyKey(public_key, encoder=nacl.encoding.HexEncoder)
                    public_key.verify(authorization)

                except:
                    to_be_deleted.append(c)
                    print('Not valid Doctor authorization')
                if transaction['type'] == 'prescription':
                    try:
                        incompatibilites = self.Minister.incompatibilities
                        if transaction['prescription'] in incompatibilites.keys():
                            prescription = transaction['prescription']
                            illnesses_inc = set(self.Minister.incompatibilities[prescription])
                            illnesses_patient = set(transaction['recipient'].illnesses)
                            assert len(illnesses_inc.intersection(illnesses_patient)) == 0
                    except:
                        to_be_deleted.append(c)
                        print('Incompatibility of one prescription with the history of the patient')
            c += 1
        new_transactions = []
        for i in range(len(self.current_transactions)):
            if i not in to_be_deleted:
                new_transactions.append(self.current_transactions[i])
        self.current_transactions = new_transactions

    def add_wallett(self, block):
        transactions = block['transactions']
        for transaction in transactions:
            if transaction['type'] == 'diagnosis':
                recipient = transaction['recipient']
                illness = transaction['illness']
                recipient.illnesses.append(illness)
            if transaction['type'] == 'authorization':
                recipient = transaction['recipient']
                authorization = transaction['authorization']
                recipient.authorization = authorization

    def mine(self):
        last_block = self.last_block
        last_proof = last_block['nounce']
        nounce = self.proof_of_work(last_proof)

        # Forge the new Block by adding it to the chain
        previous_hash = self.hash(last_block)
        self.verify_authorizations()
        block = self.new_block(nounce, previous_hash)
        self.add_wallett(block)


############################# Doctor, Patient and Minister (acting as nodes) ##############################
#todo: implementing class Miner
class Doctor:
    def __init__(self, name):
        self.name = name
        self.address = self.get_address(name)
        self.authorization = None

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()

class Patient:
    def __init__(self, name):
        self.name = name
        self.address = self.get_address(name)
        self.illnesses = []

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
        self.incompatibilities = {'medicine1': ['illness1', 'illness2'],
                                  'medicine2': ['illness1'],
                                  'medicine3': ['illness2', 'illness3']}

    def get_address(self, name):
        key = hashlib.sha256()
        key.update(name.encode('utf-8'))
        return key.hexdigest()

    def generate_authorization(self, doctor):
        assert isinstance(doctor, Doctor)
        signed = self.minister_key.sign(bytes(doctor.address, 'utf-8'))
        return signed





doctor1 = Doctor('Doctor Muller')
patient1 = Patient('Mr. Black')
doctor2 = Doctor('Doctor Johannes')
patient2 = Patient('Mr. Green')
patient3 = Patient('Mr. White')

# Initiate Blockchain
Health_block = Blockchain(Minister)

print('--------------------diagnosis without authorization-------------------')

# Doctor2 tries to make diagnosis to different patients
Health_block.new_transaction(doctor2, patient1, 'illness2', 0.20)
Health_block.new_transaction(doctor2, patient3, 'illness3', 0.20)
Health_block.new_transaction(doctor2, patient3, 'illness1', 0.20)
print('patient1 illness history: ' + str(patient1.illnesses))
print('patient2 illness history: ' + str(patient2.illnesses))
print('patient3 illness history: ' + str(patient3.illnesses))
Health_block.mine()

# If we look inside the wallet of each patient we do not see any illness because the doctor2 has no authorization
# Now let's make an authorization from Minister to doctor1
print('--------------------diagnosis with authorization-------------------')
Health_block.new_authorization(doctor1, 0.50)
Health_block.mine()

# Now the doctor2 makes a new diagnosis to patient3
Health_block.new_transaction(doctor1, patient3, 'illness1', 0.20)

Health_block.mine()


# If we look a the history of patient3 we see the illness
print('patient3 illness history: '+str(patient3.illnesses))

# Now let's print the authorizations of both the doctors
print('doctor2 authorization: '+str(doctor2.authorization))
print('doctor1 authorization: '+str(doctor1.authorization))

print('--------------------prescription-------------------')
# Let's do a prescription
Health_block.new_prescription(doctor1, patient3, 'medicine3', 0.20)
Health_block.mine()

# Let's try to do a prescription incompatible with the illnesses of patient3
Health_block.new_prescription(doctor1, patient3, 'medicine1', 0.20)
Health_block.mine()

print('--------------------faake authorization-------------------')
# Now let's try to create a fake authorization.
private_key_random = nacl.signing.SigningKey.generate()
signed = private_key_random.sign(bytes(doctor2.address, 'utf-8'))
doctor2.authorization = signed

print(doctor2.authorization)
Health_block.new_transaction(doctor2, patient1, 'illness2', 0.20)
Health_block.mine()
print(Health_block.chain)
