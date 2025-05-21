#!/usr/bin/env python3

import unittest
import requests
from unittest.mock import patch, MagicMock
from yt_transcript_clipper.cli import extract_video_id, is_valid_youtube_url, format_transcript, clip
from typer.testing import CliRunner
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound


class TestYouTubeTranscriptClipper(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    # URL extraction tests
    def test_extract_video_id_standard_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_extract_video_id_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_extract_video_id_embed_url(self):
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_extract_video_id_shorts_url(self):
        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_extract_video_id_invalid_url(self):
        url = "https://example.com/video"
        self.assertIsNone(extract_video_id(url))

    def test_extract_video_id_malformed_url(self):
        urls = [
            "",  # Empty URL
            "not a url",  # Plain text
            "https://youtube.com",  # No video ID
            "https://www.youtube.com/watch",  # Incomplete URL
            "https://www.youtube.com/watch?q=test"  # Wrong parameter
        ]
        for url in urls:
            self.assertIsNone(extract_video_id(url))

    # URL validation tests
    @patch('requests.get')
    def test_is_valid_youtube_url_valid(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertTrue(is_valid_youtube_url(url))

    @patch('requests.get')
    def test_is_valid_youtube_url_invalid(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        url = "https://www.youtube.com/watch?v=invalid_id"
        self.assertFalse(is_valid_youtube_url(url))

    @patch('requests.get')
    def test_is_valid_youtube_url_request_error(self, mock_get):
        mock_get.side_effect = requests.RequestException()
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertFalse(is_valid_youtube_url(url))

    # Transcript formatting tests
    def test_format_transcript_empty(self):
        transcript = []
        self.assertEqual(format_transcript(transcript), "")

    def test_format_transcript_single_entry(self):
        transcript = [{"text": "Hello", "start": 0.0, "duration": 1.0}]
        self.assertEqual(format_transcript(transcript), "Hello")

    def test_format_transcript_multiple_entries(self):
        transcript = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0},
        ]
        self.assertEqual(format_transcript(transcript), "Hello\nWorld")

    def test_format_transcript_with_special_chars(self):
        transcript = [
            {"text": "Line 1!", "start": 0.0, "duration": 1.0},
            {"text": "Line 2?", "start": 1.0, "duration": 1.0},
            {"text": "Line 3...", "start": 2.0, "duration": 1.0},
        ]
        self.assertEqual(format_transcript(transcript), "Line 1!\nLine 2?\nLine 3...")

    # CLI tests
    @patch('yt_transcript_clipper.cli.is_valid_youtube_url')
    @patch('yt_transcript_clipper.cli.get_transcript')
    @patch('pyperclip.copy')
    def test_cli_successful_execution(self, mock_copy, mock_get_transcript, mock_is_valid):
        mock_is_valid.return_value = True
        mock_get_transcript.return_value = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0}
        ]
        
        with patch('yt_transcript_clipper.cli.app') as mock_app:
            mock_app.return_value = "Hello\nWorld"
            result = clip("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            self.assertEqual(result, "Hello\nWorld")
            mock_copy.assert_called_once_with("Hello\nWorld")

    @patch('yt_transcript_clipper.cli.is_valid_youtube_url')
    def test_cli_invalid_url(self, mock_is_valid):
        mock_is_valid.return_value = False
        with self.assertRaises(SystemExit):
            clip("https://invalid-url.com")


if __name__ == "__main__":
    unittest.main()