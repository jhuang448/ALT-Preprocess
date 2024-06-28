import soundfile as sf
import librosa
from tqdm import tqdm
import pandas as pd
import argparse
from concurrent.futures import ProcessPoolExecutor
from data_util import *
import warnings
warnings.filterwarnings('ignore')

if not os.path.exists(seg_dir):
    os.mkdir(seg_dir)
def get_sepa_file(filename):
    if "_vocals" not in filename: # MulJam
        filename = filename.split("/")[-1]
        filename = filename.replace(".mp3", "_vocals.wav")
    return os.path.join(sepa_dir, filename)

def segment_one(args):
    input_file, segs = args
    y, sr = librosa.load(input_file, sr=target_sr, mono=True)
    if y.shape[0] / sr < 1:
        return False

    for seg in segs:
        save_file, input_file, start, end = seg
        if os.path.exists(save_file):
            continue
        st = int(sr * start)
        ed = int(sr * end)
        if ed <= st: # or ed > y.shape[0]:
            print("invalid segment time! {}".format(save_file))
            continue
        y_seg = y[st:ed]
        sf.write(save_file, y_seg, target_sr)

    return True

def prepare_audio(meta, save_folder, split):
    df = pd.read_csv(meta)
    songs = {}
    for idx in df.index:
        id = df.loc[idx, "id"]
        lang = df.loc[idx, "lang"]

        input_file = get_sepa_file(df.loc[idx, "file"])
        if os.path.exists(input_file) == False:
            print("File not found: ", input_file)
            continue

        if split == "train":
            subfolder = str(id[:2])
            if os.path.exists(os.path.join(save_folder, subfolder)) == False:
                os.mkdir(os.path.join(save_folder, subfolder))
            save_file = os.path.join(save_folder, subfolder, id + ".wav")
        else:
            save_file = os.path.join(save_folder, id + ".wav")

        start = df.loc[idx, "start"]
        end = df.loc[idx, "end"]

        if input_file not in songs.keys():
            songs[input_file] = []

        songs[input_file] += [[save_file, input_file, start, end]]
    args_list = [[k, v] for k, v in songs.items()]

    # multiprocessing
    with ProcessPoolExecutor(max_workers=5) as executor:
        results = list(tqdm(executor.map(segment_one, args_list), total=len(args_list)))


def segment_data(input_file, split="test"):
    save_folder = os.path.join(seg_dir, split)
    os.makedirs(save_folder, exist_ok=True)
    prepare_audio(input_file, save_folder, split=split)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta_file", type=str, required=True, default=None,
                        help="The meta file. E.g. ./input/dummy/muljam_dummy.meta")
    parser.add_argument("--split", type=str, required=True, default="unknown",
                        help="The split of the data.")

    args = parser.parse_args()
    segment_data(args.meta_file, split=args.split)
    print('Segment complete.')