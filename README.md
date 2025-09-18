# Meeting Copilot

A real-time meeting summarization agent built using Google's Agent Development Kit (ADK).

## Installation

1. Clone or download this repository.

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## API Key Setup

To use this agent, you need a Google Gemini API key.

1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/) or [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai).

2. Set the API key as an environment variable:
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   ```
   Or pass it via the `--api-key` CLI option.

**Important:** Do not hard-code or store the API key in the repository.

## Usage

### Command Line

Run the agent locally from the command line:

```bash
python -m meeting_copilot.agent path/to/transcript.txt
```

Or with API key option:

```bash
python -m meeting_copilot.agent path/to/transcript.txt --api-key "your-api-key-here"
```

The agent will process the transcript and print a structured summary including decisions, action items, owners, and risks.

### ADK Dev UI

You can also run the agent via the ADK development UI for interactive testing.

1. Ensure ADK is set up.
2. Load the agent and provide a transcript prompt.

## Project Structure

- `meeting_copilot/agent.py`: Main agent implementation with summarization logic.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Excludes cache, environment files, and virtual environments.

## License

[Add license if applicable]