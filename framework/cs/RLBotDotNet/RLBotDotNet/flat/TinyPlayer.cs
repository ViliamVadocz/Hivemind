// <auto-generated>
//  automatically generated by the FlatBuffers compiler, do not modify
// </auto-generated>

namespace rlbot.flat
{

using global::System;
using global::FlatBuffers;

/// A minimal version of player data, useful when bandwidth needs to be conserved.
public struct TinyPlayer : IFlatbufferObject
{
  private Table __p;
  public ByteBuffer ByteBuffer { get { return __p.bb; } }
  public static TinyPlayer GetRootAsTinyPlayer(ByteBuffer _bb) { return GetRootAsTinyPlayer(_bb, new TinyPlayer()); }
  public static TinyPlayer GetRootAsTinyPlayer(ByteBuffer _bb, TinyPlayer obj) { return (obj.__assign(_bb.GetInt(_bb.Position) + _bb.Position, _bb)); }
  public void __init(int _i, ByteBuffer _bb) { __p.bb_pos = _i; __p.bb = _bb; }
  public TinyPlayer __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }

  public Vector3? Location { get { int o = __p.__offset(4); return o != 0 ? (Vector3?)(new Vector3()).__assign(o + __p.bb_pos, __p.bb) : null; } }
  public Rotator? Rotation { get { int o = __p.__offset(6); return o != 0 ? (Rotator?)(new Rotator()).__assign(o + __p.bb_pos, __p.bb) : null; } }
  public Vector3? Velocity { get { int o = __p.__offset(8); return o != 0 ? (Vector3?)(new Vector3()).__assign(o + __p.bb_pos, __p.bb) : null; } }
  public bool HasWheelContact { get { int o = __p.__offset(10); return o != 0 ? 0!=__p.bb.Get(o + __p.bb_pos) : (bool)false; } }
  public bool IsSupersonic { get { int o = __p.__offset(12); return o != 0 ? 0!=__p.bb.Get(o + __p.bb_pos) : (bool)false; } }
  public int Team { get { int o = __p.__offset(14); return o != 0 ? __p.bb.GetInt(o + __p.bb_pos) : (int)0; } }
  public int Boost { get { int o = __p.__offset(16); return o != 0 ? __p.bb.GetInt(o + __p.bb_pos) : (int)0; } }

  public static void StartTinyPlayer(FlatBufferBuilder builder) { builder.StartObject(7); }
  public static void AddLocation(FlatBufferBuilder builder, Offset<Vector3> locationOffset) { builder.AddStruct(0, locationOffset.Value, 0); }
  public static void AddRotation(FlatBufferBuilder builder, Offset<Rotator> rotationOffset) { builder.AddStruct(1, rotationOffset.Value, 0); }
  public static void AddVelocity(FlatBufferBuilder builder, Offset<Vector3> velocityOffset) { builder.AddStruct(2, velocityOffset.Value, 0); }
  public static void AddHasWheelContact(FlatBufferBuilder builder, bool hasWheelContact) { builder.AddBool(3, hasWheelContact, false); }
  public static void AddIsSupersonic(FlatBufferBuilder builder, bool isSupersonic) { builder.AddBool(4, isSupersonic, false); }
  public static void AddTeam(FlatBufferBuilder builder, int team) { builder.AddInt(5, team, 0); }
  public static void AddBoost(FlatBufferBuilder builder, int boost) { builder.AddInt(6, boost, 0); }
  public static Offset<TinyPlayer> EndTinyPlayer(FlatBufferBuilder builder) {
    int o = builder.EndObject();
    return new Offset<TinyPlayer>(o);
  }
};


}