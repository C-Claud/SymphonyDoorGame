from flask import Flask, render_template, jsonify, send_from_directory, request
import os
import random
import mutagen

app = Flask(__name__)
SYMPHONY_DIR = 'dataset'
ALLOWED_EXT = ('.mp3', '.wav', '.ogg', '.flac', '.m4a')

def get_symphony_files():
    return [f for f in os.listdir(SYMPHONY_DIR) if f.lower().endswith(ALLOWED_EXT)]

def natural_sort_key(name):
    import re
    parts = re.split(r'(\d+)', name)
    return [int(part) if part.isdigit() else part.lower() for part in parts]

def get_duration(filepath):
    try:
        info = mutagen.File(filepath)
        return info.info.length
    except Exception:
        return 0.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_challenge')
def challenge():
    # 获取用户选择的片段时长，默认20秒
    try:
        sample_duration = int(request.args.get('duration', 20))
    except ValueError:
        sample_duration = 20
    # 限制范围，防止异常值
    sample_duration = max(10, min(sample_duration, 120))

    files = get_symphony_files()
    if not files:
        return jsonify({'error': '未找到音频文件'}), 404

    chosen = random.choice(files)
    filepath = os.path.join(SYMPHONY_DIR, chosen)
    duration = get_duration(filepath)
    offset = 10

    if duration < sample_duration:
        start_time = 0.0
    else:
        start_time = random.uniform(0, duration - sample_duration - offset)

    names = [os.path.splitext(f)[0] for f in files]
    return jsonify({
        'audio_file': chosen,
        'start_time': start_time,
        'names': names,
        'sample_duration': sample_duration   # 传给前端用于计时
    })

@app.route('/api/songs')
def song_list():
    files = get_symphony_files()
    songs = []
    for f in files:
        filepath = os.path.join(SYMPHONY_DIR, f)
        name = os.path.splitext(f)[0]
        duration = get_duration(filepath)
        songs.append({
            'filename': f,
            'name': name,
            'duration': duration
        })
    songs.sort(key=lambda x: natural_sort_key(x['name']))
    return jsonify(songs)

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(SYMPHONY_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)