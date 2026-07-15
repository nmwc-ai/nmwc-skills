---
name: wl-audio
description: 음성 파일을 받아써(STT) 오늘 Daily의 오프라인 활동에 반영한다. git에 안 잡히는 비-git 작업을 음성으로 수집하는 보완 경로. "이 음성 메모 일지에 넣어줘", "녹음 받아써서 오늘 일지에" 요청 시 사용.
---

# worklog 오디오 받아쓰기

음성 메모/녹음을 텍스트로 전사(STT)해 **오늘** Daily의 `## 오프라인 활동`에 넣는다.
worklog의 약한 고리인 "비-git 오프라인 활동 수집"을 음성 입력으로 메우는 보완 스킬.

> ⚠️ STT 엔진은 머신마다 다를 수 있다. 1단계에서 가용 엔진을 탐지하고, 없으면 설치를 안내한다.
> 환경이 Apple Silicon이면 `mlx-whisper`(빠름)를, 아니면 `whisper.cpp` 또는 OpenAI Whisper API를 쓴다.

## 실행 절차

### 1단계: 입력 + STT 엔진 탐지

```bash
ls -la "<오디오 파일 경로>"   # 사용자가 알려준 오디오 파일 경로 (없으면 경로 요청 후 중단)
# 가용 STT 엔진 탐지 (우선순위: mlx-whisper > whisper.cpp > openai-whisper > OpenAI API)
command -v mlx_whisper || command -v whisper-cli || command -v whisper || \
  { [ -n "$OPENAI_API_KEY" ] && echo "OpenAI Whisper API 사용 가능"; } || \
  echo "STT 엔진 없음 — 설치 필요"
```

- 엔진이 하나도 없으면 설치를 **안내만** 한다(자동 설치 금지). 권장:
  - Apple Silicon: `pip install mlx-whisper` (또는 `uv pip install mlx-whisper`)
  - 범용 로컬: `brew install whisper-cpp` + 모델 다운로드(`~/.whisper-models/ggml-small.bin`)
  - 클라우드: `OPENAI_API_KEY` 설정 후 Whisper API
- 포맷 변환이 필요하면 `ffmpeg`로 16kHz mono wav로 변환: `ffmpeg -i "<파일>" -ar 16000 -ac 1 /tmp/wl-audio.wav`

### 2단계: 전사 (한국어)

탐지된 엔진으로 전사한다(한국어 기본, `-l ko`).

```bash
# mlx-whisper (Apple Silicon 권장)
mlx_whisper "<파일>" --language ko --output-dir /tmp
# 또는 whisper.cpp
whisper-cli -m ~/.whisper-models/ggml-small.bin -l ko -f /tmp/wl-audio.wav
# 또는 OpenAI API (curl /v1/audio/transcriptions, model=whisper-1, language=ko)
```

### 3단계: 확인 후 worklog 반영

- 전사 텍스트를 사용자에게 **보여 확인**받는다(오인식 교정 기회).
- 확인된 텍스트를 오늘 Daily의 `## 오프라인 활동`(`<!-- manual-start -->`~`<!-- manual-end -->`)에 추가한다.
  이는 wl-note와 같은 반영 경로다 — Daily 작성 로직은 worklog 스킬에 위임하고 중복 구현하지 않는다.
- 긴 전사는 핵심만 요약해 넣고, 원문이 필요하면 `Offline/YYYY-MM-DD-audio.md`에 보관 후 Daily에서 링크한다.

## 검증 체크리스트

- [ ] 입력 오디오 파일 존재를 실제로 확인했는가?
- [ ] STT 엔진을 탐지했는가? 없으면 설치만 안내하고 자동 설치하지 않았는가?
- [ ] 전사 결과를 일지에 넣기 전 사용자에게 보여 확인받았는가?
- [ ] 오늘(`date +%F`) Daily의 오프라인 활동 블록에 넣었는가? (과거 날짜·git 활동은 소관 아님)
- [ ] Daily 작성을 worklog 스킬에 위임했는가(중복 구현 금지)?
