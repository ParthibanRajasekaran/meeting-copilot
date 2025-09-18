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

# Wrap as FunctionTool
summarise_tool = FunctionTool(summarise_meeting)

def build_agent(model_id: str) -> Agent:
    """
    Factory function to build Agent with the summarise tool.
    """
    agent = Agent(
        name="MeetingSummarizer",
        description="An agent that summarizes meeting transcripts",
        model=model_id,
        tools=[summarise_tool],
        instruction="You are a helpful assistant that summarizes meeting transcripts. Use the summarise_meeting tool to analyze transcripts and extract key information."
    )
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
    try:
        with open(args.transcript_file, 'r') as f:
            transcript = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.transcript_file}' not found.")
        exit(1)

    # Build agent
    agent = build_agent("gemini-1.5-flash")

    # Invoke agent with prompt
    prompt = f"Please summarize this meeting transcript using the summarise_meeting tool: {transcript}"
    
    try:
        # Use run_live for synchronous execution - it returns an async generator
        result_generator = agent.run_live(prompt)
        
        # Collect all responses from the generator
        import asyncio
        async def get_results():
            results = []
            async for response in result_generator:
                results.append(str(response))
            return results
        
        # Run the async generator
        responses = asyncio.run(get_results())
        print("Agent Response:")
        for response in responses:
            print(response)
            
    except Exception as e:
        print(f"Error running agent: {e}")
        
        # Fallback: run the summarization directly
        print("\nFalling back to direct summarization:")
        summary = summarise_transcript(transcript)
        print("Meeting Summary:")
        print(f"Summary: {summary.summary}")
        print(f"Decisions: {summary.decisions}")
        print(f"Action Items: {summary.action_items}")
        print(f"Owners: {summary.owners}")
        print(f"Risks: {summary.risks}")