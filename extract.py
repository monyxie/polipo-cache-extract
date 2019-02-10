#!/usr/bin/env python3
import sys
argc = len(sys.argv)
if  argc < 2 or argc > 3:
    print("Usage: python3 extract.py cache-file [output-file]")
    print("    If an output-file is not provided, then it'll be automatically decided.")
    sys.exit(1)

cache_file = sys.argv[1]
output_file = ""
if (argc == 3):
    output_file = sys.argv[2]

with open(cache_file, "rb") as cache_fp:
    offset = 0
    location = ""

    while True:
        line = cache_fp.readline()
        if line == "\r\n".encode():
            break
        if line.startswith("X-Polipo-Body-Offset: ".encode()):
            kv = line[:-2].split(': '.encode())
            offset = int(kv[1])
        if line.startswith("X-Polipo-Location: ".encode()):
            kv = line[:-2].split(': '.encode())
            location = kv[1].decode()

    if output_file == "":
        segments = location.rstrip("/").split("/")
        if len(segments) >= 3 and segments[-1] != "":
            output_file = segments[-1]

        if output_file == "":
            output_file = cache_file + ".output"

    with open(output_file, "xb") as output_fp:
        cache_fp.seek(offset)
        buf = cache_fp.read(4096)
        while len(buf) > 0:
            output_fp.write(buf)
            buf = cache_fp.read(4096)

