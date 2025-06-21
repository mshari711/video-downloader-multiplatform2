from flask import Flask, request, jsonify, send_file
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'الرابط غير صالح'})

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
        'extract_flat': False
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            results = []
            for fmt in formats:
                if fmt.get('url') and fmt.get('ext') in ['mp4', 'webm', 'm4a']:
                    results.append({
                        'format': f"{fmt.get('format_note', '')} - {fmt.get('ext')} - {round(fmt.get('filesize', 0)/1024/1024, 2)} MB" if fmt.get('filesize') else fmt.get('ext'),
                        'url': fmt['url']
                    })
            return jsonify({'links': results[:10]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
