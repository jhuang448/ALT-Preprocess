# ref: https://github.com/facebookresearch/demucs
# !python3 -m pip install -U demucs
import io
import os.path
from pathlib import Path
import select
import subprocess as sp
import sys, argparse
from typing import Dict, Tuple, Optional, IO
import numpy as np
from data_util import *

if not os.path.exists(sepa_dir):
    os.mkdir(sepa_dir)

def find_files(in_path):
    out = []
    for file in Path(in_path).iterdir():
        if file.suffix.lower().lstrip(".") in extensions:
            out.append(file)
    return out

def copy_process_streams(process: sp.Popen):
    def raw(stream: Optional[IO[bytes]]) -> IO[bytes]:
        assert stream is not None
        if isinstance(stream, io.BufferedIOBase):
            stream = stream.raw
        return stream

    p_stdout, p_stderr = raw(process.stdout), raw(process.stderr)
    stream_by_fd: Dict[int, Tuple[IO[bytes], io.StringIO, IO[str]]] = {
        p_stdout.fileno(): (p_stdout, sys.stdout),
        p_stderr.fileno(): (p_stderr, sys.stderr),
    }
    fds = list(stream_by_fd.keys())

    while fds:
        # `select` syscall will wait until one of the file descriptors has content.
        ready, _, _ = select.select(fds, [], [])
        for fd in ready:
            p_stream, std = stream_by_fd[fd]
            raw_buf = p_stream.read(2 ** 16)
            if not raw_buf:
                fds.remove(fd)
                continue
            buf = raw_buf.decode()
            std.write(buf)
            std.flush()

def separate(files=None, inp=None, outp=None):
    if files is None:
        inp = inp or mix_dir
        outp = outp or sepa_dir
        files = [str(f) for f in find_files(inp)]
        if not files:
            print(f"No valid audio files in {inp}")
            return
    else:
        files = files

    unprocessed_files = []
    for file in files:
        basename = os.path.splitext(os.path.basename(file))[0]
        sepa_file = os.path.join(outp, "htdemucs", basename, "vocals.wav")
        sepa_file2 = os.path.join(outp, basename+"_vocals.wav")
        if os.path.exists(sepa_file) or os.path.exists(sepa_file2):
            continue
        unprocessed_files.append(file)
    files = unprocessed_files

    cmd = ["python3", "-m", "demucs.separate", "-o", str(outp), "-n", model]
    cmd += ["--float32"]
    cmd += [f"--two-stems=vocals"]

    # separate
    print("Going to separate {} files:".format(len(files)))
    print('\n'.join(files))
    print("With command: ", " ".join(cmd))
    p = sp.Popen(cmd + files, stdout=sp.PIPE, stderr=sp.PIPE)
    copy_process_streams(p)
    p.wait()
    if p.returncode != 0:
        print("Command failed, something went wrong.")

    # rename
    for file in files:
        basename = os.path.splitext(os.path.basename(file))[0]
        mv_cmd = ["mv", os.path.join(outp, "htdemucs", basename, "vocals.wav"), os.path.join(outp, basename+"_vocals.wav")]
        p1 = sp.Popen(mv_cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        copy_process_streams(p1)
        p1.wait()
        assert (p1.returncode == 0)
    # remove useless folder
    rm_cmd = ["rm", "-r", os.path.join(outp, "htdemucs")]
    p1 = sp.Popen(rm_cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    copy_process_streams(p1)
    p1.wait()
    assert (p1.returncode == 0)

def separate_data(ids_file=None, audio_ext=".mp3"):
    if ids_file is not None:
        files = list(np.load(ids_file))
        files = [os.path.join(mix_dir, file.split("/")[-1]) for file in files]
    else:
        files = None
    separate(files, mix_dir, sepa_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids_file", type=str, required=False, default=None,
                        help="If None, will run source separation on all audio files in the mixture folder. "
                             "e.g. ./input/dummy/muljam_dummy_ids.npy")

    args = parser.parse_args()

    separate_data(args.ids_file)
    print('Separate complete.')