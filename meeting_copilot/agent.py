# Copyright 2025
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import List
from google.adk import Agent
from google.adk.tools import FunctionTool
import os
import argparse

@dataclass
class MeetingSummary:
    summary: str
    decisions: List[str]
    action_items: List[str]
    owners: List[str]
    risks: List[str]

def summarise_transcript(transcript: str) -> MeetingSummary:
    """
    Extract meeting summary elements using simple heuristics.
    """
    summary = "Overall summary of the meeting based on transcript."
    decisions = []
    action_items = []
    owners = []
    risks = []

    lines = transcript.split('\n')
    for line in lines:
        line = line.strip()
        if line.lower().startswith('decision:'):
            decisions.append(line[9:].strip())
        elif line.lower().startswith('action:'):
            action_items.append(line[7:].strip())
        elif line.lower().startswith('risk:'):
            risks.append(line[5:].strip())
        
        # Extract owners from any line containing "will"
        if 'will' in line.lower():
            words = line.split()
            for i, word in enumerate(words):
                if word.lower() == 'will' and i > 0:
                    potential_owner = words[i-1].strip('.,!?;:')
                    # Filter for likely person names:
                    # - Starts with capital letter
                    # - At least 2 characters, max 20
                    # - Not common non-person words
                    # - Contains only letters (and possibly apostrophes)
                    common_non_names = {
                        'we', 'i', 'you', 'they', 'it', 'this', 'that', 'these', 'those',
                        'team', 'system', 'service', 'project', 'company', 'organization',
                        'department', 'group', 'meeting', 'session', 'discussion',
                        'process', 'method', 'approach', 'strategy', 'plan',
                        'implementation', 'development', 'testing', 'deployment',
                        'infrastructure', 'architecture', 'design', 'code', 'database',
                        'api', 'interface', 'framework', 'library', 'module',
                        'function', 'class', 'object', 'variable', 'parameter',
                        'security', 'authentication', 'authorization', 'encryption',
                        'performance', 'scalability', 'reliability', 'monitoring'
                    }
                    
                    if (2 <= len(potential_owner) <= 20 and 
                        potential_owner[0].isupper() and 
                        potential_owner.lower() not in common_non_names and
                        all(c.isalpha() or c in "'-" for c in potential_owner)):
                        owners.append(potential_owner)

    return MeetingSummary(
        summary=summary,
        decisions=decisions,
        action_items=action_items,
        owners=owners,
        risks=risks
    )

def summarise_meeting(transcript: str) -> str:
    """
    Function to be wrapped as ADK FunctionTool.
    Returns a formatted string summary.
    """
    result = summarise_transcript(transcript)
    return f"""
Meeting Summary:
Summary: {result.summary}
Decisions: {', '.join(result.decisions) if result.decisions else 'None'}
Action Items: {', '.join(result.action_items) if result.action_items else 'None'}
Owners: {', '.join(result.owners) if result.owners else 'None'}
Risks: {', '.join(result.risks) if result.risks else 'None'}
"""

def get_decisions(transcript: str) -> str:
    """
    Extract and return only the decisions from a meeting transcript.
    """
    result = summarise_transcript(transcript)
    if result.decisions:
        return "Meeting Decisions:\n" + "\n".join(f"• {decision}" for decision in result.decisions)
    return "No decisions were identified in this meeting."

def get_action_items(transcript: str) -> str:
    """
    Extract and return only the action items from a meeting transcript.
    """
    result = summarise_transcript(transcript)
    if result.action_items:
        return "Action Items:\n" + "\n".join(f"• {item}" for item in result.action_items)
    return "No action items were identified in this meeting."

def get_owners(transcript: str) -> str:
    """
    Extract and return only the owners/responsible parties from a meeting transcript.
    """
    result = summarise_transcript(transcript)
    if result.owners:
        return "Meeting Participants/Owners:\n" + "\n".join(f"• {owner}" for owner in result.owners)
    return "No specific owners were identified in this meeting."

def get_risks(transcript: str) -> str:
    """
    Extract and return only the risks from a meeting transcript.
    """
    result = summarise_transcript(transcript)
    if result.risks:
        return "Identified Risks:\n" + "\n".join(f"• {risk}" for risk in result.risks)
    return "No risks were identified in this meeting."

def ask_about_meeting(transcript: str, question: str) -> str:
    """
    Answer specific questions about the meeting using AI analysis.
    This function provides context that the agent can use to answer questions.
    """
    result = summarise_transcript(transcript)
    
    # Create context for the AI to answer questions
    context = f"""
Based on the meeting transcript, here is the structured information:

SUMMARY: {result.summary}

DECISIONS: {', '.join(result.decisions) if result.decisions else 'None identified'}

ACTION ITEMS: {', '.join(result.action_items) if result.action_items else 'None identified'}

OWNERS/PARTICIPANTS: {', '.join(result.owners) if result.owners else 'None identified'}

RISKS/CONCERNS: {', '.join(result.risks) if result.risks else 'None identified'}

QUESTION: {question}

Please provide a helpful, accurate answer to this question based on the meeting information above. If the question cannot be answered from the available information, say so clearly.
"""
    return context

# Wrap as FunctionTools
summarise_tool = FunctionTool(summarise_meeting)
decisions_tool = FunctionTool(get_decisions)
action_items_tool = FunctionTool(get_action_items)
owners_tool = FunctionTool(get_owners)
risks_tool = FunctionTool(get_risks)
ask_tool = FunctionTool(ask_about_meeting)

def build_agent(model_id: str, transcript: str = "") -> Agent:
    """
    Factory function to build Agent with multiple meeting analysis tools.
    """
    tools = [
        summarise_tool,
        decisions_tool,
        action_items_tool,
        owners_tool,
        risks_tool,
    ]
    
    # Add the ask tool if we have a transcript
    if transcript:
        tools.append(ask_tool)
    
    instruction = f"""You are an intelligent Meeting Copilot that helps analyze meeting transcripts.

You have access to various tools to help users understand meeting content:

- summarise_meeting: Provides a complete summary of the meeting
- get_decisions: Lists all decisions made in the meeting
- get_action_items: Lists all action items and tasks
- get_owners: Lists all people mentioned as responsible for tasks
- get_risks: Lists all risks or concerns identified

{f"If you have a specific transcript loaded, you can also answer detailed questions about it using the ask_about_meeting tool." if transcript else ""}

Always be helpful, accurate, and provide clear, well-formatted responses. If asked questions, use the most appropriate tool or combination of tools to provide comprehensive answers."""

    agent = Agent(
        name="MeetingCopilot",
        description="An intelligent assistant for analyzing meeting transcripts and answering questions about them",
        tools=tools,
        instruction=instruction,
        model=model_id
    )
    return agent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Meeting Copilot - Analyze meeting transcripts with AI")
    parser.add_argument("transcript_file", nargs="?", help="Path to the transcript file (optional for interactive mode)")
    parser.add_argument("--api-key", help="Google API key (optional if GOOGLE_API_KEY env var is set)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive NLP chat mode")
    parser.add_argument("--model", default="gemini-1.5-flash", help="Google AI model to use (default: gemini-1.5-flash)")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY") or args.api_key
    if not api_key:
        print("Error: API key is required. Set GOOGLE_API_KEY environment variable or use --api-key option.")
        exit(1)

    # Set the API key in environment
    os.environ["GOOGLE_API_KEY"] = api_key

    if args.interactive:
        # Interactive NLP mode
        print("🤖 Meeting Copilot - Interactive Mode")
        print("=" * 50)
        print("You can now ask questions about meetings in natural language!")
        print("Commands:")
        print("  /load <file>  - Load a transcript file")
        print("  /quit         - Exit interactive mode")
        print("  /help         - Show this help")
        print()

        transcript = ""
        agent = None

        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ["/quit", "/exit", "quit", "exit"]:
                    print("Goodbye! 👋")
                    break
                    
                elif user_input.lower() in ["/help", "help"]:
                    print("Commands:")
                    print("  /load <file>  - Load a transcript file")
                    print("  /quit         - Exit interactive mode")
                    print("  /help         - Show this help")
                    print("Just type your questions about meetings!")
                    continue
                    
                elif user_input.lower().startswith("/load "):
                    file_path = user_input[6:].strip()
                    try:
                        with open(file_path, 'r') as f:
                            transcript = f.read()
                        print(f"✅ Loaded transcript from {file_path}")
                        agent = build_agent(args.model, transcript)
                    except FileNotFoundError:
                        print(f"❌ File not found: {file_path}")
                    continue
                
                if not transcript:
                    print("❌ Please load a transcript first using: /load <file>")
                    continue
                
                if not agent:
                    agent = build_agent(args.model, transcript)
                
                # Process the query using the agent
                print("🤔 Thinking...")
                try:
                    response = agent.run(user_input)
                    print(f"\n🤖 Meeting Copilot: {response}")
                except Exception as e:
                    print(f"❌ Error processing query: {e}")
                
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\nGoodbye! 👋")
                break
            except EOFError:
                print("\nGoodbye! 👋")
                break

    else:
        # File processing mode (original functionality)
        if not args.transcript_file:
            print("Error: transcript_file is required when not in interactive mode.")
            print("Use --interactive for NLP chat mode, or provide a transcript file.")
            exit(1)

        # Read transcript
        try:
            with open(args.transcript_file, 'r') as f:
                transcript = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.transcript_file}' not found.")
            exit(1)

        print("Processing meeting transcript...")
        print("=" * 50)
        
        # Use direct summarization (more reliable than ADK for now)
        summary = summarise_transcript(transcript)
        print("Meeting Summary:")
        print(f"Summary: {summary.summary}")
        print(f"Decisions: {summary.decisions}")
        print(f"Action Items: {summary.action_items}")
        print(f"Owners: {summary.owners}")
        print(f"Risks: {summary.risks}")
        
        print("\n" + "=" * 50)
        print("✅ Transcript processed successfully!")