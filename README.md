# 🥧π

django와 django-ninja로 만든 [PEP 691](https://peps.python.org/pep-0691/) json API 기반 pypi 서버.

## Usage

일반적인 django 프로젝트를 실행하는 방법과 같습니다.

여기서는 [granian](https://github.com/emmett-framework/granian)을 기본 웹 서버로 사용하도록 설정되어있습니다.

```sh
granian --interface wsgi --host 0.0.0.0 --port 8182 piepi.wsgi_docker:application
```

## requirements

[pip >= 23.2](https://pip.pypa.io/en/stable/news/#v23-2) (설치하는 쪽에서 필요)

## environment variables

설정가능한 환경변수 목록

```
LANGUAGE_CODE
TIME_ZONE
SECRET_KEY (주어지지 않으면 생성해서 사용함)
MEDIA_ROOT (파이썬 패키지 파일의 위치)

ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS (https://github.com/adamchainz/django-cors-headers)
CORS_URLS_REGEX
CORS_ORIGIN_ALLOW_ALL
CSRF_TRUSTED_ORIGINS

DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_PASSWORD
```

superuser의 아이디와 암호는 주어지지 않으면 기본값 `admin`이 사용됩니다.
