# YouTube Transcript Clipper

A lean, fast command-line utility to extract transcripts from YouTube videos and copy them directly to your clipboard.

## Features

- Extract transcripts from any YouTube video with available captions
- Copy extracted transcripts directly to system clipboard
- Validate YouTube URLs before attempting extraction
- Handle various YouTube URL formats (standard, shortened, embedded, and shorts)
- Provide clear, user-friendly feedback with progress indicators
- Cross-platform support (Windows, macOS, Linux)
- Minimal dependencies for fast execution

## Installation

### Requirements

- Python 3.8 or higher

### Install from GitHub

```bash
# Clone the repository
git clone https://github.com/Sharma-IT/yt-transcript-clipper.git

# Navigate to the project directory
cd yt-transcript-clipper

# Install the package
pip install -e .
```

### Direct Installation

```bash
pip install git+https://github.com/Sharma-IT/yt-transcript-clipper.git
```

## Usage

After installation, you can use the tool from anywhere in your terminal:

```bash
# Extract transcript and copy to clipboard
yt-transcript-clipper clip "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Show version information
yt-transcript-clipper version

# Show help information
yt-transcript-clipper --help
```

### Examples

1. Extract transcript from a standard YouTube URL:

```bash
yt-transcript-clipper clip "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

2. Extract transcript from a shortened URL:

```bash
yt-transcript-clipper clip "https://youtu.be/dQw4w9WgXcQ"
```

3. Extract transcript from YouTube Shorts:

```bash
yt-transcript-clipper clip "https://www.youtube.com/shorts/dQw4w9WgXcQ"
```

## Troubleshooting

### Common Issues

1. **No transcript available**

   If the video doesn't have any captions or transcripts available, you'll receive an error message. Unfortunately, not all YouTube videos have transcripts available.

2. **Invalid URL**

   Ensure you're providing a valid YouTube URL. The tool supports various YouTube URL formats but won't work with other video platforms.

3. **Clipboard Issues**

   If the transcript isn't copied to your clipboard, ensure you have the necessary dependencies for your specific operating system:

   - **Windows**: No additional dependencies required.
   - **macOS**: No additional dependencies required.
   - **Linux**: Depending on your distro, you might need `xclip` or `xsel`:

     ```bash
     # For Debian/Ubuntu
     sudo apt-get install xclip
     
     # For Fedora
     sudo dnf install xclip
     ```

## Development

### Running Tests

```bash
# Navigate to the project directory
cd yt-transcript-clipper

# Run the tests
python -m unittest discover
```

### Building from Source

```bash
# Navigate to the project directory
cd yt-transcript-clipper

# Install development dependencies
pip install -e ".[dev]"

# Build the package
python setup.py sdist bdist_wheel
```

## Compliance with YouTube Terms of Service

This tool uses the public YouTube API and follows YouTube's terms of service for data access. It only extracts publicly available transcripts that YouTube provides for videos. Please use this tool responsibly and respect content creators' rights.

## License

MIT

## Author

Shubham Sharma | [GitHub](https://github.com/Sharma-IT) | [Email](mailto:shubhamsharma.emails@gmail.com)
