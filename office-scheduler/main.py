# main.py  ←  Entry point: chạy file này để khởi động server
# Cách chạy: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from backend.database import init_db
from backend.auth import hash_password
from backend.database import SessionLocal, User
from backend.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Chạy khi server khởi động: tạo DB và tạo admin mặc định."""
    try:
        init_db()
        _create_default_admin()
    except Exception as e:
        print(f"Loi khoi tao database: {e}")
        print("Server van khoi dong, nhung database co the chua san sang.")
    yield


def _create_default_admin():
    """Tạo tài khoản admin mặc định nếu chưa có."""
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                full_name="Quản trị viên",
                role="admin"
            )
            db.add(admin)
            db.commit()
            print("Da tao tai khoan admin mac dinh: admin / admin123")
            print("Hay doi mat khau sau khi dang nhap lan dau!")
    finally:
        db.close()


# ─── Khởi tạo FastAPI app ──────────────────────────────────────────────────
app = FastAPI(
    title="Office Scheduler",
    description="Hệ thống đăng ký lịch lên văn phòng nội bộ",
    version="1.0.0",
    lifespan=lifespan
)

# CORS: cho phép frontend (trên cùng máy hoặc LAN) gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trên LAN nội bộ, cho phép tất cả origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount thư mục static để serve file CSS/JS
STATIC_DIR = "public/static" if os.path.isdir("public/static") else "frontend/static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Đăng ký tất cả API routes với prefix /api
app.include_router(router, prefix="/api")


# ─── Serve Frontend HTML ───────────────────────────────────────────────────
FRONTEND_DIR = "public" if os.path.isdir("public") else "frontend"

@app.get("/", include_in_schema=False)
def serve_root():
    """Trả về trang login."""
    return FileResponse(f"{FRONTEND_DIR}/index.html")


@app.get("/dashboard", include_in_schema=False)
def serve_dashboard():
    """Trả về trang dashboard."""
    return FileResponse(f"{FRONTEND_DIR}/dashboard.html")


@app.get("/admin", include_in_schema=False)
def serve_admin():
    """Trả về trang quản lý admin."""
    return FileResponse(f"{FRONTEND_DIR}/admin.html")
