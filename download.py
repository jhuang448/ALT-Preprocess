import os
import numpy as np
import argparse
from tqdm import tqdm
import gdown
from data_util import *

def download_data(dataset="MulJam"):
    if dataset == "MulJam":
        # download from MTG fast mirror
        if not os.path.exists(mix_dir):
            os.mkdir(mix_dir)
        muljam_ids = list(np.load(muljam_id_file))
        for id in tqdm(muljam_ids):
            save_file = os.path.join(mix_dir, id.split("/")[1])
            url = "https://cdn.freesound.org/mtg-jamendo/raw_30s/audio-low/{}".format(id)
            gdown.download(url, save_file, quiet=True)
    elif dataset == "DALI":
        print("DALI dataset is not supported. Please follow the instructions in the repository to download: https://github.com/gabolsgabs/DALI/tree/version2/versions")
        pass
    elif dataset == "Jamendo":
        # download from github
        url = "https://github.com/f90/jamendolyrics/archive/refs/tags/v1.1.zip"
        gdown.download(url, working_path, quiet=False)
        os.system("unzip -qq {}/v1.1.zip -d {} && rm {}/v1.1.zip".format(working_path, working_path, working_path))

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True, default="MulJam",
                        help="Which dataset to download.")

    args = parser.parse_args()

    download_data(args.dataset)
    print('Download complete.')