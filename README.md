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

<pre lang="markdown"> ```mermaid 
erDiagram companies ||--o{ company_names : has companies ||--o{ company_tags : links tags ||--o{ tag_names : has tags ||--o{ company_tags : links companies { int id PK } company_names { int id PK string language string name int company_id FK } tags { int id PK } tag_names { int id PK string language string name int tag_id FK } company_tags { int id PK int company_id FK int tag_id FK } ``` </pre>

## 기술 스택

## 설치 및 실행
