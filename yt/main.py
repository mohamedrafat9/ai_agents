from src.llm.factory import get_llm
from langchain.agents import create_agent
import re
from pytube import YouTube , Search
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.tools import tool
import yt_dlp
from typing import List, Dict
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
import json
import warnings
warnings.filterwarnings("ignore")
import logging
pytube_logger = logging.getLogger('pytube')
pytube_logger.setLevel(logging.ERROR)
yt_dpl_logger = logging.getLogger('yt_dlp')
yt_dpl_logger.setLevel(logging.ERROR)
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(text: str) -> str:
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

llm=get_llm(provider="groq")
tools=[]

@tool
def extract_video_id(url: str) -> str:
    """
    Extracts the 11-character YouTube video ID from a URL.
    Args:
        url (str): A YouTube URL containing a video ID.
    Returns:
        str: Extracted video ID or error message if parsing fails.
    """
    # Regex pattern to match video IDs
    pattern = r'(?:v=|be/|embed/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else "Error: Invalid YouTube URL"

# print(extract_video_id.invoke({
#     "url": "https://www.youtube.com/watch?v=ZWdF4gHC214"
# }))
tools.append(extract_video_id)

@tool
def fetch_transcript(video_id: str, language: str = "en") -> str:
    """
    Fetches the transcript of a YouTube video.
    Args:
        video_id (str): The YouTube video ID (e.g., "dQw4w9WgXcQ").
        language (str): Language code for the transcript (e.g., "en", "es").
    Returns:
        str: The transcript text or an error message.
    """
    
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id, languages=[language])
        return " ".join([snippet.text for snippet in transcript.snippets])
    except Exception as e:
        return f"Error: {str(e)}"

tools.append(fetch_transcript)


@tool
def search_youtube(query: str) -> List[Dict[str, str]]:
    """
        Search YouTube for videos matching the query.
        
        Args:
            query (str): The search term to look for on YouTube
            
        Returns:
            List of dictionaries containing video titles and IDs in format:
            [{'title': 'Video Title', 'video_id': 'abc123'}, ...]
            Returns error message if search fails
    """
    try:
        options = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(
                f"ytsearch5:{query}",
                download=False,
            )

        return [
            {
                "title": video.get("title", ""),
                "video_id": video.get("id", ""),
                "url": video.get("url", ""),
            }
            for video in result.get("entries", [])
        ]

    except Exception as error:
        return [{"error": str(error)}]


tools.append(search_youtube)

@tool
def get_full_metadata(url:str) -> Dict[str, str]:
    """
    Fetch full metadata for a YouTube video given its URL.
    Args:
        url (str): The YouTube video URL.
    Returns:
        Dictionary containing video metadata or an error message.
    """
    try:
        options = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            'title': info.get('title'),
            'views': info.get('view_count'),
            'duration': info.get('duration'),
            'channel': info.get('uploader'),
            'likes': info.get('like_count'),
            'comments': info.get('comment_count'),
            'chapters': info.get('chapters', [])
        }

    except Exception as error:
        return {"error": str(error)}

@tool
def get_thumbnails(url: str) -> List[Dict]:
    """
    Fetches the thumbnails of a YouTube video given its URL.
    Args:
        url (str): The YouTube video URL.
    Returns:
        List of dictionaries containing thumbnail URLs and their resolutions or an error message.
    """
    try:
        options = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

            thumbnails = []
            for t in info.get('thumbnails', []):
                if 'url' in t:
                    thumbnails.append({
                        "url": t['url'],
                        "width": t.get('width'),
                        "height": t.get('height'),
                        "resolution": f"{t.get('width', '')}x{t.get('height', '')}".strip('x')
                    })
            return thumbnails

    except Exception as error:
        return [{"error": str(error)}]

tools.append(get_full_metadata)
tools.append(get_thumbnails)


print(search_youtube.invoke({"query":"Python programming"}))

agent =create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful YouTube assistant.",
    )

        