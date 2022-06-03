import fnmatch
import os
from collections.abc import Mapping
from pathlib import Path

__all__ = ["DirectoryResourceMapping"]


class DirectoryResourceMapping(Mapping):
    """
    Resource mapping that reads resource content
    from a directory or directory tree.

    Parameters
    ----------
    root : str or importlib.abc.Traversable
        Root directory (or directory-like Traversable) of the resource
        files.  ``str`` will be interpreted as a filesystem path.
    uri_prefix : str
        Prefix used to construct URIs from file paths.  The
        prefix will be prepended to paths relative to the root
        directory.
    recursive : bool, optional
        If ``True``, recurse into subdirectories.  Defaults to ``False``.
    filename_pattern : str, optional
        Glob pattern that identifies relevant filenames.
        Defaults to ``"*.yaml"``.
    stem_filename : bool, optional
        If ``True``, remove the filename's extension when
        constructing its URI.
    """

    def __init__(self, root, uri_prefix, recursive=False, filename_pattern="*.yaml", stem_filename=True):
        self._uri_to_file = {}
        self._recursive = recursive
        self._filename_pattern = filename_pattern
        self._stem_filename = stem_filename

        if isinstance(root, str):
            self._root = Path(root)
        else:
            self._root = root

        if uri_prefix.endswith("/"):
            self._uri_prefix = uri_prefix[:-1]
        else:
            self._uri_prefix = uri_prefix

        for file, path_components in self._iterate_files(self._root, []):
            self._uri_to_file[self._make_uri(file, path_components)] = file

    def _iterate_files(self, directory, path_components):
        for obj in directory.iterdir():
            if obj.is_file() and fnmatch.fnmatch(obj.name, self._filename_pattern):
                yield obj, path_components
            elif obj.is_dir() and self._recursive:
                yield from self._iterate_files(obj, path_components + [obj.name])

    def _make_uri(self, file, path_components):
        if self._stem_filename:
            filename = os.path.splitext(file.name)[0]
        else:
            filename = file.name

        return "/".join([self._uri_prefix] + path_components + [filename])

    def __getitem__(self, uri):
        return self._uri_to_file[uri].read_bytes()

    def __len__(self):
        return len(self._uri_to_file)

    def __iter__(self):
        yield from self._uri_to_file

    def __repr__(self):
        return "{}({!r}, {!r}, recursive={!r}, filename_pattern={!r}, stem_filename={!r})".format(
            self.__class__.__name__,
            self._root,
            self._uri_prefix,
            self._recursive,
            self._filename_pattern,
            self._stem_filename,
        )
