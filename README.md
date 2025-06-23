# 🌈 MultiTales: AI-Driven Multi-Agent Children's Story Generation System

## 🧸 Project Overview

MultiTales is a collaborative multi-agent system built with Google Cloud's Agent Development Kit (ADK), designed to automate the children's story creation workflow. By simulating roles in the traditional publishing process—including writer, editor, reviewers, reader, and illustrator—it forms a fully closed-loop pipeline from initial story generation to illustration and final PDF output.

This project addresses key challenges in children's book production: long creation cycles, the need for multi-role collaboration, and constraints around creativity, safety, and emotional appropriateness. Through a structured, modular agent workflow, MultiTales showcases the power of ADK in creative content generation.

## 🧩 Hackathon Category & Goal

- **Category**: Content Creation and Generation
- **Goal**: Build a smart, traceable, end-to-end multi-agent system that automates story writing, reviewing, visual enhancement, and book publishing.

## 🧠 Agent Roles

- **Writer Agent**: Generates story drafts using user prompts and random narrative elements.
- **Editor Agent**: Polishes language, adjusts logic, and ensures stylistic and semantic coherence.
- **Reviewer Agent 1**: Acts as a critical reviewer providing suggestions and identifying issues.
- **Reviewer Agent 2**: Plays the general reader, providing scores and praise.
- **ImageCreator Agent**: Translates final text into illustrations and compiles a printable storybook PDF.

## ⚙️ Tech Stack

- **Google ADK**: Multi-agent orchestration framework
- **Workflow Agents**: Uses `SequentialAgent`, `LoopAgent`, `AgentTool`
- **LLM Models**:
  - Gemini 2.5 Pro for writing and editing
  - Gemini 2.0 Flash for reviewing
- **Tooling & Services**:
  - Google Cloud Run
  - Imagen 4 (image generation model)
- **Output Format**: Fully structured in JSON for traceability and visual analysis


## 🚀 How to Run

To run the MultiTales project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/MultiTales/childbook-adk.git
cd childbook-adk
```

### 2. Set Up a Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the root directory or set environment variables manually:

```dotenv
GOOGLE_API_KEY=your_google_api_key
GOOGLE_GENAI_USE_VERTEXAI=False
```

Or, for Vertex AI:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
```

### 5. Run the Agent Locally

```bash
adk run multitales_main
```

Or launch the visual interface:

```bash
adk web
```

Access: `http://localhost:8000`

### 6. (Optional) Deploy to Google Cloud Run

Follow our tutorial:  
👉 [One-click Cloud Run deployment blog](https://dev.to/shvlev9cywkk/one-click-deployment-of-your-multi-agent-system-to-cloud-run-with-google-adk-2l50)


## 🧪 Demo & Results

- 📽️ Demo Video: [https://youtu.be/demo-link](https://youtu.be/demo-link)
- 💻 Repository: [https://github.com/MultiTales/childbook-adk/](https://github.com/MultiTales/childbook-adk/)
- 📚 Each run iterates through 3 story versions with automatic review and refinement
- 📄 Final output: a fully illustrated, child-friendly storybook in PDF format

## 🛠️ Learnings & Challenges

- 🧠 Prompt engineering to ensure agents have clear and non-overlapping roles
- 🔁 Managed session state transitions for multi-round interactions using ADK
- 🪐 Gemini 2.5 Pro required post-processing to correct occasional unstable outputs
- 🎲 A PlayCard tool was integrated to randomly inject characters, settings, and conflicts to boost creativity
- 🔄 Loop control and stopping conditions implemented via ADK callbacks
- 🖼️ Handling asynchronous tool calls and artifact versioning in the image generation flow
- ✅ Striking a balance between automation and quality required careful multi-agent coordination

## ✨ Bonus Contributions

- ✅ Used Imagen 4 to generate visual illustrations
- ✅ Deployed system to Google Cloud Run for live usage
- ✅ Published a blog tutorial for deploying ADK systems to Cloud Run:  
  [Read it here](https://dev.to/shvlev9cywkk/one-click-deployment-of-your-multi-agent-system-to-cloud-run-with-google-adk-2l50)

## 🧑‍💻 Team Members

| Name         | Role                | Key Contributions                                                      |
|--------------|---------------------|------------------------------------------------------------------------|
| Jiahui Bai   | Architecture, DevOps | Multi-agent flow design, orchestration control, Cloud Run deployment   |
| Shumin Liu   | Model Engineering    | Prompt crafting, role specification, Gemini model tuning, architecture improvements |
| Yiyang Huang | Integration & Output | Output structuring, PDF synthesis logic, story-image formatting         |
| Jacky Wang   | Visualization & Media| Demo video production, system diagram design, Imagen integration        |
