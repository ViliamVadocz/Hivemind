# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class RenderMessage(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsRenderMessage(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RenderMessage()
        x.Init(buf, n + offset)
        return x

    # RenderMessage
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # RenderMessage
    def RenderType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 1

    # RenderMessage
    def Color(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from .Color import Color
            obj = Color()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

# /// For 2d renders this only grabs x and y
    # RenderMessage
    def Start(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = o + self._tab.Pos
            from .Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

# /// For 2d renders this only grabs x and y
    # RenderMessage
    def End(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = o + self._tab.Pos
            from .Vector3 import Vector3
            obj = Vector3()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

# /// Scales the x size of the text/rectangle, is used for rectangles assuming an initial value of 1
    # RenderMessage
    def ScaleX(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 1

# /// Scales the y size of the text/rectangle, is used for rectangles assuming an initial value of 1
    # RenderMessage
    def ScaleY(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 1

    # RenderMessage
    def Text(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return bytes()

# /// Rectangles can be filled or just outlines.
    # RenderMessage
    def IsFilled(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

def RenderMessageStart(builder): builder.StartObject(8)
def RenderMessageAddRenderType(builder, renderType): builder.PrependInt8Slot(0, renderType, 1)
def RenderMessageAddColor(builder, color): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(color), 0)
def RenderMessageAddStart(builder, start): builder.PrependStructSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(start), 0)
def RenderMessageAddEnd(builder, end): builder.PrependStructSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(end), 0)
def RenderMessageAddScaleX(builder, scaleX): builder.PrependInt32Slot(4, scaleX, 1)
def RenderMessageAddScaleY(builder, scaleY): builder.PrependInt32Slot(5, scaleY, 1)
def RenderMessageAddText(builder, text): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(text), 0)
def RenderMessageAddIsFilled(builder, isFilled): builder.PrependBoolSlot(7, isFilled, 0)
def RenderMessageEnd(builder): return builder.EndObject()