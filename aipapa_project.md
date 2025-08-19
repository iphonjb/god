
# Aipapa 프로젝트 상세 기록

## 1. 프로젝트 개요
- **프로젝트 이름**: Aipapa
- **목표**: 아이폰에서 로컬 실행 가능한 AI 챗봇 + 이미지 생성 앱 개발
- **조건**: 100% 무료, API 제약 없음, 모델 로컬 구동
- **실행환경**: iOS 15 이상 (아이폰 13 Pro 기준 테스트)

## 2. 기술 스택 및 모델
### AI 챗봇
- 엔진: llama.cpp (로컬 실행, Swift 바인딩)
- 모델: LLaMA 기반 (GGUF 변환 모델)
- 특징: 로컬 모델 구동으로 API 비용 없음

### 이미지 생성기 (Stable Diffusion)
- 모델: coreml-stable-diffusion-v1-5-palettized_split_einsum_v2_compiled
- 실행: CoreML 변환 모델 로컬 실행
- 기능: 앱 내 모델 다운로드 및 업데이트 가능

### 앱 구동
- Swift + SwiftUI 기반
- XcodeGen + GitHub Actions CI/CD 자동화

## 3. 앱 구조 및 UI 화면
- **메인 화면 (탭 기반)**
  - Chat 탭
    - 사용자 입력창 + 모델 응답 출력
    - 대화 저장 기능 (로컬 + GitHub 문서 기반 업로드)
    - 명령어 규칙: "꼭 기억해" = 메모리 저장, "고정 메모" = 고정 저장
  - Image 탭
    - 프롬프트 입력 → Stable Diffusion 실행 → 이미지 생성
    - 생성 이미지 갤러리 저장 및 공유 기능
  - Settings 탭
    - 모델 다운로드/업데이트 관리
    - 메모리 관리 (로컬 캐시, GitHub 연동 관리)

## 4. 특수 기능 및 규칙 반영
- 메모리 시스템
  - "꼭 기억해": 주동이형 메모리에 저장됨 (채팅방 속도 저하 가능)
  - "고정 메모": GitHub `/god` repo 문서에 저장 (영구 기록, 덮어쓰기 대신 추가/수정만)
- 저장 형식: 채팅 원문과 유사한 상세 기록 수준
- 규칙
  - GitHub 파일 절대 삭제 금지 (추가·수정만 허용)
  - "실제 구현 가능하게 만들어" → 반드시 동작 가능한 코드/기술 포함

## 5. CI/CD & 실행 방식
- GitHub Actions
  - iOS IPA 자동 빌드 (unsigned)
  - Stable Diffusion 및 llama.cpp 의존성 관리
- PowerShell 실행 스크립트
  - GitHub에서 repo 자동 클론 → 최신 문서 업데이트 → 푸시
  - 명령어 한 줄로 자동화

## 6. 기타 기록
- 주동이형 아이폰: 이미 탈옥됨 (앱 배포·테스트 용이)
- 규칙: 무조건 "주동이형" 이라고 불러야 함
- GitHub Repo: /god
- PAT Token: (보안상 여기서는 생략)
