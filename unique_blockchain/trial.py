from unique_blockchain.blockchain import Blockchain
from unique_blockchain.agents import Doctor, Miner, Patient, Minister
import nacl.signing


# Initiate Blockchain
Health_block = Blockchain(Minister, incompatibilities={'medicine1': ['illness1', 'illness2'],
                                  'medicine2': ['illness1'],
                                  'medicine3': ['illness2', 'illness3']})

miner1 = Miner(Health_block)
miner2 = Miner(Health_block)
miner3 = Miner(Health_block)
miner4 = Miner(Health_block)

doctor1 = Doctor('Doctor Muller')
doctor2 = Doctor('Doctor Johannes')
patient1 = Patient('Mr. Black')
patient2 = Patient('Mr. Green')
patient3 = Patient('Mr. White')

print(miner1.wallet, miner2.wallet, miner3.wallet, miner4.wallet)
miners = [miner1, miner2, miner3, miner4]
print('--------------------diagnosis without authorization-------------------')

# Doctor2 tries to make diagnosis to different patients
Health_block.new_diagnosis(doctor2, patient1, 'illness2', 0.20)
Health_block.new_diagnosis(doctor2, patient3, 'illness3', 0.20)
Health_block.new_diagnosis(doctor2, patient3, 'illness1', 0.20)
print('patient1 illness history: ' + str(patient1.illnesses))
print('patient2 illness history: ' + str(patient2.illnesses))
print('patient3 illness history: ' + str(patient3.illnesses))
Health_block.mine(miners)

# If we look inside the wallet of each patient we do not see any illness because the doctor2 has no authorization
# Now let's make an authorization from Minister to doctor1
print('--------------------diagnosis with authorization-------------------')
Health_block.new_authorization(doctor1, 0.50)
Health_block.mine(miners)
print('--------------------------------')
print('wallets')
print(miner1.wallet, miner2.wallet, miner3.wallet, miner4.wallet)
print('--------------------------------')
# Now the doctor2 makes a new diagnosis to patient3
Health_block.new_diagnosis(doctor1, patient3, 'illness1', 0.20)

Health_block.mine(miners)


# If we look a the history of patient3 we see the illness
print('patient3 illness history: '+str(patient3.illnesses))

# Now let's print the authorizations of both the doctors
print('doctor2 authorization: '+str(doctor2.authorization))
print('doctor1 authorization: '+str(doctor1.authorization))

print('--------------------prescription-------------------')
# Let's do a prescription
Health_block.new_prescription(doctor1, patient3, 'medicine3', 0.20)
Health_block.mine(miners)

# Let's try to do a prescription incompatible with the illnesses of patient3
Health_block.new_prescription(doctor1, patient3, 'medicine1', 0.20)
Health_block.mine(miners)

print('--------------------faake authorization-------------------')
# Now let's try to create a fake authorization.
private_key_random = nacl.signing.SigningKey.generate()
signed = private_key_random.sign(bytes(doctor2.address, 'utf-8'))
doctor2.authorization = signed

print(doctor2.authorization)
Health_block.new_diagnosis(doctor2, patient1, 'illness2', 0.20)
Health_block.mine(miners)
print(Health_block.chain)

print('--------------------------------')
print('wallets')
print(miner1.wallet, miner2.wallet, miner3.wallet, miner4.wallet)
print('--------------------------------')
print(miner1.wallet)

print('---------------------------------')
print("patient1's illnesses")
private_key = patient3.private_key
print(Health_block.get_patient_history(patient3, private_key=private_key))

# If we try again with the same private key the access is denied
print(Health_block.get_patient_history(patient3, private_key=private_key))