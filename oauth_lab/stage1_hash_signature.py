"""
CHẶNG 1 — Hash (vân tay) & Chữ ký số (con dấu)

Hình ảnh:
  - Hash       = "vân tay" của dữ liệu: đổi 1 chữ -> vân tay khác hẳn.
  - Private key= con dấu gốc, chỉ lễ tân (Auth Server) giữ trong két.
  - Signature  = vết dấu đóng lên giấy (thẻ ra vào).
  - Public key = mẫu dấu dán công khai ở cửa: ai cũng so được, không ai khắc lại được.

Chạy:  python stage1_hash_signature.py
"""
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# 👉 Bài "phá thử": sửa các hằng số này rồi chạy lại
TEN_1 = "Peter"
TEN_2 = "Petar"
CAU_GOC = "Peter duoc phep xem bao cao"
CAU_BI_SUA = "Peter duoc phep xem bao cao!"   # thêm đúng 1 ký tự "!"


def line(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# ---------------------------------------------------------------------
# BƯỚC 1: HASH — lấy "vân tay" SHA-256
# ---------------------------------------------------------------------
line("BƯỚC 1: Hash (vân tay) của 2 cái tên")

h1 = hashlib.sha256(TEN_1.encode()).hexdigest()
h2 = hashlib.sha256(TEN_2.encode()).hexdigest()
print(f"SHA-256('{TEN_1}') = {h1}")
print(f"SHA-256('{TEN_2}') = {h2}")

# Đếm xem bao nhiêu bit (trong 256 bit) bị khác nhau
bit_khac = bin(int(h1, 16) ^ int(h2, 16)).count("1")
print(f"\n-> Input chỉ khác 1 chữ, nhưng {bit_khac}/256 bit của vân tay bị lật "
      f"(~{bit_khac / 256:.0%}). Đây gọi là 'hiệu ứng tuyết lở'.")
print("-> Vân tay LUÔN dài 64 ký tự hex, dù input là 1 chữ hay 1 cuốn sách.")
print("-> Từ vân tay KHÔNG thể suy ngược ra input (hàm một chiều).")

# ---------------------------------------------------------------------
# BƯỚC 2: Tạo cặp khóa RSA — khắc con dấu + in mẫu dấu
# ---------------------------------------------------------------------
line("BƯỚC 2: Tạo cặp khóa RSA (con dấu + mẫu dấu)")

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

pem = public_key.public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
).decode()
print("Public key (mẫu dấu, dán công khai):")
print(pem.strip()[:120] + " ...")
print(f"\nĐộ dài khóa: {private_key.key_size} bit")
print("Private key (con dấu gốc): KHÔNG in ra — nó phải nằm trong két!")

# ---------------------------------------------------------------------
# BƯỚC 3: KÝ — đóng dấu lên câu
# ---------------------------------------------------------------------
line("BƯỚC 3: Ký (đóng dấu) lên câu gốc")

# Bên trong sign(): (1) hash câu bằng SHA-256  (2) "khóa" vân tay đó bằng private key
van_tay = hashlib.sha256(CAU_GOC.encode()).hexdigest()
print(f"Câu gốc       : '{CAU_GOC}'")
print(f"Vân tay câu   : {van_tay}")

chu_ky = private_key.sign(CAU_GOC.encode(), padding.PKCS1v15(), hashes.SHA256())
print(f"Chữ ký ({len(chu_ky)} byte): {chu_ky.hex()[:64]}...")
print("-> Thứ được ký thực chất là VÂN TAY của câu, không phải cả câu.")

# ---------------------------------------------------------------------
# BƯỚC 4: VERIFY — so vết dấu với mẫu dấu
# ---------------------------------------------------------------------
line("BƯỚC 4: Kiểm tra chữ ký (so với mẫu dấu)")


def verify(pub, message, signature, mo_ta):
    """Trả True nếu chữ ký khớp. Bên trong: hash message, rồi dùng public key
    'mở' chữ ký ra để xem có đúng vân tay đó không."""
    print(f"\n[{mo_ta}]")
    print(f"  Câu đem kiểm tra: '{message}'")
    print(f"  Vân tay của nó  : {hashlib.sha256(message.encode()).hexdigest()[:32]}...")
    try:
        pub.verify(signature, message.encode(), padding.PKCS1v15(), hashes.SHA256())
        print("  Kết quả: ✅ HỢP LỆ — đúng dấu thật, nội dung nguyên vẹn")
        return True
    except InvalidSignature:
        print("  Kết quả: ❌ GIẢ / BỊ SỬA — vết dấu không khớp")
        return False


# 4a. Câu gốc + chữ ký gốc + mẫu dấu đúng
verify(public_key, CAU_GOC, chu_ky, "Test A: câu gốc, mẫu dấu đúng")

# 4b. Sửa 1 ký tự nhưng vẫn dùng chữ ký cũ
verify(public_key, CAU_BI_SUA, chu_ky, "Test B: câu bị sửa 1 ký tự, giữ chữ ký cũ")

# 4c. Kẻ gian tự tạo con dấu riêng -> so với mẫu dấu thật của lễ tân
ke_gian_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
chu_ky_gia = ke_gian_key.sign(CAU_BI_SUA.encode(), padding.PKCS1v15(), hashes.SHA256())
verify(public_key, CAU_BI_SUA, chu_ky_gia, "Test C: kẻ gian ký bằng con dấu riêng")

line("TÓM TẮT")
print("1. Hash: đổi 1 chữ -> vân tay khác hoàn toàn.")
print("2. Chữ ký = vân tay được 'khóa' bằng private key. Chỉ chủ con dấu tạo được.")
print("3. Ai có public key cũng kiểm tra được, nhưng không thể tạo chữ ký mới.")
print("=> Đây chính là nền móng của JWT ở Chặng 2.")
