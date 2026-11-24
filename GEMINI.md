# MultiTales Gemini Workspace Context

This repository is a Google ADK multi-agent system for generating child-friendly
storybooks. Treat the complete repository as relevant project context.

## Project map

- `main.py`: FastAPI entry point for the Google ADK web or local interface.
- `agents/agent.py`: Defines the root agent and production workflow.
- `agents/writer.py`: Generates story drafts with Gemini.
- `agents/editor.py`: Revises and improves story text.
- `agents/reviewers.py`: Runs positive and negative review agents in parallel.
- `agents/language_detector.py`: Detects the requested story language.
- `agents/image_creator.py`: Generates illustrations and assembles the PDF.
- `agents/tools/playcard.py`: Supplies random story elements.
- `README.md`: Project overview, setup, deployment, and demo information.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Container build and deployment configuration.

## Architecture

The runtime is organized as Google ADK agents:

1. `LanguageDetectorAgent` determines the output language.
2. `BookProductionLoop` runs the writer, editor, and reviewer workflow up to
   three iterations.
3. Positive and negative reviewers run in parallel.
4. `ImageCreatorAgent` generates illustrations and the final storybook PDF.

Preserve this separation when making changes. Shared state should use the
existing agent state keys and callback patterns rather than introducing a
separate state store.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `agents/.env` or configure environment variables:

- `GOOGLE_API_KEY` for API-key authentication.
- `GOOGLE_GENAI_USE_VERTEXAI=False` for Gemini API usage.
- `GOOGLE_GENAI_USE_VERTEXAI=True`, `GOOGLE_CLOUD_PROJECT`, and
  `GOOGLE_CLOUD_LOCATION=global` for Vertex AI usage.

Run locally with:

```powershell
adk run multitales_main
adk web
```

## Gemini usage

- The agent currently uses Gemini 2.5 and Gemini 2.0 Flash model variants.
- Use explicit, age-appropriate, child-safety-focused instructions in prompts.
- Keep structured JSON outputs parseable and validate agent callbacks.
- Do not expose API keys or credentials in source, tests, logs, or examples.
- Do not replace the Gemini integration without a repository-specific request.

## Working conventions

- Use Python and follow the existing Google ADK style.
- Keep changes focused and preserve the sequential/parallel/loop orchestration.
- Update `README.md` when setup, architecture, model names, or public behavior
  changes.
- Add or update focused tests when the repository gains a test suite.
- Never add generated PDFs, databases, virtual environments, API keys, or
  cached model output to source control.
