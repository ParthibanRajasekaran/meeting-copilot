# Meeting Copilot

A real-time meeting summarization agent built using Google's Agent Development Kit (ADK).

Copyright 2025. Licensed under the Apache License, Version 2.0.

## ⚠️ Security Notice

**IMPORTANT:** This project requires a Google API key for operation. For security reasons:

- **NEVER** hard-code API keys in source code
- **NEVER** commit API keys to version control
- **NEVER** share API keys in any form
- Only pass API keys via command line arguments or environment variables
- The `.gitignore` file is configured to prevent accidental commits of secrets

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

4. (Optional) Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API key (remember: .env is gitignored)
   ```

## API Key Setup

To use this agent, you need a Google Gemini API key.

1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/) or [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai).

2. **Secure Methods to Provide the API Key:**

   **Option A: Environment Variable (Recommended)**
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   python -m meeting_copilot.agent transcript.txt
   ```

   **Option B: Command Line Argument**
   ```bash
   python -m meeting_copilot.agent transcript.txt --api-key "your-api-key-here"
   ```

### 🚨 Security Best Practices

- **Never** store API keys in files that could be committed to version control
- **Never** hard-code API keys in source code
- **Never** share API keys in emails, chat, or documentation
- Use environment variables for production deployments
- Rotate API keys regularly
- Monitor API key usage for unauthorized access

The project includes a `.env.example` file to show required environment variables, but **never** commit actual `.env` files containing real API keys.

The project is configured to prevent accidental commits of API keys through the `.gitignore` file.

## Usage

### Interactive NLP Mode (Recommended)

For the best experience, use the interactive NLP mode where you can ask questions about meetings in natural language:

```bash
python -m meeting_copilot.agent --interactive
```

**Interactive Mode Features:**
- Load transcript files dynamically
- Ask questions in natural language
- Get specific information (decisions, action items, owners, risks)
- Conversational AI-powered responses

**Example Interactive Session:**
```
🤖 Meeting Copilot - Interactive Mode
==================================================
You can now ask questions about meetings in natural language!
Commands:
  /load <file>  - Load a transcript file
  /quit         - Exit interactive mode
  /help         - Show this help

You: /load sample_transcript.txt
✅ Loaded transcript from sample_transcript.txt

You: What decisions were made in this meeting?
🤔 Thinking...

🤖 Meeting Copilot: Based on the meeting transcript, the following decisions were made:
• We will extend the deadline by two weeks.

You: Who is responsible for updating the documentation?
🤔 Thinking...

🤖 Meeting Copilot: Sarah is responsible for updating the documentation according to the action items.

You: /quit
Goodbye! 👋
```

### Command Line File Processing

Run the agent on a specific transcript file:

```bash
python -m meeting_copilot.agent path/to/transcript.txt
```

Or with API key option:

```bash
python -m meeting_copilot.agent path/to/transcript.txt --api-key "your-api-key-here"
```

The agent will process the transcript and print a structured summary including decisions, action items, owners, and risks.

**Example:**

```bash
python -m meeting_copilot.agent sample_transcript.txt --api-key "your-key"
```

Output:
```
Meeting Summary:
Summary: Overall summary of the meeting based on transcript.
Decisions: ['We will extend the deadline by two weeks.']
Action Items: ['Sarah will update the documentation.']
Owners: ['Alice']
Risks: ['There might be budget overruns.']
```

**Note:** The system includes intelligent fallback functionality. If the ADK agent encounters issues, it will automatically fall back to direct heuristic processing to ensure you always get results.

## 🧪 Testing & CI/CD

### **Cost-Optimized Testing Strategy**

The project uses a **dual-workflow approach** to balance development velocity with cost control:

#### **1. Daily CI Workflow** (FREE - Runs on every push/PR)
- **Trigger**: Push to main, pull requests
- **Cost**: $0.00 (heuristic processing only)
- **Purpose**: Fast feedback, code quality, no API usage
- **Coverage**: Unit tests, integration tests

#### **2. Monthly Comprehensive Workflow** (Optional - Minimal cost)
- **Trigger**: 1st of every month (scheduled) OR manual
- **Cost**: Minimal (free tier covers)
- **Purpose**: Full AI agent validation
- **Coverage**: AI functionality, performance tests

#### **3. Manual Comprehensive Workflow** (On-demand)
- **Trigger**: Manual from GitHub UI
- **Cost**: Controlled by user
- **Purpose**: Custom testing scenarios
- **Options**: Full test, AI-only, or performance tests

### **Running Tests**

#### **Local Testing** (Free)
```bash
# Run all tests locally (no API costs)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=meeting_copilot
```

#### **Manual Comprehensive Testing** (Controlled cost)
1. Go to **GitHub → Actions → Manual Comprehensive Test**
2. Click **"Run workflow"**
3. Select test type: `full`, `ai-only`, or `performance`
4. Click **"Run workflow"**

### **Cost Analysis**

| Workflow | Frequency | API Usage | Monthly Cost |
|----------|-----------|-----------|--------------|
| **Daily CI** | Every push/PR | None | **$0.00** |
| **Monthly Comprehensive** | 1st of month | Minimal | **$0.00** (free tier) |
| **Manual Comprehensive** | As needed | Variable | **User controlled** |

### **Why This Approach?**

✅ **Development stays fast** - No waiting for AI API calls during development
✅ **Costs are controlled** - AI usage only when explicitly requested  
✅ **Quality is maintained** - Comprehensive testing available when needed
✅ **Free tier optimized** - Minimal API usage stays within free limits

## Features

- **🤖 Interactive NLP Chat**: Ask questions about meetings in natural language using AI
- **🔍 Intelligent Analysis**: Extracts decisions, action items, owners, and risks using AI-powered analysis
- **🛠️ Multiple Tools**: Specialized tools for different types of queries (decisions, owners, risks, etc.)
- **📁 Dynamic File Loading**: Load and analyze different transcripts during interactive sessions
- **⚡ Direct Processing**: Reliable fallback using heuristic analysis
- **💻 CLI Interface**: Easy-to-use command line interface with multiple modes
- **🛡️ Error Handling**: Comprehensive error handling and user-friendly messages
- **🎯 Pattern Recognition**: Identifies meeting elements using advanced pattern matching:
  - Decisions: Lines starting with "Decision:" or AI-identified decisions
  - Action Items: Lines starting with "Action:" or AI-identified tasks
  - Owners: Names appearing before "will" or AI-identified responsible parties
  - Risks: Lines starting with "Risk:" or AI-identified concerns

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

```
Copyright 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```