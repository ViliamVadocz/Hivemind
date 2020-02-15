# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class SphereShape(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsSphereShape(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = SphereShape()
        x.Init(buf, n + offset)
        return x

    # SphereShape
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # SphereShape
    def Diameter(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def SphereShapeStart(builder): builder.StartObject(1)
def SphereShapeAddDiameter(builder, diameter): builder.PrependFloat32Slot(0, diameter, 0.0)
def SphereShapeEnd(builder): return builder.EndObject()