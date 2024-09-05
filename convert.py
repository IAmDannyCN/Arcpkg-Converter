import os
import json
import yaml
import tempfile
import shutil
from datetime import datetime

USERID = 'IAD'

class LevelPack:
    def __init__(self, id, name, imgPath):
        self.id = id
        self.name = name
        self.imgPath = imgPath
        self.songs = []

packs = {}
tmpdict = None

def getPacks():
    with open("./packlist", 'r', encoding='utf-8') as file:
        packlist_json = json.load(file)
    packlist = packlist_json['packs']
    
    for pack in packlist:
        id = pack['id']
        name = pack['name_localized']['en']
        assert os.path.exists(f'./pack/1080_select_{id}.png'), "img for pack [{id}] not found"
        imgPath = f"1080_select_{id}.png"
        packs[id] = LevelPack(id=id, name=name, imgPath=imgPath)
        
        
def getSongs():
    with open("./songlist", 'r', encoding='utf-8') as file:
        songlist_json = json.load(file)
    
    songlist = songlist_json['songs']
    for song in songlist:
        res = {'charts': []}
        
        id = song['id']
        name = song['title_localized']['en']
        composer = song['artist']
        side = song['side']
        bpm = song['bpm']
        bpm_base = song['bpm_base']
        set = song['set']
        
        if set not in packs:
            print(f"Song {id} with pack {set} not found")
            continue
        
        packs[set].songs.append(id)
        
        for chart in song['difficulties']:
            converted = {}
            difficulty = chart['ratingClass']
            if not os.path.exists(f'./{id}/{difficulty}.aff'):
                continue
            
            converted['chartPath'] = f"{difficulty}.aff"
            converted['audioPath'] = 'base.ogg' if not chart.get('audioOverride', False) else f"{difficulty}.ogg"
            converted['jacketPath'] = '1080_base.jpg' if not chart.get('jacketOverride', False) else f"1080_{difficulty}.jpg"
            converted['baseBpm'] = bpm_base if not chart.get('bpm_base', False) else chart['bpm_base']
            converted['bpmText'] = bpm if not chart.get('bpm', False) else chart['bpm']
            converted['syncBaseBpm'] = True
            converted['title'] = name if not chart.get('title_localized', False) else chart['title_localized']['en']
            converted['composer'] = composer if not chart.get('artist', False) else chart['artist']
            converted['charter'] = chart['chartDesigner']
            converted['difficulty'] = f"{['Past', 'Present', 'Future', 'Beyond', 'Eternal'][difficulty]} {chart['rating']}{['', '+'][chart.get('ratingPlus', False)]}"
            converted['difficultyColor'] = ['#3A6B78FF', '#566947FF', '#482B54FF', '#7C1C30FF', '#433455FF'][difficulty]
            converted['skin'] = {'side': ['light', 'conflict', 'colorless'][side]}
            converted['previewEnd'] = 5000
            
            res['charts'].append(converted)
        
        yaml_data = yaml.dump(res, allow_unicode=True, encoding='utf-8')
        
        with open(f'./{id}/project.arcproj', 'w', encoding='utf-8') as file:
            file.write(yaml_data.decode())


def wrapper():
    index_yml = []
    for packid in packs:
        pack = packs[packid]
        pack_index = {
            'directory': packid,
            'identifier': f"{USERID}.{packid}",
            'settingsFile': f"{packid}.yml",
            'version': 0,
            'type': 'pack',
        }
        index_yml.append(pack_index)
        
        pack_yml = {}
        pack_yml['packName'] = pack.name
        pack_yml['imagePath'] = pack.imgPath
        pack_yml['levelIdentifiers'] = [f"{USERID}.{id}" for id in pack.songs]
        pack_yml_data = yaml.dump(pack_yml, allow_unicode=True, encoding='utf-8')
        os.mkdir(f"{tmpdict}/{packid}")
        with open(f"{tmpdict}/{packid}/{packid}.yml", 'w', encoding='utf-8') as file:
            file.write(pack_yml_data.decode())
        shutil.copy(f"./pack/1080_select_{packid}.png", f"{tmpdict}/{packid}/1080_select_{packid}.png")
        
        for songid in pack.songs:
            level_index = {
                'directory': songid,
                'identifier': f"{USERID}.{songid}",
                'settingsFile': 'project.arcproj',
                'version': 0,
                'type': 'level',
            }
            index_yml.append(level_index)
            shutil.copytree(f"./{songid}", f"{tmpdict}/{songid}")
    
    index_yml_data = yaml.dump(index_yml, allow_unicode=True, encoding='utf-8')
    with open(f"{tmpdict}/index.yml", 'w', encoding='utf-8') as file:
        file.write(index_yml_data.decode())
    
    # shutil.copytree(tmpdict, f'./{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}')
    output_name = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    shutil.make_archive(f'./{output_name}', 'zip', tmpdict)
    os.rename(f"./{output_name}.zip", f"./{output_name}.arcpkg")
        
    

def main():
    global tmpdict
    tmpdict = tempfile.mkdtemp()
    getPacks()
    getSongs()
    wrapper()
            
        
if __name__ == '__main__':
    main()
