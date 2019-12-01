import hashlib
import datetime
import pandas as pd


class Block:
    """
    Minimal block containing an index, a timestamp, the data to store and the previous hash.

    """

    def __init__(self, index, timestamp, data, previous_hash):
        """

        Parameters
        ----------
        index
        timestamp
        data
        previous_hash
        """
        self.index = index
        self.timestamp = timestamp
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
        return pd.DataFrame({"Block summary": [self.index, self.timestamp, self.data, self.previous_hash, self.hash]},
                            index=["Index", "Timestamp", "Data", "Previous hash", "Hash"])


def get_genesis_block():
    """
    Return the genesis block of a BlockChain.

    """
    return Block(index=0, timestamp=datetime.datetime.utcnow(), data="Genesis", previous_hash="0"*64)


class BlockChain:
    def __init__(self):
        """
        Always initialize a genesis block when creating a new chain.

        """
        self.blocks = [get_genesis_block()]

    def add_block(self, data):
        """
        Add a new block to the chain.

        """
        self.blocks.append(Block(len(self.blocks), timestamp=datetime.datetime.utcnow(), data=data,
                                 previous_hash=self.blocks[len(self.blocks) - 1].hash))

    def get_chain_size(self):
        """
        Return the length of the chain, excluding the genesis block
        """
        return len(self.blocks) - 1

    def verify(self, verbose=True):
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
                if verbose:
                    print(f'Wrong block index at block {i}.')
            if self.blocks[i - 1].hash != self.blocks[i].previous_hash:
                flag = False
                if verbose:
                    print(f'Wrong previous hash at block {i}.')
            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False
                if verbose:
                    print(f'Wrong hash at block {i}.')
            if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                flag = False
                if verbose:
                    print(f'Backdating at block {i}.')
        return flag
