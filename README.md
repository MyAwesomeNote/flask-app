[English](./README_en.md)

## 소개

이 프로젝트는 웹 애플리케이션의 기본적인 기능 및 페이지를 구현하는 예제로, Flask에서 자주 사용되는 Model-View-Controller (MVC) 패턴과 CRUD (Create, Read, Update,
Delete) 패턴의 사용법을 보여줍니다.
이 저장소에 포함된 코드는 이 패턴들을 이해하는 데 개발자들에게 큰 도움이 될 것입니다.
MVC 패턴은 애플리케이션을 Model, View, Controller 세 가지 컴포넌트로 분리하는 소프트웨어 디자인 패턴으로, 이 구조는 코드 재사용성과 유지 보수성을 향상시킵니다.

- Model은 애플리케이션의 정보(데이터)를 대표하고 처리합니다.
- View는 사용자에게 보여지는 사용자 인터페이스(UI)를 담당합니다.
- Controller는 사용자 입력을 처리하고 Model과 View 사이의 상호 작용을 조정합니다.

CRUD는 데이터 지속성에서 가장 기본적F인 네 가지 작업인 Create(생성), Read(읽기), Update(수정), Delete(삭제)를 나타냅니다.
이러한 작업들은 모든 웹 애플리케이션에서 일반적으로 필요한 기능입니다.

## 시작하기

### 종속성 설치

다음 명령으로 종속성을 설치합니다:

```bash
pip install -r requirements.txt
```

#### 최초 실행시

앱을 처음 실행할 때는, DB를 위해 초기화, 마이그레이션, 업그레이드를 해야 합니다. 여기서는 flask-sqlalchemy, flask-migrate 그리고 flask-wtf를 사용합니다

```bash
flask db init
flask db migrate
flask db upgrade
```

Windows의 경우 터미널에 `init`을 입력하세요.

### 앱 실행

한번 이상 초기화 스크립트(또는 최초 실행 명령)을 실행했다면 다음 명령으로 앱을 실행할 수 있습니다 (또는 `run`):

```bash
flask run
```

### 엔드포인트

- 🤷 `/`
    - 📪 `/contact`
        - `/contact/us` - Contact us
        - `/contact/complete` - Contact us form을 보내면 이 페이지로 리다이렉션됩니다.
        - `/contact/<id>` - 사용자(id)에게 Hello, 메인 페이지로 사용될 예정입니다.
    - 🔐 `/auth` - 인증
        - `/auth/signup` - 회원가입
        - `/auth/signin` - 로그인
        - Redirects
            - `/auth/register` -> `/auth/signup`
            - `/auth/login` -> `/auth/signin`
    - 🗂️ `/crud`
        - `/crud/users` - 모든 사용자 보기 및 편집
        - `/crud/register` - 새 사용자를 직접 등록
        - `/crud/<id>` - 사용자 편집
        - `/crud/<id>/delete` - 사용자 삭제

### 🗝️ 로그인은 어떻게 작동하나요?

회원가입을 하면 비밀번호는 해시화되어 데이터베이스에 저장됩니다.
로그인 시, 해시화된 비밀번호는 데이터베이스에 있는 비밀번호와 비교됩니다.
로그인이 되어야만 `/auth` 엔드포인트에 접근할 수 있습니다.

### 📚 라이브러리

- 🗃️ SQL ㅣ DataBase
    - Flask SQLAlchemy > SQLAlchemy 사용을 간소화하며 강력한 ORM 제공
    - Flask Migrate > SQLAlchemy 데이터베이스 마이그레이션 처리
- 🔐 인증
    - Flask WTF > Flask와 WTForms 통합, CSRF 포함
    - Flask Login > 사용자 세션 관리 처리