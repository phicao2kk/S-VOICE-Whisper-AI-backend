import os
import whisper
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# ================= CẤU HÌNH =================
app = Flask(__name__)
CORS(app)

# Đường dẫn tuyệt đối
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

print(f"📁 Thư mục upload: {UPLOAD_FOLDER}")

# ================= LOAD MODEL =================
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Sử dụng thiết bị: {device}")

MODEL_SIZE = "base"
print(f"📥 Đang tải model Whisper '{MODEL_SIZE}'...")
model = whisper.load_model(MODEL_SIZE, device=device)
print(f"✅ Model '{MODEL_SIZE}' đã sẵn sàng!")
    
# ================= API =================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model': MODEL_SIZE,
        'device': device,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        print("\n" + "="*50)
        print("📥 Nhận request transcribe")
        
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'Không có file audio'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'Chưa chọn file'}), 400
        
        # Tạo file với đường dẫn tuyệt đối
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        filename = f"audio_{timestamp}.wav"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"💾 Lưu file: {filepath}")
        audio_file.save(filepath)
        
        # Kiểm tra file tồn tại
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'Không thể lưu file'}), 500
        
        file_size = os.path.getsize(filepath)
        print(f"📊 File size: {file_size} bytes")
        
        if file_size < 100:
            os.remove(filepath)
            return jsonify({'success': False, 'error': 'File quá nhỏ'}), 400
        
        # Nhận diện
        print("🎯 Đang nhận diện...")
        result = model.transcribe(
            filepath,
            language='en',
            task='transcribe',
            fp16=False,
            temperature=0.0
        )
        
        transcript = result['text'].strip()
        print(f"✅ Kết quả: {transcript[:100]}...")
        
        # Xóa file
        try:
            os.remove(filepath)
            print(f"🗑️ Đã xóa file: {filename}")
        except:
            pass
        
        return jsonify({
            'success': True,
            'text': transcript,
            'language': result.get('language', 'en')
        })
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'message': 'Server is running!',
        'upload_folder': UPLOAD_FOLDER,
        'files': os.listdir(UPLOAD_FOLDER)[:5]
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 WHISPER SERVER ĐANG KHỞI ĐỘNG")
    print("="*50)
    print(f"📍 http://localhost:5000")
    print(f"📊 Model: {MODEL_SIZE}")
    print(f"💻 Device: {device}")
    print(f"📁 Upload: {UPLOAD_FOLDER}")
    print("="*50)
    print("\n✅ Server sẵn sàng!\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
