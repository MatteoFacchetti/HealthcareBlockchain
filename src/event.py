import datetime

from blockchain import BlockChain, Block


def count_events(loc):
    events = []
    total_locals = loc.copy()
    for local in total_locals:
        try:
            if loc[local].player == "event":
                events.append(local)
        except AttributeError:
            continue
    return len(events), events


def add_incompatibilities(event, incompatibilities, loc):
    count, events = count_events(loc)
    for incompatibility in incompatibilities:
        for i in events:
            if i == incompatibility:
                loc[i].add_incompatibility(event.name)


class Event(BlockChain):
    """
    Event object. It could be a disease, a prescription, a surgery, etc.
    """

    def __init__(self, event, name, loc, incompatibilities=None, *args, **kw):
        super(BlockChain, self).__init__(*args, **kw)
        if incompatibilities is None:
            incompatibilities = []
        self.player = "event"
        self.name = name
        self.event = event
        self.blocks = [self.get_genesis_block()]
        self.incompatibilities = incompatibilities

        if not isinstance(incompatibilities, (list, type(None))):
            raise Exception("`incompatibilities` should be a `list` or `None`")
        add_incompatibilities(self, incompatibilities, loc)

    def add_block(self, patient, doctor):
        """
        Add a new block to the chain.

        Parameters
        ----------
        patient : :obj:`Patient`
            BlockChain relative to the patient that faced this event.
        doctor : :obj:`Doctor`
            BlockChain relative to the doctor that adds the event to the chain of the patient.
        """
        self.blocks.append(Block(len(self.blocks), event=self.event, name=self.name, player=self.player,
                                 doctor=doctor.name, timestamp=datetime.datetime.utcnow(), patient=patient.name,
                                 previous_hash=self.blocks[len(self.blocks) - 1].hash))

    def add_incompatibility(self, incompatibility):
        """
        Add an incompatibility.

        Parameters
        ----------
        incompatibility : str
            Name of the event that is not compatible with this event.
        """
        self.incompatibilities.append(incompatibility)
