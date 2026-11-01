from arena_core.storage import FileSourceStore


def test_round_trip_and_same_bytes_share_one_file(tmp_path):
    store = FileSourceStore(tmp_path)
    ref = store.put(b"source text", ".txt")
    assert ref.startswith("file:") and ref.endswith(".txt")
    assert store.get(ref) == b"source text"
    assert store.put(b"source text", ".txt") == ref
    assert len([p for p in tmp_path.rglob("*") if p.is_file()]) == 1
