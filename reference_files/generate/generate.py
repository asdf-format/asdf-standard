import os

try:
    import asdf
except ImportError:
    raise ImportError(
        "asdf must be installed to regenerate the reference files.")

import numpy as np


def ref_basic(fd):
    tree = {
        'data': np.arange(8)
        }

    asdf.AsdfFile(tree).write_to(fd)


def ref_int(fd):
    tree = {}

    for size in (1, 2, 4):
        bits = size * 8
        for endian in ['>', '<']:
            values = [(1 << (bits - 1)) - 1, -(1 << (bits - 1)), 0]
            datatype = '%si%d' % (endian, size)
            arr = np.array(values, datatype)
            tree['datatype' + datatype] = arr

            values = [(1 << bits) - 1, 0]
            datatype = '%su%d' % (endian, size)
            arr = np.array(values, datatype)
            tree['datatype' + datatype] = arr

    asdf.AsdfFile(tree).write_to(fd)


def ref_float(fd):
    tree = {}

    for size in (4, 8):
        for endian in ['>', '<']:
            datatype = '%sf%d' % (endian, size)
            finfo = np.finfo(np.dtype(datatype))
            values = [0.0, -0.0, np.nan, np.inf, -np.inf,
                      finfo.min, finfo.max, finfo.eps, finfo.epsneg, finfo.tiny]
            arr = np.array(values, datatype)
            tree['datatype' + datatype] = arr

    asdf.AsdfFile(tree).write_to(fd)


def ref_complex(fd):
    tree = {}

    for size in (4, 8):
        for endian in ['>', '<']:
            datatype = '%sf%d' % (endian, size)
            finfo = np.finfo(np.dtype(datatype))
            values = [0.0, -0.0, np.nan, np.inf, -np.inf,
                      finfo.min, finfo.max, finfo.eps, finfo.epsneg, finfo.tiny]

            complex_values = []
            for x in values:
                for y in values:
                    complex_values.append(x + 1j * y)
            datatype = '%sc%d' % (endian, size * 2)
            arr = np.array(complex_values, datatype)
            tree['datatype' + datatype] = arr

    asdf.AsdfFile(tree).write_to(fd)


def ref_ascii(fd):
    arr = np.array([b'', b'ascii'], dtype='S')
    tree = {'data': arr}
    asdf.AsdfFile(tree).write_to(fd)


def ref_unicode_bmp(fd):
    tree = {}
    for endian in ['>', '<']:
        arr = np.array(['', 'Æʩ'], dtype=endian + 'U')
        tree['datatype' + endian + 'U'] = arr

    asdf.AsdfFile(tree).write_to(fd)


def ref_unicode_spp(fd):
    tree = {}
    for endian in ['>', '<']:
        arr = np.array(['', '𐀠'], dtype=endian + 'U')
        tree['datatype' + endian + 'U'] = arr

    asdf.AsdfFile(tree).write_to(fd)


def ref_shared(fd):
    data = np.arange(8)
    tree = {
        'data': data,
        'subset': data[1::2]
        }

    asdf.AsdfFile(tree).write_to(fd)


def ref_stream(fd):
    tree = {
        # Each "row" of data will have 128 entries.
        'my_stream': asdf.Stream([8], np.float64)
    }

    ff = asdf.AsdfFile(tree)
    with open(fd, 'wb') as fd:
        ff.write_to(fd)
        # Write 100 rows of data, one row at a time.  ``write_to_stream``
        # expects the raw binary bytes, not an array, so we use
        # ``tobytes()``.
        for i in range(8):
            fd.write(np.array([i] * 8, np.float64).tobytes())


def ref_exploded(fd):
    tree = {
        'data': np.arange(8)
    }

    asdf.AsdfFile(tree).write_to(fd, all_array_storage='external')


def ref_compressed(fd):
    tree = {
        'zlib': np.arange(128),
        'bzp2': np.arange(128)
    }

    ff = asdf.AsdfFile(tree)
    ff.set_array_compression(tree['zlib'], 'zlib')
    ff.set_array_compression(tree['bzp2'], 'bzp2')
    ff.write_to(fd)


def generate(version):
    outdir = os.path.join(os.path.dirname(__file__), '..', version)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for name, func in globals().copy().items():
        if not name.startswith("ref_"):
            continue

        name = name[4:]
        filename = os.path.join(outdir, name)
        func(filename + ".asdf")
        with asdf.open(filename + ".asdf") as af:
            af.resolve_references()
            af.write_to(filename + ".yaml", all_array_storage="inline")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        "generate",
        description="Regenerate the ASDF reference files")
    parser.add_argument(
        "version", type=str, help="The ASDF version")
    args = parser.parse_args()

    with asdf.config_context() as cfg:
        cfg.default_version = args.version
        generate(args.version)
