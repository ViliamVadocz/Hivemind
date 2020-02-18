// <auto-generated>
//  automatically generated by the FlatBuffers compiler, do not modify
// </auto-generated>

namespace rlbot.flat
{

using global::System;
using global::FlatBuffers;

public struct BallPrediction : IFlatbufferObject
{
  private Table __p;
  public ByteBuffer ByteBuffer { get { return __p.bb; } }
  public static BallPrediction GetRootAsBallPrediction(ByteBuffer _bb) { return GetRootAsBallPrediction(_bb, new BallPrediction()); }
  public static BallPrediction GetRootAsBallPrediction(ByteBuffer _bb, BallPrediction obj) { return (obj.__assign(_bb.GetInt(_bb.Position) + _bb.Position, _bb)); }
  public void __init(int _i, ByteBuffer _bb) { __p.bb_pos = _i; __p.bb = _bb; }
  public BallPrediction __assign(int _i, ByteBuffer _bb) { __init(_i, _bb); return this; }

  /// A list of places the ball will be at specific times in the future.
  /// It is guaranteed to sorted so that time increases with each slice.
  /// It is NOT guaranteed to have a consistent amount of time between slices.
  public PredictionSlice? Slices(int j) { int o = __p.__offset(4); return o != 0 ? (PredictionSlice?)(new PredictionSlice()).__assign(__p.__indirect(__p.__vector(o) + j * 4), __p.bb) : null; }
  public int SlicesLength { get { int o = __p.__offset(4); return o != 0 ? __p.__vector_len(o) : 0; } }

  public static Offset<BallPrediction> CreateBallPrediction(FlatBufferBuilder builder,
      VectorOffset slicesOffset = default(VectorOffset)) {
    builder.StartObject(1);
    BallPrediction.AddSlices(builder, slicesOffset);
    return BallPrediction.EndBallPrediction(builder);
  }

  public static void StartBallPrediction(FlatBufferBuilder builder) { builder.StartObject(1); }
  public static void AddSlices(FlatBufferBuilder builder, VectorOffset slicesOffset) { builder.AddOffset(0, slicesOffset.Value, 0); }
  public static VectorOffset CreateSlicesVector(FlatBufferBuilder builder, Offset<PredictionSlice>[] data) { builder.StartVector(4, data.Length, 4); for (int i = data.Length - 1; i >= 0; i--) builder.AddOffset(data[i].Value); return builder.EndVector(); }
  public static void StartSlicesVector(FlatBufferBuilder builder, int numElems) { builder.StartVector(4, numElems, 4); }
  public static Offset<BallPrediction> EndBallPrediction(FlatBufferBuilder builder) {
    int o = builder.EndObject();
    return new Offset<BallPrediction>(o);
  }
};


}