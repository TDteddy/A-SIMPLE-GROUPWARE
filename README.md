# BRYZE Groupware

BRYZE 사내 게시판 및 그룹웨어 시스템입니다. Google Workspace 계정으로 로그인하여 사용할 수 있습니다.

## 주요 기능

- **Google OAuth 인증**: Google Workspace 계정으로 안전한 로그인
- **사내 게시판**: 공지사항, 일반 게시글 작성/수정/삭제
- **게시글 관리**: 공지사항 설정, 상단 고정, 조회수 관리
- **권한 관리**: 일반 사용자 및 관리자 권한 구분
- **관리자 페이지**:
  - 대시보드 (통계 및 현황)
  - 사용자 관리 (권한 부여, 계정 활성화/비활성화)
  - 게시글 관리 (전체 게시글 조회 및 삭제)
- **반응형 디자인**: 데스크톱 및 모바일 환경 지원

## 기술 스택

### Backend
- **FastAPI**: 최신 Python 웹 프레임워크
- **MySQL**: 관계형 데이터베이스
- **SQLAlchemy**: ORM
- **Google OAuth 2.0**: 인증
- **JWT**: 토큰 기반 인증

### Frontend
- **React 18**: UI 라이브러리
- **Vite**: 빌드 도구
- **React Router**: 라우팅
- **Axios**: HTTP 클라이언트
- **@react-oauth/google**: Google OAuth 연동

## 시작하기

### 사전 요구사항

- Docker & Docker Compose
- Google Cloud Console 프로젝트 (OAuth 클라이언트 ID)

### Google OAuth 설정

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. "API 및 서비스" > "사용자 인증 정보" 이동
4. "사용자 인증 정보 만들기" > "OAuth 클라이언트 ID" 선택
5. 애플리케이션 유형: "웹 애플리케이션"
6. **승인된 자바스크립트 원본** (실행 환경에 따라 추가):
   - 로컬 개발: `http://localhost:3000`
   - 개발/스테이징: `https://dev.bryze.kr` (예시)
   - 프로덕션: `https://groupware.bryze.kr` (예시)
7. **승인된 리디렉션 URI** (실행 환경에 따라 추가):
   - 로컬 개발: `http://localhost:3000/auth/callback`
   - 개발/스테이징: `https://dev.bryze.kr/auth/callback` (예시)
   - 프로덕션: `https://groupware.bryze.kr/auth/callback` (예시)
8. 생성된 클라이언트 ID와 클라이언트 보안 비밀번호 복사

> **참고**: Google OAuth는 여러 개의 승인된 원본과 리디렉션 URI를 동시에 등록할 수 있습니다.
> 환경별로 별도의 OAuth 클라이언트를 만들거나, 하나의 클라이언트에 모든 환경의 URL을 등록할 수 있습니다.

### 설치 및 실행

1. **저장소 클론**
```bash
git clone <repository-url>
cd A-SIMPLE-GROUPWARE
```

2. **환경 변수 설정**
```bash
cp .env.example .env
```

`.env` 파일을 열어 다음 값을 설정하세요 (로컬 개발 환경 기준):
```env
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
SECRET_KEY=your-secret-key-change-in-production
ALLOWED_DOMAIN=bryze.kr
FRONTEND_URL=http://localhost:3000
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback
```

3. **프론트엔드 환경 변수 설정**
```bash
cp frontend/.env.example frontend/.env
```

`frontend/.env` 파일을 열어 다음 값을 설정하세요 (로컬 개발 환경 기준):
```env
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
VITE_API_URL=http://localhost:8000
```

> **프로덕션 환경**: 실제 배포 시에는 위 URL들을 실제 도메인으로 변경해야 합니다.
> 예: `FRONTEND_URL=https://groupware.bryze.kr`, `VITE_API_URL=https://api.bryze.kr`

4. **Docker Compose로 실행**
```bash
docker-compose up -d
```

5. **애플리케이션 접속**
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 수동 설치 (Docker 없이)

### Backend 설정

1. **Python 가상환경 생성 및 활성화**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **환경 변수 설정**
```bash
cp .env.example .env
# .env 파일 수정
```

4. **MySQL 데이터베이스 생성**
```sql
CREATE DATABASE bryze_groupware;
```

5. **서버 실행**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend 설정

1. **의존성 설치**
```bash
cd frontend
npm install
```

2. **환경 변수 설정**
```bash
cp .env.example .env
# .env 파일 수정
```

3. **개발 서버 실행**
```bash
npm run dev
```

## 프로젝트 구조

```
A-SIMPLE-GROUPWARE/
├── backend/
│   ├── app/
│   │   ├── api/           # API 엔드포인트
│   │   │   ├── auth.py    # 인증 관련
│   │   │   ├── users.py   # 사용자 관리
│   │   │   └── posts.py   # 게시글 관리
│   │   ├── core/          # 핵심 설정
│   │   │   ├── config.py  # 환경 설정
│   │   │   ├── database.py # DB 연결
│   │   │   └── security.py # 보안 (JWT)
│   │   ├── models/        # DB 모델
│   │   │   ├── user.py
│   │   │   └── post.py
│   │   ├── schemas/       # Pydantic 스키마
│   │   └── main.py        # FastAPI 앱
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/    # 재사용 컴포넌트
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── context/       # React Context
│   │   ├── services/      # API 서비스
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## API 엔드포인트

### 인증
- `POST /api/auth/google` - Google OAuth 로그인
- `GET /api/auth/me` - 현재 사용자 정보

### 사용자
- `GET /api/users/` - 사용자 목록
- `GET /api/users/{user_id}` - 사용자 상세

### 게시글
- `GET /api/posts/` - 게시글 목록
- `GET /api/posts/{post_id}` - 게시글 상세
- `POST /api/posts/` - 게시글 작성
- `PUT /api/posts/{post_id}` - 게시글 수정
- `DELETE /api/posts/{post_id}` - 게시글 삭제

### 관리자 (Admin only)
- `GET /api/admin/stats` - 대시보드 통계
- `GET /api/admin/users` - 모든 사용자 목록
- `PATCH /api/admin/users/{user_id}` - 사용자 권한/상태 변경
- `GET /api/admin/posts` - 모든 게시글 목록
- `DELETE /api/admin/posts/{post_id}` - 게시글 삭제

## 보안 설정

### 도메인 제한
`.env` 파일의 `ALLOWED_DOMAIN`을 설정하여 특정 도메인의 Google 계정만 로그인할 수 있도록 제한합니다.

```env
ALLOWED_DOMAIN=bryze.kr
```

이 설정으로 `@bryze.kr` 이메일만 로그인이 허용됩니다.

### JWT Secret Key
프로덕션 환경에서는 반드시 강력한 비밀 키를 생성하여 사용하세요:

```bash
# Python으로 생성
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 프로덕션 배포

프로덕션 환경에서는 다음 사항을 확인하세요:

1. **환경 변수**: 모든 비밀 값을 안전하게 관리
   - `SECRET_KEY`: 강력한 랜덤 키 생성
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: 프로덕션용 OAuth 클라이언트 사용

2. **URL 설정**: 실제 도메인으로 변경
   - Backend `.env`:
     ```env
     FRONTEND_URL=https://groupware.bryze.kr
     GOOGLE_REDIRECT_URI=https://groupware.bryze.kr/auth/callback
     ```
   - Frontend `.env`:
     ```env
     VITE_API_URL=https://api.bryze.kr
     VITE_GOOGLE_CLIENT_ID=your-production-client-id
     ```
   - Google Cloud Console에서 프로덕션 URL을 승인된 원본 및 리디렉션 URI로 등록

3. **HTTPS**: SSL/TLS 인증서 적용
   - Let's Encrypt 또는 유료 인증서 사용
   - Nginx/Apache 리버스 프록시 설정

4. **데이터베이스**: 안전한 비밀번호 및 백업 설정

5. **CORS**: 프론트엔드 도메인만 허용

6. **로깅**: 적절한 로깅 레벨 설정

7. **모니터링**: 서버 및 애플리케이션 모니터링 구성

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다.

## 연락처

문제가 있거나 질문이 있으시면 이슈를 생성해주세요.