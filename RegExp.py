import re
import os
import shutil



def to_salt_language(text):
    ''' Function for translating to "salt" language. '''

    vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    result = ""

    for char in text:
        if char in vowels:
            s_char = 'с' if char.islower() else 'С'
            result += char + s_char + char
        else:
            result += char

    return result

def extract_chords(filepath):
    ''' Function for extracting chords from a file. '''
    chords = set()
    chord_pattern = r'\b[A-G][#b]?(?:m|maj|min|dim|aug|sus|add|\d+)*(?:/[A-G][#b]?)?\b'

    for encoding in ['utf-8', 'utf-8-sig', 'cp1251', 'latin1']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                for line in f:
                    matches = re.findall(chord_pattern, line)
                    chords.update(matches)
                return chords
        except UnicodeDecodeError:
            continue
    
    raise ValueError("Не удалось определить кодировку файла")

    
def rename_files(dir, pattern, new_pattern=None, sample_names=None, to_replace=False):
    ''' Function for bulk file renaming '''

    if sample_names is None:
        sample_names = {}

    files = os.listdir(dir)

    for filename in files:
        if re.search(pattern, filename):
            new_name = filename

            if new_pattern:
                new_name = re.sub(pattern, new_pattern, new_name)

            for old_sample, new_sample in sample_names.items():
                new_name = new_name.replace(old_sample, new_sample)

            src_path = os.path.join(dir, filename)
            dst_path = os.path.join(dir, new_name)

            if src_path == dst_path:
                continue

            if to_replace:
                os.rename(src_path, dst_path)
                print(f"Переименован: {filename} -> {new_name}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"Скопирован: {filename} -> {new_name}")




