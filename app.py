
# -*- coding: utf-8 -*-
# Main app for Chinese-Quick-Input-checking-Terminal
# All comments are in English for clarity.

import json
import os

def load_mapping(file_path):
    """
    Load mapping data from a JSON file.
    """
    if not os.path.exists(file_path):
        print(f"Can't find the file: {file_path}")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fuzzy_search(mapping, keyword, mode='cheat'):
    """
    Search for a character or code in the mapping.
    If mode is 'quick', only show first and last code.
    """
    results = []
    for k, v in mapping.items():
        if keyword in k or (isinstance(v, str) and keyword in v):
            if mode == 'quick' and isinstance(v, str) and len(v) >= 2:
                v_show = v[0] + v[-1]
            else:
                v_show = v
            results.append((k, v_show))
    return results

def save_mode_to_env(mode):
    """
    Save the current mode to .env file.
    """
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(f"MODE={mode}\n")

def load_mode_from_env():
    """
    Load the mode from .env file if exists.
    """
    if not os.path.exists('.env'):
        return None
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('MODE='):
                return line.strip().split('=', 1)[1]
    return None

def select_mode():
    """
    Let user select input mode: 1 for Quick (first/last code), 2 for Cangjie (full code).
    """
    print('查詢模式：1. 速成 (只顯示首尾碼)  2. 倉頡 (完整碼)')
    mode = ''
    while mode not in ['1', '2']:
        mode = input('請選擇模式 [1=速成, 2=倉頡]：').strip()
    save_mode_to_env(mode)
    return mode

def main():
    # File paths for mapping data
    small_mapping_file = './ChineseQuickMappingSmall.json'
    full_mapping_file = './ChineseQuickMapping.json'
    # Load mapping data
    small_mapping = load_mapping(small_mapping_file)
    full_mapping = None
    if small_mapping is None:
        small_mapping = {}
        full_mapping = load_mapping(full_mapping_file)
        if full_mapping is None:
            return
    # Load mode from .env or ask user
    mode = load_mode_from_env()
    if mode not in ['1', '2']:
        mode = select_mode()
    # Display current mode with description
    mode_display = f"{mode} (速成)" if mode == '1' else f"{mode} (倉頡)"
    print(f'--- 查字碼 目前mode: {mode_display} ---')
    mode_str = 'quick' if mode == '1' else 'cheat'
    import re
    zh_pattern = re.compile(r'^[\u4e00-\u9fff]+$')  # Only allow Chinese characters
    # Mapping from code to root name
    key_to_quick_unit = {
        'q': '手', 'w': '田', 'e': '水', 'r': '口', 't': '廿', 'y': '卜', 'u': '山', 'i': '戈', 'o': '人', 'p': '心',
        'a': '日', 's': '尸', 'd': '木', 'f': '火', 'g': '土', 'h': '竹', 'j': '十', 'k': '大', 'l': '中',
        'z': '重', 'x': '難', 'c': '金', 'v': '女', 'b': '月', 'n': '弓', 'm': '一'
    }
    import random
    while True:
        # Main input loop
        keyword = input('請輸入關鍵字（/setting 重新選擇模式，/train 進入訓練模式）：').strip()
        if not keyword:
            break
        if keyword == '/setting':
            # Change mode
            mode = select_mode()
            mode_str = 'quick' if mode == '1' else 'cheat'
            continue
        if keyword == '/train':
            # Training mode: random pick from small_mapping
            train_keys = list(small_mapping.keys())
            if not train_keys:
                print('無可用字元進行訓練！')
                continue
            combo = 0
            while True:
                # Pick a random character for training
                ch = random.choice(train_keys)
                print(f"請輸入「{ch}」的對應碼（輸入/exit 離開訓練）：")
                user_input = input('> ').strip()
                if user_input == '/exit':
                    print('離開訓練模式。')
                    break
                # Get the correct answer according to mode
                # mode 1: Quick (first/last code), mode 2: Cangjie (full code)
                results_full = fuzzy_search(small_mapping, ch, mode='cheat')
                if not results_full and full_mapping:
                    results_full = fuzzy_search(full_mapping, ch, mode='cheat')
                if not results_full:
                    print('查無此字碼。')
                    continue
                full_code = results_full[0][1]
                if mode_str == 'quick' and isinstance(full_code, str) and len(full_code) >= 2:
                    answer = full_code[0] + full_code[-1]
                else:
                    answer = full_code
                # Show root names
                if isinstance(full_code, str):
                    if mode_str == 'quick' and len(full_code) >= 2:
                        code_str = full_code[0] + full_code[-1]
                    else:
                        code_str = full_code
                    roots = ''.join([key_to_quick_unit.get(c, c) for c in code_str])
                else:
                    roots = '--'
                if user_input == answer:
                    combo += 1
                    print('正確！', end='')
                    if combo > 1:
                        print(f' Combo: {combo}')
                    else:
                        print()
                else:
                    print(f'錯誤，正確答案是：{answer} ({roots})')
                    combo = 0
            continue
        if not zh_pattern.fullmatch(keyword):
            print('請只輸入中文！')
            continue
        result_list = []
        for ch in keyword:
            # For each character, search and show code and root
            results = fuzzy_search(small_mapping, ch, mode=mode_str)
            if not results:
                if full_mapping is None:
                    full_mapping = load_mapping(full_mapping_file)
                    if full_mapping is None:
                        result_list.append('--')
                        continue
                results = fuzzy_search(full_mapping, ch, mode=mode_str)
            if results:
                code = results[0][1]
                full_code = fuzzy_search(small_mapping, ch, mode='cheat')
                if not full_code and full_mapping:
                    full_code = fuzzy_search(full_mapping, ch, mode='cheat')
                if full_code and isinstance(full_code[0][1], str):
                    code_str = full_code[0][1]
                    if mode_str == 'quick' and len(code_str) >= 2:
                        code_str = code_str[0] + code_str[-1]
                    roots = ''.join([key_to_quick_unit.get(c, c) for c in code_str])
                    result_list.append(f"{code}({roots})")
                else:
                    result_list.append(f"{code}(--)" )
            else:
                result_list.append('--')
        print(f"{' '.join(result_list)}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nbyebye!")