import asyncio
import logging
import os
import sys
from pathlib import Path
import yt_dlp # Added yt-dlp

from fastapi import Depends, FastAPI, Request, BackgroundTasks # Added Request, BackgroundTasks
from fastapi.responses import JSONResponse # Added JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from load_dotenv import load_dotenv
from spotdl.types.options import DownloaderOptions, WebOptions
from spotdl.utils.arguments import parse_arguments
from spotdl.utils.config import create_settings
from spotdl.utils.logging import NAME_TO_LEVEL
from spotdl.utils.spotify import SpotifyClient
from spotdl.utils.web import (
    ALLOWED_ORIGINS,
    SPAStaticFiles,
    app_state,
    fix_mime_types,
    get_current_state,
    router,
)
from uvicorn import Config, Server

load_dotenv()

__version__ = '1.1.1'
logger = logging.getLogger(__name__)
DOWNLOAD_DIR = Path(os.getenv('DOWNLOAD_DIR', '/downloads'))
WEB_GUI_LOCATION = os.getenv('WEB_GUI_LOCATION', '/downtify/frontend/dist')


def web(web_settings: WebOptions, downloader_settings: DownloaderOptions):
    """
    Run the web server.

    ### Arguments
    - web_settings: Web server settings.
    - downloader_settings: Downloader settings.
    """

    # Apply the fix for mime types
    fix_mime_types()

    # Set up the app loggers
    uvicorn_logger = logging.getLogger('uvicorn')
    uvicorn_logger.propagate = False

    spotipy_logger = logging.getLogger('spotipy')
    spotipy_logger.setLevel(logging.NOTSET)

    # Initialize the web server settings
    app_state.web_settings = web_settings
    app_state.logger = uvicorn_logger

    # Create the event loop
    app_state.loop = (
        asyncio.new_event_loop()
        if sys.platform != 'win32'
        else asyncio.ProactorEventLoop()  # type: ignore
    )

    downloader_settings['simple_tui'] = True
    web_settings['web_gui_location'] = WEB_GUI_LOCATION

    # Download web app from GitHub if not already downloaded or force flag set
    web_app_dir = WEB_GUI_LOCATION

    app_state.api = FastAPI(
        title='Downtify',
        description='Download your Spotify playlists and songs along with album art and metadata in a self-hosted way via Docker.',
        version=__version__,
        dependencies=[Depends(get_current_state)],
    )

    # Add exception handler for JSON 500 responses
    @app_state.api.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"message": str(exc)},
        )

    app_state.api.include_router(router)

    @app_state.api.get('/list')
    def list_downloads():
        downloads_dir = str(DOWNLOAD_DIR)
        audio_exts = {'.mp3', '.m4a', '.flac', '.ogg', '.wav', '.aac', '.opus'}
        image_exts = {'.jpg', '.jpeg', '.png', '.webp'}
        try:
            entries = set(os.listdir(downloads_dir)) # Use set for O(1) lookup
        except FileNotFoundError:
            return []

        files = []
        for entry in entries:
            full_path = os.path.join(downloads_dir, entry)
            if os.path.isfile(full_path):
                basename, ext = os.path.splitext(entry)
                if ext.lower() in audio_exts:
                    # Look for matching image
                    image_file = None
                    for img_ext in image_exts:
                        if (basename + img_ext) in entries:
                            image_file = basename + img_ext
                            break
                    
                    files.append({
                        "name": entry,
                        "timestamp": os.path.getmtime(full_path) * 1000, # JS expects ms
                        "size": os.path.getsize(full_path),
                        "image": image_file
                    })

        # Default sort by newest
        files.sort(key=lambda x: x['timestamp'], reverse=True)
        return files

    @app_state.api.delete('/delete')
    def delete_download(file: str):
        downloads_dir = str(DOWNLOAD_DIR)
        full_path = os.path.join(downloads_dir, file)
        if not os.path.isfile(full_path):
            return {'deleted': False, 'error': 'File not found'}
        try:
            os.remove(full_path)
        except Exception as e:
            return {'deleted': False, 'error': str(e)}
        return {'deleted': True}

    # Add the CORS middleware
    app_state.api.add_middleware(
        CORSMiddleware,
        allow_origins=(
            ALLOWED_ORIGINS + web_settings['allowed_origins']
            if web_settings['allowed_origins']
            else ALLOWED_ORIGINS
        ),
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Expose downloads as static files for direct links
    app_state.api.mount(
        '/downloads',
        StaticFiles(directory=str(DOWNLOAD_DIR)),
        name='downloads',
    )

    @app_state.api.post('/api/download/soundcloud')
    def download_soundcloud(url: str, client_id: str, format: str = 'mp3'):
        """
        Download a song from SoundCloud using yt-dlp.
        """
        logger.info(f"Starting SoundCloud download: {url} in format {format}")
        
        try:
            # Clean format to valid extension/codec
            valid_formats = {'mp3', 'flac', 'm4a', 'opus', 'wav', 'ogg'}
            if format not in valid_formats:
                format = 'mp3'

            out_tmpl = str(DOWNLOAD_DIR / '%(uploader)s - %(title)s.%(ext)s')
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': out_tmpl,
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': format,
                        'preferredquality': '192',
                    },
                    {
                        'key': 'FFmpegThumbnailsConvertor',
                        'format': 'jpg',
                    },
                    {
                        'key': 'EmbedThumbnail',
                    },
                    {
                        'key': 'FFmpegMetadata',
                    }
                ],
                'writethumbnail': True,
                'quiet': False,
                'no_warnings': True,
                'ignoreerrors': True, # Skip errors in playlist
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Handle Playlist vs Single Track
                if 'entries' in info:
                    entries = list(info['entries'])
                    if entries:
                        # Return the name of the first track for UI feedback
                        # (The loop handled downloads, entries contains info dicts)
                        # We use the first one to determine the filename pattern
                        first_entry = entries[0]
                        # prepare_filename expects a dict
                        filename = ydl.prepare_filename(first_entry)
                        final_filename = os.path.splitext(filename)[0] + '.' + format
                    else:
                        return "Empty Playlist"
                else:
                    filename = ydl.prepare_filename(info)
                    final_filename = os.path.splitext(filename)[0] + '.' + format
                
            logger.info(f"SoundCloud download complete (or first file): {final_filename}")
            return os.path.basename(final_filename)
            
        except Exception as e:
            logger.error(f"SoundCloud download failed: {str(e)}")
            return JSONResponse(status_code=500, content={"message": str(e)})

    # Add the static files for the SPA (must be mounted after /downloads)
    app_state.api.mount(
        '/',
        SPAStaticFiles(directory=web_app_dir, html=True),
        name='static',
    )
    config = Config(
        app=app_state.api,
        host=web_settings['host'],
        port=web_settings['port'],
        workers=1,
        log_level=NAME_TO_LEVEL[downloader_settings['log_level']],
        loop=app_state.loop,  # type: ignore
    )
    if web_settings['enable_tls']:
        logger.info('Enabling TLS')
        config.ssl_certfile = web_settings['cert_file']
        config.ssl_keyfile = web_settings['key_file']
        config.ssl_ca_certs = web_settings['ca_file']

    app_state.server = Server(config)

    app_state.downloader_settings = downloader_settings

    if not web_settings['web_use_output_dir']:
        logger.info(
            'Files are stored in temporary directory '
            'and will be deleted after the program exits '
            'to save them to current directory permanently '
            'enable the `web_use_output_dir` option '
        )
    else:
        logger.info(
            'Files are stored in current directory '
            'to save them to temporary directory '
            'disable the `web_use_output_dir` option '
        )

    logger.info('Starting web server \n')

    # Start the web server
    app_state.loop.run_until_complete(app_state.server.serve())


if __name__ == '__main__':
    # Parse the arguments
    arguments = parse_arguments()

    # Create settings dicts
    spotify_settings, downloader_settings, web_settings = create_settings(
        arguments
    )

    web_settings['web_use_output_dir'] = True
    downloader_settings['output'] = str(
        DOWNLOAD_DIR / '{artists} - {title}.{output-ext}'
    )
    # Add fallback audio providers: try YouTube if YouTube Music fails
    downloader_settings['audio_providers'] = ['youtube-music', 'youtube']
    spotify_settings['client_id'] = os.getenv(
        'CLIENT_ID', '5f573c9620494bae87890c0f08a60293'
    )
    spotify_settings['client_secret'] = os.getenv(
        'CLIENT_SECRET', '212476d9b0f3472eaa762d90b19b0ba8'
    )

    # Initialize spotify client
    SpotifyClient.init(**spotify_settings)
    spotify_client = SpotifyClient()

    # Start web ui
    # Start web ui
    web(web_settings, downloader_settings)
