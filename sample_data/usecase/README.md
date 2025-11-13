# Use Case Examples

이 디렉토리는 실제 사용 사례를 보여주는 예제 데이터를 포함합니다.

## 개요

slide-renderer는 다양한 형태의 비구조화된 데이터를 LLM을 통해 구조화된 프레젠테이션으로 변환할 수 있습니다.

**워크플로우:**
```
비구조화된 데이터 (JSON) → LLM 구조화 → 슬라이드 JSON → Marp Markdown → PDF/HTML/PPTX
```

---

## Use Cases

### 1. 📄 Academic Paper to Presentation

**디렉토리**: `paper/`

**목적**: 학술 논문 데이터를 프레젠테이션으로 자동 변환

**입력 데이터**: `attention_is_all_you_need.json`
- Abstract: 논문 초록
- Method: 방법론 설명
- Performance: 실험 결과
- Conclusion: 결론

**출력**: 10장 이내의 프레젠테이션
- Title slide: 논문 제목과 주요 기여
- Abstract highlight: 핵심 문제와 솔루션
- Method explanation: 방법론 설명
- Performance metrics: 성능 결과
- Conclusion quote: 인상적인 결론

**실행 방법**:
```bash
# 논문 JSON을 프레젠테이션으로 변환
make paper

# 또는 직접 실행
python examples/paper_to_presentation.py

# PDF로 변환
make render-pdf MARKDOWN_FILE=attention_is_all_you_need_presentation.md
```

**예제 파일**:
- 입력: `sample_data/usecase/paper/attention_is_all_you_need.json`
- 스크립트: `examples/paper_to_presentation.py`

---

## 데이터 구조 예시

### Paper JSON 구조

```json
{
  "abstract": [
    {
      "header_id": "header_0_1",
      "header_text": "Abstract",
      "level": 1,
      "paragraphs": ["Abstract text..."],
      "figures": []
    }
  ],
  "method": [
    {
      "header_id": "S3",
      "header_text": "3 Model Architecture",
      "level": 2,
      "paragraphs": ["Method description..."],
      "figures": [
        {
          "figure_id": "S3.F1",
          "absolute_url": "https://...",
          "caption": "Figure 1: ...",
          "width": 912,
          "height": 1344
        }
      ]
    }
  ],
  "performance": [...],
  "conclusion": [...]
}
```

### LLM 구조화 출력 (Presentation JSON)

```json
{
  "title": "Attention Is All You Need",
  "slides": [
    {
      "type": "title_slide",
      "content": {
        "title": "Attention Is All You Need",
        "subtitle": "Transformer 아키텍처 소개"
      }
    },
    {
      "type": "highlight",
      "content": {
        "title": "핵심 아이디어",
        "content": "Recurrence와 Convolution 없이 Attention만으로..."
      }
    },
    {
      "type": "metrics_grid",
      "content": {
        "title": "성능 결과",
        "description": "WMT 2014 번역 태스크",
        "metrics": [
          {"value": "28.4", "label": "EN-DE BLEU"},
          {"value": "41.8", "label": "EN-FR BLEU"},
          {"value": "3.5일", "label": "학습 시간"},
          {"value": "8 GPUs", "label": "사용 자원"}
        ]
      }
    }
  ]
}
```

---

## LLM 프롬프트 전략

### 1. 명확한 구조 요구

```python
prompt = f"""
당신은 학술 논문을 프레젠테이션으로 변환하는 전문가입니다.

## 요구사항
1. 슬라이드 구성 (최대 10장):
   - Title slide: 논문 제목과 주요 기여
   - Highlight: 핵심 문제와 솔루션
   - Vertical list: 방법론 (3-4개)
   - Metrics grid: 성능 (정확히 4개)
   - Quote: 결론 인용

2. 슬라이드 타입별 제약:
   - metrics_grid: 정확히 4개 메트릭 필요
   - vertical_list: 3-6개 항목
   - quote: 최대 500자

## JSON 스키마
{schema}
"""
```

### 2. 예시 기반 학습

LLM에게 좋은 예시를 제공하면 더 나은 결과를 얻을 수 있습니다:

```python
example = {
    "type": "metrics_grid",
    "content": {
        "title": "성능 결과",
        "description": "WMT 2014 번역 태스크",
        "metrics": [
            {"value": "28.4", "label": "BLEU (EN-DE)"},
            {"value": "41.8", "label": "BLEU (EN-FR)"},
            {"value": "3.5일", "label": "학습 시간"},
            {"value": "8 GPUs", "label": "자원"}
        ]
    }
}
```

### 3. Temperature 조정

- **구조화 작업**: `temperature=0.3~0.5` (일관성)
- **창의적 내용**: `temperature=0.7~0.9` (다양성)

---

## 확장 가능한 Use Cases

### 추가 가능한 사용 사례

1. **📊 Business Report**
   - 입력: 분기별 실적 데이터
   - 출력: 경영진 보고 프레젠테이션

2. **📚 Documentation**
   - 입력: API 문서, 사용자 가이드
   - 출력: 온보딩 프레젠테이션

3. **📰 News Summary**
   - 입력: 뉴스 기사 모음
   - 출력: 일일 브리핑 슬라이드

4. **💼 Meeting Notes**
   - 입력: 회의록
   - 출력: 액션 아이템 정리 슬라이드

5. **🎓 Educational Content**
   - 입력: 교재 챕터
   - 출력: 강의 슬라이드

---

## 개발 가이드

### 새로운 Use Case 추가하기

1. **데이터 준비**
   ```bash
   mkdir sample_data/usecase/your_usecase
   # JSON 데이터 추가
   ```

2. **변환 스크립트 작성**
   ```python
   # examples/your_usecase_example.py
   def convert_your_data_to_presentation(data):
       prompt = create_prompt(data)
       llm_response = call_llm(prompt)
       presentation = parse_response(llm_response)
       return render_presentation(presentation)
   ```

3. **Makefile 명령어 추가**
   ```makefile
   your_usecase: ## Convert your data to presentation
       @python examples/your_usecase_example.py
   ```

4. **문서화**
   - 이 README에 사용 사례 추가
   - 예제 데이터 설명
   - 실행 방법 안내

---

## 트러블슈팅

### LLM이 잘못된 구조 생성

**문제**: 메트릭 개수가 4개가 아님

**해결**:
```python
prompt += """
⚠️ 중요: metrics_grid는 정확히 4개의 메트릭이 필요합니다.
3개나 5개가 아닌 정확히 4개여야 합니다.
"""
```

### JSON 파싱 실패

**문제**: LLM이 마크다운 코드 블록으로 감쌈

**해결**: `examples/paper_to_presentation.py`의 `parse_llm_response()` 참고

### 검증 오류

**문제**: Pydantic 검증 실패

**해결**:
1. LLM 응답 확인
2. 프롬프트에 제약 조건 명시
3. 예시 추가

---

## 참고 자료

- **Paper JSON 소스**: arXiv HTML API
- **LLM 프롬프트 가이드**: [SOLAR_PRO2_GUIDE.md](../../SOLAR_PRO2_GUIDE.md)
- **슬라이드 타입**: [README.md](../../README.md#slide-types)
- **스키마 정의**: `src/slide_renderer/schemas/content.py`

---

**Last Updated**: 2025-01-13
