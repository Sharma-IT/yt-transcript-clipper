#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from yt_transcript_clipper.cli import extract_video_id, is_valid_youtube_url, format_transcript


class TestYouTubeTranscriptClipper(unittest.TestCase):
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

    def test_format_transcript(self):
        transcript = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0},
        ]
        self.assertEqual(format_transcript(transcript), "Hello\nWorld")


if __name__ == "__main__":
    unittest.main()