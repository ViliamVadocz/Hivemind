# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

# /// A bot controlled by the RLBot framework
class RLBotPlayer(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsRLBotPlayer(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RLBotPlayer()
        x.Init(buf, n + offset)
        return x

    # RLBotPlayer
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

def RLBotPlayerStart(builder): builder.StartObject(0)
def RLBotPlayerEnd(builder): return builder.EndObject()