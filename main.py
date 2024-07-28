import zipfile
import os
import json
import random
import string
from PIL import Image
import shutil


def mcz_unzip(mcz_path: str) -> str:
    zip = zipfile.ZipFile(mcz_path, metadata_encoding='UTF-8')
    os.mkdir(mcz_path.split('.')[0])
    zip.extractall(mcz_path.split('.')[0])
    zip.close()
    return mcz_path.split('.')[0]


def gen_random_uid(length: int = 13) -> str:
    uid_random_str_list = list(string.ascii_lowercase) + list(string.digits)
    random_uid = ''
    for i in range(length):
        random_uid += uid_random_str_list[random.randint(0, len(uid_random_str_list) - 1)]
    return random_uid


def mc2tres(mc_path: str, mc_dir: str) -> str:
    global sound_path, corrected
    if not mc_dir.endswith('\\'):
        mc_dir += '\\'
    print('mcz_path:', mc_dir)
    with open(f'{mc_path}', 'r', encoding='UTF-8') as mc:
        mc_json = json.load(mc)
    # 4k谱面检测
    if mc_json['meta']['mode_ext']['column'] != 4:
        return '非4k谱面，转换失败'
    # 非变速谱检测
    if len(mc_json['time']) != 1:
        return '谱面bpm非法（bpm信息错误/变速谱）'

    # 铺面信息提取 Part 1
    song_name = mc_json['meta']['song']['title']
    creator = mc_json['meta']['creator']
    info = f'曲师：{mc_json['meta']['song']['artist']}\n{mc_json['meta']['version']}'
    bg = mc_json['meta']['background']
    bpm = mc_json['time'][0]['bpm']

    print('info:', [song_name, creator, info, bg, bpm])
    notes = list()
    # 主谱面提取
    for note in mc_json['note']:
        note = dict(note)
        if note.get('column', -1) != -1:
            # note种类判断
            if note.get('endbeat', None) is not None:
                # hold判定
                beat_i = round(int(note['beat'][1]) * 48) / int(note['beat'][2])
                drag = (int(note['endbeat'][0]) - int(note['beat'][0])) * 48 + (
                        round(int(note['endbeat'][1]) * 48) / int(note['endbeat'][2]) - beat_i)
                if drag <= 0:
                    return f'程序失误了，将下面这段信息保存\n\n\n{note}|{beat_i}|{drag}'
                single_note = {
                    'beat': note['beat'][0],
                    'i': beat_i,
                    'drag': drag,
                    'key': note['column']
                }
            else:
                beat_i = round(int(note['beat'][1]) * 48) / int(note['beat'][2])
                single_note = {
                    'beat': note['beat'][0],
                    'i': beat_i,
                    'drag': 0,
                    'key': note['column']
                }
            notes.append(single_note)
            print(single_note)
        else:
            corrected = int(note['offset']) / 1000
            sound_path = note['sound']
    # 导出
    os.mkdir(f'{mc_dir}export')
    shutil.copy(f'{mc_dir}{sound_path}', f'{mc_dir}export/{song_name}.ogg')
    shutil.copy(f'{mc_dir}{bg}', f'{mc_dir}export/{song_name}.jpg')
    with Image.open(f'{mc_dir}export/{song_name}.jpg') as img:
        width, height = img.size
        if height > width:
            empty = round((height - width) / 2)
            region = f'Rect2(0, {empty}, {width}, {width})'
        else:
            empty = round((width - height) / 2)
            region = f'Rect2({empty}, 0, {height}, {height})'
    print('region', region)
    with open(f'{mc_dir}export/{song_name}.tres', 'w', encoding='UTF-8') as tres:
        load_step = len(notes) + 6
        cover_uid = f'cover{gen_random_uid(8)}'
        song_uid = f'song{gen_random_uid(9)}'
        full_tres = (
            f'[gd_resource type="Resource" script_class="Chart" load_steps={load_step} format=3 uid="uid://{gen_random_uid()}"]\n\n'
            f'[ext_resource type="Script" path="res://scripts/res/chart.gd" id="1"]\n'
            f'[ext_resource type="Texture2D" uid="uid://{cover_uid}" path="res://images/covers/{song_name}.jpg" id="2"]\n'
            f'[ext_resource type="AudioStream" uid="uid://{song_uid}" path="res://songs/{song_name}.ogg" id="3"]\n'
            f'[ext_resource type="Script" path="res://scripts/res/note.gd" id="4"]\n\n'
            f'[sub_resource type="AtlasTexture" id="1"]\n'
            f'atlas = ExtResource("2")\n'
            f'region = {region}\n\n')
        for i in range(len(notes)):
            full_tres += (f'[sub_resource type="Resource" id="{i + 2}"]\n'
                          f'script = ExtResource("4")\n'
                          f'beat = {notes[i]['beat']}\n'
                          f'i = {notes[i]['i']}\n'
                          f'drag = {notes[i]['drag']}\n'
                          f'key = {notes[i]['key']}\n\n')
        full_tres += (f'[resource]\n'
                      f'script = ExtResource("1")\n'
                      f'cover = SubResource("1")\n'
                      f'name = "{song_name}"\n'
                      f'author = "{creator}"\n'
                      f'info = "{info}"\n'
                      f'song = ExtResource("3")\n'
                      f'bpm = {bpm}\n'
                      f'corrected = {corrected}\n'
                      f'notes = Array[ExtResource("4")]([')
        for i in range(len(notes)):
            full_tres += f'SubResource("{i + 2}"),'
            if i != len(notes) - 1:
                full_tres += ' '
        full_tres += '])\n'
        tres.write(full_tres)
    # import文件部分
    with open(f'{mc_dir}export/{song_name}.jpg.import', 'w', encoding='utf-8') as jpg_import:
        full_jpg_import = (f'[remap]\n\n'
                           f'importer="texture"\n'
                           f'type="CompressedTexture2D"\n'
                           f'uid="uid://{cover_uid}"\n'
                           f'path="res://.godot/imported/{song_name}.jpg-abcdabcdabcdabcdabcdabcdabcdabcd.ctex"\n'
                           f'metadata={{\n'
                           f'"vram_texture": false\n'
                           f'}}\n\n'
                           f'[deps]\n\n'
                           f'source_file="res://images/covers/{song_name}.jpg"\n'
                           f'dest_files=PackedStringArray("res://.godot/imported/{song_name}.jpg-abcdabcdabcdabcdabcdabcdabcdabcd.ctex")\n\n'
                           f'[params]\n\n'
                           f'dummy_value_ignore_me=0\n')
        jpg_import.write(full_jpg_import)
    with open(f'{mc_dir}export/{song_name}.ogg.import', 'w', encoding='utf-8') as ogg_import:
        full_ogg_import = (f'[remap]\n\n'
                           f'importer="oggvorbisstr"\n'
                           f'type="AudioStreamOggVorbis"\n'
                           f'uid="uid://{song_uid}"\n'
                           f'path="res://.godot/imported/{song_name}.ogg-aaaabbbbccccddddaaaabbbbccccdddd.oggvorbisstr"\n\n'
                           f'[deps]\n\n'
                           f'source_file="res://songs/{song_name}.ogg"\n'
                           f'dest_files=PackedStringArray("res://.godot/imported/{song_name}.ogg-aaaabbbbccccddddaaaabbbbccccdddd.oggvorbisstr")\n\n'
                           f'[params]\n\n'
                           f'dummy_value_ignore_me=0\n')
        ogg_import.write(full_ogg_import)
    return f'操作完成，请查看{mc_dir}export'


if __name__ == '__main__':
    mcz = input('请输入py文件目录下mcz名：')
    mcz_path = mcz.split('.')[0]
    shutil.rmtree(mcz_path)
    mcz_unzip(mcz)
    mc_files = list()
    for root, dirs, files in os.walk(mcz_path):
        for file in files:
            # 构建相对路径
            relative_path = os.path.relpath(os.path.join(root, file), mcz_path)
            if relative_path.endswith('.mc'):
                mc_files.append(relative_path)
    for i in range(len(mc_files)):
        print(f'{i}:{mc_files[i]}')

    nums = input('请输入欲转换mc文件名序号：')
    mc_dir = ''
    mc_path = os.path.relpath(os.path.join(mcz_path, mc_files[int(nums)]))
    for i in mc_path.split("\\")[:-1]:
        mc_dir += i + '\\'
    mc_dir = os.path.relpath(mc_dir)
    print(mc2tres(mc_path, mc_dir))
