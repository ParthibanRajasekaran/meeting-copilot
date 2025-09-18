from dataclasses import dataclass
from typing import List
from google.adk import LlmAgent, FunctionTool
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
        elif 'will' in line.lower():
            words = line.split()
            for i, word in enumerate(words):
                if word.lower() == 'will' and i > 0:
                    owners.append(words[i-1])
        elif line.lower().startswith('risk:'):
            risks.append(line[5:].strip())

    return MeetingSummary(
        summary=summary,
        decisions=decisions,
        action_items=action_items,
        owners=owners,
        risks=risks
    )

def summarise_meeting(transcript: str) -> MeetingSummary:
    """
    Function to be wrapped as ADK FunctionTool.
    """
    return summarise_transcript(transcript)

# Wrap as FunctionTool
summarise_tool = FunctionTool.from_function(summarise_meeting)

def build_agent(model_id: str) -> LlmAgent:
    """
    Factory function to build LlmAgent with the summarise tool.
    """
    agent = LlmAgent(model_id=model_id, tools=[summarise_tool])
    return agent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a meeting transcript using Google ADK.")
    parser.add_argument("transcript_file", help="Path to the transcript file")
    parser.add_argument("--api-key", help="Google API key (optional if GOOGLE_API_KEY env var is set)")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY") or args.api_key
    if not api_key:
        print("Error: API key is required. Set GOOGLE_API_KEY environment variable or use --api-key option.")
        exit(1)

    # Set the API key in environment
    os.environ["GOOGLE_API_KEY"] = api_key

    # Read transcript
    with open(args.transcript_file, 'r') as f:
        transcript = f.read()

    # Build agent
    agent = build_agent("gemini-1.5-flash")  # Assuming model_id for Gemini

    # Invoke agent with prompt
    prompt = f"Summarize the following meeting transcript: {transcript}"
    result = agent.run(prompt)

    # Assuming result is the MeetingSummary from the tool
    print("Meeting Summary:")
    print(f"Summary: {result.summary}")
    print(f"Decisions: {result.decisions}")
    print(f"Action Items: {result.action_items}")
    print(f"Owners: {result.owners}")
    print(f"Risks: {result.risks}")