# OAuth 2.0 Token Exchange (RFC 8693): học bằng cách tự làm

Dự án học tập, **không dùng cho production**.

## Cài đặt
```bash
cd oauth_lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Các chặng
| Chặng | Nội dung | Chạy |
|---|---|---|
| 1 | Hash & chữ ký số | `python stage1_hash_signature.py` |
| 2 | Tự tạo JWT bằng tay | (sắp có) |
| 3 | Auth Server :8000 + Service B :8002 (JWKS) | (sắp có) |
| 4 | Token Exchange: App A :8001 → B | (sắp có) |
| 5 | Chuỗi A → B → C :8003 | (sắp có) |
