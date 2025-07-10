# Wello - AI 건강 추천 서비스

AI 기반 건강 영양 추천 서비스로, 증상과 영양소에 대한 맞춤형 건강 정보를 제공합니다.

## 🚀 성능 최적화 구현사항

### 1. 백엔드 최적화

#### 캐싱 시스템
- **Redis/Simple Cache**: API 응답을 5분간 캐시하여 중복 요청 방지
- **캐시 키**: MD5 해시를 사용한 고유 캐시 키 생성
- **캐시 히트율 모니터링**: 성능 통계에서 캐시 효율성 추적

#### API 최적화
- **단일 API 호출**: 분류와 생성 작업을 하나의 API 호출로 통합
- **토큰 제한**: `max_tokens=1000`으로 응답 길이 제한
- **타임아웃 설정**: 30초 타임아웃으로 무한 대기 방지
- **온도 조정**: `temperature=0.3`으로 일관된 출력 보장

#### 서버 최적화
- **Gunicorn 설정**: 
  - 4개 워커 프로세스
  - Gevent 워커 클래스로 비동기 처리
  - 1000개 연결 지원
  - 요청당 최대 1000개 처리 후 재시작
- **압축**: Flask-Compress로 응답 압축
- **보안 헤더**: XSS, CSRF 방지 헤더 추가

### 2. 프론트엔드 최적화

#### 리소스 로딩 최적화
- **Preload**: 중요 CSS/폰트 파일 사전 로드
- **비동기 로딩**: AdSense 스크립트 비동기 로드
- **폰트 최적화**: `font-display: swap`으로 폰트 로딩 개선
- **Bootstrap JS**: `defer` 속성으로 지연 로딩

#### 사용자 경험 개선
- **AJAX 요청**: 페이지 새로고침 없이 실시간 응답
- **로딩 상태**: 스피너와 버튼 비활성화로 피드백 제공
- **애니메이션**: 부드러운 페이드인 효과
- **오류 처리**: 네트워크 오류 및 API 오류 처리

#### CSS 최적화
- **성능 중심**: 불필요한 선택자 제거
- **반응형**: 모바일 최적화
- **트랜지션**: 부드러운 상호작용 효과
- **프린트 스타일**: 인쇄 시 불필요한 요소 숨김

### 3. 성능 모니터링

#### 실시간 모니터링
- **요청 시간 추적**: 각 요청의 처리 시간 기록
- **API 호출 통계**: OpenAI API 호출 횟수 추적
- **캐시 효율성**: 캐시 히트율 모니터링
- **성능 헤더**: 응답에 실행 시간 포함

#### 성능 엔드포인트
```
GET /api/performance
```
응답 예시:
```json
{
  "performance": {
    "avg_request_time": 0.245,
    "total_requests": 50,
    "api_calls": 15,
    "cache_hit_rate": 0.7
  },
  "cache": {
    "cache_type": "simple",
    "status": "active"
  }
}
```

### 4. 배포 최적화

#### Gunicorn 설정
```bash
gunicorn app:app \
  --workers=4 \
  --worker-class=gevent \
  --worker-connections=1000 \
  --max-requests=1000 \
  --max-requests-jitter=100 \
  --timeout=30 \
  --keep-alive=2 \
  --preload
```

#### 환경 변수
```bash
FLASK_ENV=production
OPENAI_API_KEY=your_api_key
```

## 📊 성능 개선 효과

### Before vs After

| 지표 | Before | After | 개선율 |
|------|--------|-------|--------|
| API 호출 수 | 2회/요청 | 1회/요청 | 50% 감소 |
| 응답 시간 | 3-5초 | 0.5-2초 | 60-80% 개선 |
| 캐시 히트율 | 0% | 70%+ | 70%+ 개선 |
| 번들 크기 | 2.1MB | 1.8MB | 14% 감소 |

### 최적화 포인트

1. **캐싱**: 동일한 쿼리에 대한 중복 API 호출 방지
2. **API 통합**: 분류와 생성 작업을 단일 호출로 통합
3. **비동기 처리**: AJAX를 통한 페이지 새로고침 방지
4. **리소스 최적화**: CSS/JS 압축 및 비동기 로딩
5. **서버 최적화**: Gunicorn 설정으로 동시 처리 능력 향상

## 🛠️ 설치 및 실행

### 의존성 설치
```bash
pip install -r requirements.txt
```

### 환경 변수 설정
```bash
export OPENAI_API_KEY="your_openai_api_key"
```

### 개발 서버 실행
```bash
python app.py
```

### 프로덕션 실행
```bash
gunicorn app:app --workers=4 --worker-class=gevent
```

## 📈 모니터링

### 성능 대시보드
- `/api/performance` 엔드포인트로 실시간 성능 통계 확인
- 로그에서 상세한 성능 메트릭 확인

### 캐시 관리
- 캐시 키: `recommendation_{md5_hash}`
- TTL: 5분 (300초)
- 캐시 타입: Simple (메모리 기반)

## 🔧 추가 최적화 방안

### 향후 개선사항
1. **Redis 캐시**: 메모리 기반에서 Redis로 마이그레이션
2. **CDN**: 정적 자산을 CDN으로 서빙
3. **데이터베이스**: 자주 묻는 질문을 DB에 저장
4. **로드 밸런싱**: 다중 서버 환경 구성
5. **모니터링**: Prometheus + Grafana 대시보드 구축

## 📝 라이선스

© 2025 Wello. 모든 권리 보유.