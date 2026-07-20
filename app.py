if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 WHISPER SERVER ĐANG KHỞI ĐỘNG")
    print("="*50)
    print(f"📊 Model: {MODEL_SIZE}")
    print(f"💻 Device: {device}")
    print(f"📁 Upload: {UPLOAD_FOLDER}")
    print("="*50)
    print("\n✅ Server sẵn sàng!\n")
    
    # Lấy port từ biến môi trường Render
    port = int(os.environ.get('PORT', 5000))
    # Tắt debug trên production
    app.run(host='0.0.0.0', port=port, debug=False)
