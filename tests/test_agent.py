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

import pytest
from meeting_copilot.agent import MeetingSummary, summarise_transcript, summarise_meeting


class TestMeetingSummary:
    """Test the MeetingSummary dataclass"""

    def test_meeting_summary_creation(self):
        """Test creating a MeetingSummary instance"""
        summary = MeetingSummary(
            summary="Test summary",
            decisions=["Decision 1", "Decision 2"],
            action_items=["Action 1", "Action 2"],
            owners=["Alice", "Bob"],
            risks=["Risk 1", "Risk 2"]
        )

        assert summary.summary == "Test summary"
        assert summary.decisions == ["Decision 1", "Decision 2"]
        assert summary.action_items == ["Action 1", "Action 2"]
        assert summary.owners == ["Alice", "Bob"]
        assert summary.risks == ["Risk 1", "Risk 2"]


class TestSummariseTranscript:
    """Test the summarise_transcript function"""

    def test_empty_transcript(self):
        """Test summarization of empty transcript"""
        result = summarise_transcript("")

        assert result.summary == "Overall summary of the meeting based on transcript."
        assert result.decisions == []
        assert result.action_items == []
        assert result.owners == []
        assert result.risks == []

    def test_transcript_with_decisions(self):
        """Test extraction of decisions from transcript"""
        transcript = """
        Decision: We will implement the new feature
        Decision: The deadline is next Friday
        Some other discussion about the project
        """

        result = summarise_transcript(transcript)

        assert "We will implement the new feature" in result.decisions
        assert "The deadline is next Friday" in result.decisions

    def test_transcript_with_action_items(self):
        """Test extraction of action items from transcript"""
        transcript = """
        Action: John will update the documentation
        Action: Sarah will review the code
        Regular meeting discussion continues
        """

        result = summarise_transcript(transcript)

        assert "John will update the documentation" in result.action_items
        assert "Sarah will review the code" in result.action_items

    def test_transcript_with_owners(self):
        """Test extraction of owners from transcript"""
        transcript = """
        John will handle the deployment
        Sarah will coordinate with the team
        The system will be updated next week
        We will implement the changes
        """

        result = summarise_transcript(transcript)

        assert "John" in result.owners
        assert "Sarah" in result.owners
        # Should not include "system" or "we" as owners
        assert "system" not in result.owners
        assert "we" not in result.owners

    def test_transcript_with_risks(self):
        """Test extraction of risks from transcript"""
        transcript = """
        Risk: The deadline might be missed
        Risk: There could be integration issues
        Discussion about project timeline
        """

        result = summarise_transcript(transcript)

        assert "The deadline might be missed" in result.risks
        assert "There could be integration issues" in result.risks

    def test_complex_transcript(self):
        """Test with a more complex transcript"""
        transcript = """
        Meeting started at 10 AM.

        Decision: We will use Python for the backend
        Action: Mike will set up the development environment
        Risk: The third-party API might have rate limits

        Sarah will lead the frontend development
        John will handle database design

        Decision: Deployment will be on AWS
        Action: Team will review security requirements

        The project timeline looks good.
        """

        result = summarise_transcript(transcript)

        # Check decisions
        assert "We will use Python for the backend" in result.decisions
        assert "Deployment will be on AWS" in result.decisions

        # Check action items
        assert "Mike will set up the development environment" in result.action_items
        assert "Team will review security requirements" in result.action_items

        # Check owners
        assert "Sarah" in result.owners
        assert "John" in result.owners
        assert "Mike" in result.owners

        # Check risks
        assert "The third-party API might have rate limits" in result.risks

    def test_owner_filtering(self):
        """Test that owner extraction properly filters out non-names"""
        transcript = """
        The team will handle this
        We will implement the feature
        This will be done by the system
        Project will be completed on time
        Alice will review the code
        Bob will test the functionality
        """

        result = summarise_transcript(transcript)

        # Should only include actual names
        assert "Alice" in result.owners
        assert "Bob" in result.owners

        # Should not include these common non-names
        non_names = ["team", "we", "system", "project"]
        for non_name in non_names:
            assert non_name not in result.owners


class TestSummariseMeeting:
    """Test the summarise_meeting function"""

    def test_summarise_meeting_formatting(self):
        """Test that summarise_meeting returns properly formatted string"""
        transcript = """
        Decision: Test decision
        Action: Test action
        Alice will handle this
        Risk: Test risk
        """

        result = summarise_meeting(transcript)

        assert "Meeting Summary:" in result
        assert "Summary:" in result
        assert "Decisions: Test decision" in result
        assert "Action Items: Test action" in result
        assert "Owners: Alice" in result
        assert "Risks: Test risk" in result

    def test_summarise_meeting_empty_fields(self):
        """Test formatting when some fields are empty"""
        transcript = "Just a regular discussion with no specific items"

        result = summarise_meeting(transcript)

        assert "Decisions: None" in result
        assert "Action Items: None" in result
        assert "Owners: None" in result
        assert "Risks: None" in result


class TestTranscriptFiles:
    """Test with actual transcript files"""

    def test_sample_transcript_file(self):
        """Test processing of sample transcript file"""
        # Read the sample transcript
        with open("sample_transcript.txt", "r") as f:
            transcript = f.read()

        result = summarise_transcript(transcript)

        # Should extract some information from the sample
        assert isinstance(result, MeetingSummary)
        assert result.summary == "Overall summary of the meeting based on transcript."

    def test_realistic_transcript_file(self):
        """Test processing of realistic transcript file"""
        # Read the realistic transcript
        with open("realistic_transcript.txt", "r") as f:
            transcript = f.read()

        result = summarise_transcript(transcript)

        # Should extract some information from the realistic transcript
        assert isinstance(result, MeetingSummary)
        assert result.summary == "Overall summary of the meeting based on transcript."