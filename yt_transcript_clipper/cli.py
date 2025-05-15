#!/usr/bin/env python3

import sys
import re
from typing import Optional, List, Dict, Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import pyperclip
import requests

app = typer.Typer(help="Extract YouTube video transcripts and copy to the clipboard")
console = Console()


def extract_video_id(url: str) -> Optional[str]:
    """Extract the YouTube video ID from a URL."""
    # Match various YouTube URL formats
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([\w-]+)',  # Standard YouTube URL
        r'(?:https?://)?(?:www\.)?youtu\.be/([\w-]+)',  # Shortened YouTube URL
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([\w-]+)',  # Embedded YouTube URL
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([\w-]+)',  # Old style YouTube URL
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([\w-]+)'  # YouTube Shorts URL
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def is_valid_youtube_url(url: str) -> bool:
    """Check if the given URL is a valid YouTube URL."""
    video_id = extract_video_id(url)
    
    # If we couldn't extract a video ID, it's not a valid YouTube URL
    if not video_id:
        return False
    
    # Verify the video exists by checking the oEmbed endpoint
    try:
        response = requests.get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}")
        return response.status_code == 200
    except requests.RequestException:
        return False


def get_transcript(video_id: str) -> List[Dict[str, Any]]:
    """Get the transcript for a YouTube video."""
    return YouTubeTranscriptApi.get_transcript(video_id)


def format_transcript(transcript: List[Dict[str, Any]]) -> str:
    """Format the transcript into a readable string."""
    return "\n".join([entry["text"] for entry in transcript])


@app.command()
def clip(url: str = typer.Argument(..., help="YouTube video URL to extract transcript from")):
    """Extract transcript from a YouTube video and copy it to the clipboard."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        transient=True,
    ) as progress:
        # Validate URL
        progress.add_task(description="Validating YouTube URL...", total=None)
        if not is_valid_youtube_url(url):
            console.print(Panel("[bold red]Error: Invalid YouTube URL[/bold red]\n\nPlease provide a valid YouTube video URL.", 
                               title="Invalid URL", expand=False))
            sys.exit(1)
        
        # Extract video ID
        video_id = extract_video_id(url)
        
        # Get transcript
        progress.add_task(description=f"Extracting transcript for video ID: {video_id}...", total=None)
        try:
            transcript = get_transcript(video_id)
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            console.print(Panel(f"[bold red]Error: {str(e)}[/bold red]\n\nThis video does not have available transcripts.", 
                               title="Transcript Not Available", expand=False))
            sys.exit(1)
        except Exception as e:
            console.print(Panel(f"[bold red]Error: {str(e)}[/bold red]\n\nFailed to extract transcript.", 
                               title="Extraction Failed", expand=False))
            sys.exit(1)
        
        # Format and copy transcript
        progress.add_task(description="Formatting and copying transcript to clipboard...", total=None)
        formatted_transcript = format_transcript(transcript)
        pyperclip.copy(formatted_transcript)
        
    # Success message
    # Count line breaks and add 1 to get the number of lines
    line_count = formatted_transcript.count('\n') + 1
    console.print(Panel(
        "[bold green]Successfully extracted transcript![/bold green]\n\n"
        "The transcript has been copied to your clipboard.\n"
        f"Video ID: {video_id}\n"
        f"Character count: {len(formatted_transcript)}\n"
        f"Line count: {line_count}",
        title="Success", expand=False
    ))


@app.command()
def version():
    """Show the version of the tool."""
    from importlib.metadata import version as get_version
    try:
        version_str = get_version("yt-transcript-clipper")
        console.print(f"yt-transcript-clipper version: {version_str}")
    except Exception:
        console.print("yt-transcript-clipper version: 0.1.0")


if __name__ == "__main__":
    app()