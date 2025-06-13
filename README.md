# childbook-adk

## Run project
[uv](https://github.com/astral-sh/uv) is recommended.

Install dependencies:
```sh
uv sync
```

Create a `.env` file based on `.env.example`. Modify the `GOOGLE_CLOUD_PROJECT` to your project name.

Run adk:
```sh
uv run adk web
```