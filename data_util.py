import os

target_sr = 16000
working_path = os.environ["WORKING_PATH"]

# separate
model = "htdemucs"
extensions = ["mp3", "wav", "ogg", "flac"]  # we will look for all those file types.

muljam_id_file = "./input/muljam_ids.npy" # all ids in MTG-Jamendo dataset that forms the MulJam v2 dataset

# uncomment below if processing DALI
# audio_ext = ".mp3"
# mix_dir = '/PATH/TO/DALI_v2.0/audio/' # CHANGE (where DALI_v2.0 is located): mixture audio path: ID.mp3
# sepa_dir = os.path.join(working_path, 'dali_ss') # separated audio path: ID_vocals.wav
# seg_dir = os.path.join(working_path, 'dali_seg') # segment audio path: prefix/ID_segID.wav

# uncomment below if processing MulJam
audio_ext = ".mp3"
mix_dir = '/PATH/TO/MULJAM_V2/' # CHANGE (where to save MulJam v2): mixture audio path: postfix/ID.mp3
sepa_dir = os.path.join(working_path, 'muljam_ss') # separated audio path: ID_vocals.wav
seg_dir = os.path.join(working_path, 'muljam_seg') # segment audio path: prefix/ID_segID.wav

# uncomment below if processing MultiLang Jamendo
# audio_ext = ".mp3"
# mix_dir = os.path.join(working_path, 'jamendolyrics-1.1/mp3/')
# sepa_dir = os.path.join(working_path, 'jamendo_ss') # separated audio path: ID_vocals.wav
# seg_dir = os.path.join(working_path, 'jamendo_seg') # segment audio path: ID_segID.wav