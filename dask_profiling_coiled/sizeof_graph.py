import time
import pickle

import dask
import dask.utils
import dask.dataframe
import dask.highlevelgraph
import distributed
import distributed.protocol


def print_sizeof_serialized_graph(x) -> None:
    start = time.perf_counter()
    dsk = dask.base.collections_to_dsk([x], optimize_graph=True)
    optimize_time = time.perf_counter() - start

    if not isinstance(dsk, dask.highlevelgraph.HighLevelGraph):
        dsk = dask.highlevelgraph.HighLevelGraph.merge(dsk)

    start = time.perf_counter()
    packed = dsk.__dask_distributed_pack__(distributed.get_client(), x.__dask_keys__())
    pack_time = time.perf_counter() - start

    start = time.perf_counter()
    frames = distributed.protocol.dumps(packed)
    dumps_time = time.perf_counter() - start
    dumps = sum(len(f) for f in frames)

    start = time.perf_counter()
    pickled = len(pickle.dumps(packed))
    pickle_time = time.perf_counter() - start

    print(
        f"Graph ({len(dsk)} optimized tasks) is:\n"
        f"* {dask.utils.format_bytes(dumps)} with distributed-dumps ({len(frames)} frames) - {dumps_time:.1}s\n"
        f"* {dask.utils.format_bytes(pickled)} pickled  - {pickle_time:.1}s\n"
        f"Optimize: {optimize_time:.1}s, pack: {pack_time:.1}s"
    )
