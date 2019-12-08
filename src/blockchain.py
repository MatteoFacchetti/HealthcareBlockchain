import hashlib
import datetime
import pandas as pd


class Block:
    """
    Minimal block containing an index, a timestamp, the data to store and the previous hash.
    """

    def __init__(self, index, name, player, timestamp, previous_hash,
                 doctor=None, data=None, kind=None, patient=None, event=None):
        self.index = index
        self.player = player
        self.event = event
        self.name = name
        self.timestamp = timestamp
        self.kind = kind
        self.patient = patient
        self.doctor = doctor
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
            return pd.DataFrame({"Block summary": [self.index, self.name, self.doctor, self.timestamp, self.kind,
                                                   self.data, self.previous_hash, self.hash]},
                                index=["Index", "Name", "Doctor", "Timestamp", "Event", "Kind",
                                       "Previous hash", "Hash"])

        if self.player == "event":
            return pd.DataFrame({"Block summary": [self.index, self.name, self.doctor, self.timestamp, self.patient,
                                                   self.previous_hash, self.hash]},
                                index=["Index", "Name", "Doctor", "Timestamp", "Patient",
                                       "Previous hash", "Hash"])

        if self.player == "doctor":
            return pd.DataFrame({"Block summary": [self.index, self.name, self.patient, self.timestamp, self.kind,
                                                   self.data, self.previous_hash, self.hash]},
                                index=["Index", "Name", "Patient", "Timestamp", "Event", "Kind",
                                       "Previous hash", "Hash"])


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
        for i in range(1, len(self.blocks)):
            if self.blocks[i].index != i:
                return False, f'Wrong block index at block {i}.'
            if self.blocks[i - 1].hash != self.blocks[i].previous_hash:
                return False, f'Wrong previous hash at block {i}.'
            if self.blocks[i].hash != self.blocks[i].hashing():
                return False, f'Wrong hash at block {i}.'
            if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                return False, f'Backdating at block {i}.'
        return True

    def get_block(self, n):
        """
        Return block `n` in the chain.

        Parameters
        ----------
        n : int
            Index of the block to be returned.
        """
        return self.blocks[n].summary()

    def get_chain(self):
        """
        Return a pandas DataFrame containing all the blocks of the chain.

        Returns
        -------
        chain : pandas.DataFrame
        """
        chain = pd.DataFrame()
        for block in self.blocks:
            block_T = block.summary().T
            chain = chain.append(block_T)
        chain.set_index("Index", inplace=True)
        return chain
