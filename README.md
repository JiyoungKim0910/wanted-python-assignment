# wanted-python-assignment

FastAPI 기반의 다국어 회사/태그 검색 REST API 입니다.

## 주요 기능

-   회사명 자동 완성
-   회사 이름으로 회사 검색
-   태그명으로 회사 검색
-   다국어 검색 가능
-   회사 태그 정보 추가
-   회사 태그 정보 삭제

## ERD

<pre lang="markdown"> ```text
[companies]

-   id (PK)

          │
          └────────────┐
                       ▼

[company_names]

-   id (PK)
-   language (string)
-   name (string)
-   company_id (FK → companies.id)

            ▲
            │
            │

    [company_tags] (중간 테이블)

-   id (PK)
-   company_id (FK → companies.id)
-   tag_id (FK → tags.id)
    │
    ▼

[tags]

-   id (PK)

          │
          └────────────┐
                       ▼

[tag_names]

-   id (PK)
-   language (string)
-   name (string)
-   tag_id (FK → tags.id)
```
</pre>

## 기술 스택

## 설치 및 실행
