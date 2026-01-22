import os
import json
import subprocess
from pathlib import Path

def fix_bili_m4s(input_path, output_path):
    """修复 B 站 m4s 文件头"""
    with open(input_path, 'rb') as f:
        data = f.read()
    pos = data.find(b'ftyp')
    if pos != -1:
        start = max(0, pos - 4)
        with open(output_path, 'wb') as f_out:
            f_out.write(data[start:])
        return True
    return False

def get_title_from_json(folder_path):
    """适配您提供的 JSON 结构提取标题"""
    possible_files = ['videoInfo.json', 'video.info', '.videoInfo.json']
    for filename in possible_files:
        info_path = os.path.join(folder_path, filename)
        if os.path.exists(info_path):
            try:
                with open(info_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    group = content.get('groupTitle', '').strip()
                    item_title = content.get('title', '').strip()
                    full_title = f"{group}_{item_title}" if group and item_title and group != item_title else (item_title or group or "Video")
                    return "".join([c for c in full_title if c not in r'\/:*?"<>|']).strip()
            except:
                pass
    return os.path.basename(folder_path)

def process_single_folder(in_dir, out_dir):
    """处理单个文件夹逻辑：取最大和最小 m4s"""
    m4s_files = [os.path.join(in_dir, f) for f in os.listdir(in_dir) if f.endswith('.m4s')]
    if len(m4s_files) < 2:
        print(f"⚠️  跳过 (未找到足够文件): {in_dir}")
        return

    m4s_files.sort(key=os.path.getsize, reverse=True)
    v_path, a_path = m4s_files[0], m4s_files[-1]
    
    title = get_title_from_json(in_dir)
    final_output = os.path.join(out_dir, f"{title}.mp4")
    temp_v, temp_a = f"temp_v_{os.getpid()}.m4s", f"temp_a_{os.getpid()}.m4s"

    print(f"🎬 正在处理: {title}")
    try:
        if fix_bili_m4s(v_path, temp_v) and fix_bili_m4s(a_path, temp_a):
            cmd = ['ffmpeg', '-y', '-i', temp_v, '-i', temp_a, '-c', 'copy', '-loglevel', 'error', final_output]
            if subprocess.run(cmd).returncode == 0:
                print(f"  ✅ 完成")
            else:
                print(f"  ❌ FFmpeg 失败")
    finally:
        for t in [temp_v, temp_a]:
            if os.path.exists(t): os.remove(t)

def manual_select_run():
    # 核心改动：支持拖入多个路径
    raw_input = input("1. 请拖入【一个或多个】视频文件夹 (多个请一起拖入): ").strip()
    
    # 解析拖入的多个路径 (macOS/Linux 拖入多个文件夹通常以空格分隔)
    # 处理带空格的路径转义
    paths = []
    if "'" in raw_input or '"' in raw_input:
        # 简单处理被引号包裹的路径
        import shlex
        paths = shlex.split(raw_input)
    else:
        paths = raw_input.replace("\\ ", " ").split(" /") 
        if len(paths) > 1:
            paths = [paths[0]] + ["/" + p for p in paths[1:]]

    out_dir = input("2. 请拖入【输出目录】(回车默认下载目录): ").strip().replace("\\ ", " ").replace("'", "")
    if not out_dir:
        out_dir = str(Path.home() / "Downloads")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for p in paths:
        p = p.strip()
        if os.path.isdir(p):
            process_single_folder(p, out_dir)
        else:
            # 如果拖入的是父目录，则自动扫描其下一层子目录
            for entry in os.scandir(p):
                if entry.is_dir():
                    process_single_folder(entry.path, out_dir)

    print("\n✨ 选定任务处理完成！")

if __name__ == "__main__":
    manual_select_run()
