import hashlib
import datetime
import pandas as pd


class Block:
    """
    Minimal block containing an index, a timestamp, the data to store and the previous hash.
    """

    def __init__(self, index, name, player, timestamp, previous_hash, data=None, kind=None, patient=None, event=None):
        self.index = index
        self.player = player
        self.event = event
        self.name = name
        self.timestamp = timestamp
        self.kind = kind
        self.patient = patient
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()

    def summary(self):
        if self.player == "patient":
            return pd.DataFrame({"Block summary": [self.index, self.name, self.timestamp, self.kind,
                                                   self.data, self.previous_hash, self.hash]},
                                index=["Index", "Name", "Timestamp", "Kind", "Data", "Previous hash", "Hash"])

        if self.player == "event":
            return pd.DataFrame({"Block summary": [self.index, self.name, self.timestamp, self.patient,
                                                   self.previous_hash, self.hash]},
                                index=["Index", "Name", "Timestamp", "Patient", "Previous hash", "Hash"])


class BlockChain:
    def __init__(self, player, name):
        """
        Always initialize a genesis block when creating a new chain.
        """
        self.name = name
        self.player = player
        self.blocks = [self.get_genesis_block()]

    def get_genesis_block(self):
        """
        Return the genesis block of a BlockChain.
        """
        return Block(index=0, player=self.player, name=self.name,
                     timestamp=datetime.datetime.utcnow(), previous_hash="0"*64)

    def get_chain_size(self):
        """
        Return the length of the chain, excluding the genesis block.
        """
        return len(self.blocks) - 1

    def verify(self):
        """
        Verify data integrity:

        * index in `blocks[i]` is `i`, there are no missing or extra blocks;
        * current and previous hashes are correct;
        * there is not any backdating.
        """
        flag = True
        for i in range(1, len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                print(f'Wrong block index at block {i}.')
            if self.blocks[i - 1].hash != self.blocks[i].previous_hash:
                flag = False
                print(f'Wrong previous hash at block {i}.')
            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False
                print(f'Wrong hash at block {i}.')
            if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                flag = False
                print(f'Backdating at block {i}.')
        return flag


def add_event(event, patient):
    """
    Add an event to the patient blockchain. This will in turn add the patient itself to the blockchain of the event.

    Parameters
    ----------
    event : :obj:`Event`
        The Blockchain relative to the event that the patient faces.
    patient : :obj:`Patient`
        The BlockChain relative to the patient that faces the event.
    """
    event.add_block(patient)
    patient.add_block(event)
