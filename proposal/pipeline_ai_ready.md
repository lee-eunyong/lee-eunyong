# AI-Ready 데이터 가공 파이프라인

> 인공지능(AI)·머신러닝(ML) 모델이 **추가적인 전처리 없이 즉시 학습·예측에 사용**할 수 있도록
> 데이터를 정제·구조화하는 일련의 과정.
>
> *"데이터가 새 시대의 원유라면, AI-Ready 가공은 원유를 자동차에 바로 넣을 수 있는 휘발유로 만드는 정제 과정"*

---

## 📊 파이프라인 다이어그램 (Mermaid)

```mermaid
flowchart TB
    %% ===== 원천 데이터 =====
    subgraph SRC["🗂️ Raw Data Sources"]
        direction LR
        SRC1[정형<br/>RDB·DW]
        SRC2[반정형<br/>JSON·XML·CSV]
        SRC3[비정형<br/>Image·Text·Audio·Video]
        SRC4[스트리밍<br/>API·Log·IoT]
    end

    %% ===== 1단계 =====
    subgraph STG1["①  Data Collection · 수집"]
        direction LR
        A1[Ingestion<br/>Kafka·NiFi·Airbyte]
        A2[Sampling<br/>대표성·균형성 검증]
        A3[Bias Check<br/>분포·편향 진단]
    end

    %% ===== 2단계 =====
    subgraph STG2["②  Data Cleaning · 정제"]
        direction LR
        B1[Missing Value<br/>대체·삭제·KNN Imputer]
        B2[Outlier<br/>IQR·Z-score·Isolation Forest]
        B3[Deduplication<br/>해시·퍼지 매칭]
        B4[Noise/Typo<br/>정규식·맞춤법 보정]
    end

    %% ===== 3단계 =====
    subgraph STG3["③  Transformation & Labeling · 변환·라벨링"]
        direction LR
        C1[Encoding<br/>One-Hot·Label·Target]
        C2[Scaling<br/>MinMax·Standard·Robust]
        C3[Tokenize<br/>BPE·WordPiece·Sentence]
        C4[Labeling<br/>BBox·Polygon·NER·Sentiment]
    end

    %% ===== 4단계 =====
    subgraph STG4["④  Feature Engineering · 피처 엔지니어링"]
        direction LR
        D1[Extraction<br/>날짜→요일/공휴일·TF-IDF·Embedding]
        D2[Combination<br/>비율·차분·교차항]
        D3[Reduction<br/>PCA·t-SNE·UMAP]
        D4[Selection<br/>RFE·Mutual Info·SHAP]
    end

    %% ===== 5단계 =====
    subgraph STG5["⑤  Loading & MLOps · 적재·파이프라인"]
        direction LR
        E1[Feature Store<br/>Feast·Tecton]
        E2[Data Lake/WH<br/>S3·Iceberg·BigQuery]
        E3[Versioning<br/>DVC·MLflow·LakeFS]
        E4[Orchestration<br/>Airflow·Kubeflow·Dagster]
    end

    %% ===== 소비자 =====
    subgraph CON["🤖 AI/ML Consumers"]
        direction LR
        Z1[Training]
        Z2[Online Inference]
        Z3[Batch Prediction]
    end

    %% ===== 횡단 거버넌스 =====
    subgraph GOV["🛡️ Cross-cutting Governance"]
        direction LR
        G1[Privacy<br/>비식별·가명·DP]
        G2[Quality Monitor<br/>Great Expectations·Soda]
        G3[Schema Registry<br/>Avro·Protobuf]
        G4[Access Control<br/>IAM·Lineage·Audit]
    end

    SRC --> STG1 --> STG2 --> STG3 --> STG4 --> STG5 --> CON

    GOV -. enforce .-> STG1
    GOV -. enforce .-> STG2
    GOV -. enforce .-> STG3
    GOV -. enforce .-> STG4
    GOV -. enforce .-> STG5

    %% 피드백 루프
    CON -. drift/feedback .-> STG2
    STG5 -. retrain trigger .-> STG1

    classDef src fill:#e3f2fd,stroke:#1976d2,color:#0d47a1
    classDef s1 fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef s2 fill:#f3e5f5,stroke:#8e24aa,color:#4a148c
    classDef s3 fill:#e8f5e9,stroke:#43a047,color:#1b5e20
    classDef s4 fill:#fce4ec,stroke:#d81b60,color:#880e4f
    classDef s5 fill:#ede7f6,stroke:#5e35b1,color:#311b92
    classDef gov fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef con fill:#e0f7fa,stroke:#00838f,color:#006064

    class SRC,SRC1,SRC2,SRC3,SRC4 src
    class STG1,A1,A2,A3 s1
    class STG2,B1,B2,B3,B4 s2
    class STG3,C1,C2,C3,C4 s3
    class STG4,D1,D2,D3,D4 s4
    class STG5,E1,E2,E3,E4 s5
    class GOV,G1,G2,G3,G4 gov
    class CON,Z1,Z2,Z3 con
```

---

## 🖼️ 파이프라인 다이어그램 (ASCII)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AI-Ready 데이터 가공 파이프라인                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

  🗂️  RAW DATA SOURCES
  ┌──────────┬──────────────┬────────────────────┬──────────────┐
  │   정형   │   반정형     │      비정형        │  스트리밍    │
  │ RDB / DW │ JSON/XML/CSV │ Image/Text/A/V     │ API/Log/IoT  │
  └────┬─────┴──────┬───────┴─────────┬──────────┴──────┬───────┘
       └────────────┴─────────────────┴─────────────────┘
                                │
       ┌────────────────────────▼────────────────────────┐
       │ ① Data Collection · 수집                        │
       │   • Ingestion (Kafka / NiFi / Airbyte)          │
       │   • 대표성·균형성 샘플링 · Bias 진단            │
       └────────────────────────┬────────────────────────┘
                                ▼
       ┌─────────────────────────────────────────────────┐
       │ ② Data Cleaning · 정제                          │
       │   ┌─결측치──┐ ┌─이상치──┐ ┌─중복────┐ ┌─노이즈─┐│
       │   │ KNN 대체│ │ IQR/Z   │ │ Hash    │ │ Regex  ││
       │   │ 평균/중앙│ │IsoForest│ │ Fuzzy   │ │ Spell  ││
       │   └─────────┘ └─────────┘ └─────────┘ └────────┘│
       └────────────────────────┬────────────────────────┘
                                ▼
       ┌─────────────────────────────────────────────────┐
       │ ③ Transformation & Labeling · 변환·라벨링       │
       │   [정형]   Encoding (OneHot/Label/Target)       │
       │           Scaling  (MinMax/Standard/Robust)     │
       │   [텍스트] Tokenization (BPE/WordPiece)         │
       │   [이미지] BBox / Polygon / Segmentation        │
       │   [텍스트] NER / 감정태깅 / 의도분류            │
       └────────────────────────┬────────────────────────┘
                                ▼
       ┌─────────────────────────────────────────────────┐
       │ ④ Feature Engineering · 피처 엔지니어링         │
       │   • Extraction : 날짜→요일/공휴일, TF-IDF, Embed│
       │   • Combination: 비율, 차분, 교차항, 윈도우집계 │
       │   • Reduction  : PCA, t-SNE, UMAP, AutoEncoder  │
       │   • Selection  : RFE, MI, SHAP, L1 Regularize   │
       └────────────────────────┬────────────────────────┘
                                ▼
       ┌─────────────────────────────────────────────────┐
       │ ⑤ Loading & MLOps · 적재·파이프라인             │
       │   ┌──────────────┐  ┌──────────────────────┐    │
       │   │Feature Store │  │ Data Lake / Warehouse│    │
       │   │ Feast/Tecton │  │ S3·Iceberg·BigQuery  │    │
       │   └──────┬───────┘  └──────────┬───────────┘    │
       │   ┌──────▼───────┐  ┌──────────▼───────────┐    │
       │   │ Versioning   │  │ Orchestration        │    │
       │   │ DVC / MLflow │  │ Airflow/Kubeflow     │    │
       │   └──────────────┘  └──────────────────────┘    │
       └────────────────────────┬────────────────────────┘
                                ▼
            🤖 AI / ML  ─────────────────────────────
            ├─ Training       (학습)
            ├─ Online Serving (실시간 추론)
            └─ Batch Predict  (배치 예측)
                ▲
                │  drift / feedback
                └────── 재학습 트리거 ──┐
                                        │
  ╔════════════════════════════════════════════════════════════════════════╗
  ║ 🛡️  Cross-cutting Governance (전 단계 횡단)                           ║
  ║  Privacy(비식별·가명·DP) │ Quality(GE·Soda) │ Schema │ IAM/Lineage     ║
  ╚════════════════════════════════════════════════════════════════════════╝
```

---

## 🛠️ 단계별 상세

### ① Data Collection · 데이터 수집 및 데이터셋 구성
- **목적**: 흩어진 정형·반정형·비정형 데이터를 한 곳에 모음
- **AI-Ready 요건**: 모델 편향(Bias)을 막기 위한 **다양성·균형성** 확보
- **주요 도구**: Kafka, NiFi, Airbyte, Fluentd, Debezium

### ② Data Cleaning · 데이터 정제
| 작업 | 설명 | 기법 |
|---|---|---|
| 결측치 처리 | 비어 있는 값 보완·제거 | 평균/중앙값, KNN Imputer, MICE |
| 이상치 제거 | 극단값으로 인한 왜곡 방지 | IQR, Z-score, Isolation Forest |
| 중복 제거 | 과적합(Overfitting) 방지 | 정확 매칭, 퍼지 매칭(Levenshtein) |
| 노이즈 제거 | 오탈자·잡음 보정 | 정규식, 맞춤법 검사기 |

### ③ Transformation & Labeling · 데이터 변환 및 라벨링
- **정형 데이터**
  - Encoding: One-Hot, Label, Target, Ordinal
  - Scaling: Min-Max, Standard(Z-score), Robust, Log
- **비정형 데이터 (라벨링 = 정답지 부여)**
  - 이미지: Bounding Box, Polygon, Semantic Segmentation
  - 텍스트: NER, 감정 태깅, 의도 분류, RLHF 선호도
  - 음성: Transcription, Speaker Diarization

### ④ Feature Engineering · 피처 엔지니어링
- **추출(Extraction)**: 날짜 → 요일/공휴일/월말여부, 텍스트 → TF-IDF/Embedding
- **조합(Combination)**: 비율, 차분, 시계열 윈도우 집계, 교차항
- **차원 축소(Reduction)**: PCA, t-SNE, UMAP, AutoEncoder
- **선택(Selection)**: RFE, Mutual Information, SHAP, L1 Regularization

### ⑤ Loading & MLOps · 적재 및 파이프라인 구축
- **Feature Store**: Feast, Tecton (학습-서빙 일관성 보장)
- **Data Lake/Warehouse**: S3 + Iceberg, BigQuery, Snowflake
- **Versioning**: DVC, MLflow, LakeFS (재현성)
- **Orchestration**: Airflow, Kubeflow, Dagster, Prefect

---

## 🛡️ 횡단 거버넌스 (Cross-cutting Concerns)

모든 단계에 **동시 적용**되어야 하는 요소:

- **Privacy**: 가명화, 익명화, 차등 프라이버시(DP), PII 마스킹
- **Quality Monitoring**: Great Expectations, Soda, 스키마/통계 drift 탐지
- **Schema Registry**: Avro, Protobuf 기반 계약(contract) 관리
- **Access Control & Lineage**: IAM, Data Catalog, 감사 로그

---

## ✅ AI-Ready 체크리스트

| 조건 | 설명 | 검증 방법 |
|---|---|---|
| **일관성 (Consistency)** | 모든 데이터의 형식·단위·스키마가 통일 | 스키마 검증, 단위 통일 테스트 |
| **품질 (Quality)** | 결측·이상·중복·노이즈 제거 완료 | GE/Soda 등 데이터 품질 룰 통과 |
| **접근성 (Accessibility)** | API/SQL/Feature Store로 즉시 호출 가능 | 카탈로그 등록, 권한 부여 |
| **윤리·보안 (Privacy)** | 비식별화·가명처리 완비 | 개인정보 영향평가(PIA), DPIA |
| **재현성 (Reproducible)** | 데이터·코드·모델 버전 고정 | DVC/MLflow 태깅, lineage 추적 |

---

## 🔁 핵심 포인트

1. **5단계는 순차적이지만, 거버넌스는 횡단(cross-cutting)** — 모든 단계에 동시에 적용됩니다.
2. **피드백 루프가 진짜 파이프라인** — 운영 중 drift 감지 → 정제·수집 단계로 되돌아가는 폐쇄 루프가 핵심.
3. **Feature Store가 학습-서빙 일관성의 열쇠** — training-serving skew 방지의 표준 패턴.
4. **AI 프로젝트 비용의 70~80%가 데이터 가공** — 자동화(MLOps)가 ROI를 좌우합니다.
