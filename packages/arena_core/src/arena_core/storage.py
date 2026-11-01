"""Raw source files (captions, audio, written texts), stored by content hash.

The filesystem is enough while the work is small. `transcript.storage_ref` holds the returned
reference, so a move to S3-compatible storage means a new class here and a copy of the files.
"""

import hashlib
import os
import pathlib
import tempfile


class FileSourceStore:
    def __init__(self, root: pathlib.Path) -> None:
        self.root = root

    def put(self, data: bytes, suffix: str = "") -> str:
        """Store bytes and return their reference. Storing the same bytes twice is a no-op."""
        digest = hashlib.sha256(data).hexdigest()
        ref = f"{digest[:2]}/{digest}{suffix}"
        path = self.root / ref
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
                handle.write(data)
            os.replace(handle.name, path)
        return f"file:{ref}"

    def get(self, ref: str) -> bytes:
        return (self.root / ref.removeprefix("file:")).read_bytes()
