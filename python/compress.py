"""
compress 压缩
"""

import sys

if sys.version_info >= (3, 14):
    from compression import bz2, gzip, lzma, zlib, zstd
else:
    import bz2
    import gzip
    import lzma
    import zlib

    import zstd


def main():
    data = b"This is some sample text data that we will use to demonstrate compression algorithms. " * 10

    print("原始数据大小:", len(data), "bytes")

    # gzip 压缩示例
    gzip_data = gzip.compress(data)
    print("gzip压缩后大小:", len(gzip_data), "bytes")
    gzip_decompressed = gzip.decompress(gzip_data)
    print("gzip解压验证:", gzip_decompressed == data)

    # bz2 压缩示例
    bz2_data = bz2.compress(data)
    print("bz2压缩后大小:", len(bz2_data), "bytes")
    bz2_decompressed = bz2.decompress(bz2_data)
    print("bz2解压验证:", bz2_decompressed == data)

    # zlib 压缩示例
    zlib_data = zlib.compress(data)
    print("zlib压缩后大小:", len(zlib_data), "bytes")
    zlib_decompressed = zlib.decompress(zlib_data)
    print("zlib解压验证:", zlib_decompressed == data)

    # lzma 压缩示例
    lzma_data = lzma.compress(data)
    print("lzma压缩后大小:", len(lzma_data), "bytes")
    lzma_decompressed = lzma.decompress(lzma_data)
    print("lzma解压验证:", lzma_decompressed == data)

    # zstd 压缩示例
    zstd_data = zstd.compress(data)
    print("zstd压缩后大小:", len(zstd_data), "bytes")
    zstd_decompressed = zstd.decompress(zstd_data)
    print("zstd解压验证:", zstd_decompressed == data)


if __name__ == '__main__':
    main()
