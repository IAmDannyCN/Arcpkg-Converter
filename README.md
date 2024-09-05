# Arcpkg Converter

### Environments

PyYAML==6.0.1

### Usage

1. Place it in the "songs" folder which contains the following files:
- songlist
- packlist
- pack
  - 1080_select_\[set_id\].png
- \[song_id\]
  - base.ogg
  - 1080_base.png
  - \[X\].aff (\[X\] can be 0, 1, 2, 3, 4, standing for past, present, future, beyond, eternal; Can exist at the same time)
  - (optional, required when `jacketOverride == true` in songlist) 1080_\[X\].png
  - (optional, required when `audioOverride == true` in songlist) \[X\].ogg

2. Change `USERID` in line to your own signaturing name.

3. Run `python ./convert.py`, it spawns a `\[current_time\].arcpkg` in the folder, which can be directly imported by ArcCreate PE clients.

### Notice

`songlist` **file must be valid**. For example, it should at least satisfy the following rules:
- Key values (id, title_localized/en, artist, bpm, bpm_base, set, side etc.) are not vacant
- If you don't have charts for some difficulty levels, it's okay not mentioning them
- **Make sure every song has a corresponding valid pack**

`packlist` should be valid, too.

### Acknowledgement
Thank 2e19728 for providing a testing set including all required files and fantastic charts.
