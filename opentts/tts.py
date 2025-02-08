"""Support for the OpenTTS service."""

from __future__ import annotations

import requests
import voluptuous as vol
from homeassistant.components.tts import (
    CONF_LANG,
    PLATFORM_SCHEMA as TTS_PLATFORM_SCHEMA,
    Provider,
)
from homeassistant.const import CONF_EFFECT, CONF_HOST, CONF_PORT
import homeassistant.helpers.config_validation as cv

CONF_VOICE = "voice"
CONF_CODEC = "codec"
CONF_QUALITY = "quality"
CONF_LANG = "language"

SUPPORT_LANGUAGES = ["en_US", "nl", "de", "fr", "es", "it", "sv", "pl", "pt", "tr", "ja", "zh", "ko", "cs", "ar", "hi"]  # Replace with actual OpenTTS supported languages
SUPPORT_CODEC = ["MP3_FILE", "WAVE_FILE", "AIFF_FILE", "AU_FILE"]  # Include MP3 as a supported codec
SUPPORT_OPTIONS = [CONF_EFFECT]
SUPPORT_EFFECTS = {}  # Replace with actual OpenTTS supported effects

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5500
DEFAULT_LANG = "en_US"
DEFAULT_VOICE = "larynx:harvard"
DEFAULT_CODEC = "MP3_FILE"
DEFAULT_QUALITY = "high"
DEFAULT_EFFECTS: dict[str, str] = {}

MAP_OPENTTS_CODEC = {"MP3_FILE": "mp3", "WAVE_FILE": "wav", "AIFF_FILE": "aiff", "AU_FILE": "au"}

PLATFORM_SCHEMA = TTS_PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES),
        vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): cv.string,
        vol.Optional(CONF_QUALITY, default=DEFAULT_QUALITY): cv.string,
        vol.Optional(CONF_CODEC, default=DEFAULT_CODEC): vol.In(SUPPORT_CODEC),
        vol.Optional(CONF_EFFECT, default=DEFAULT_EFFECTS): {
            vol.All(cv.string, vol.In(SUPPORT_EFFECTS)): cv.string
        },
    }
)

def get_engine(hass, config, discovery_info=None):
    """Set up OpenTTS speech component."""
    return OpenTTSProvider(hass, config)

class OpenTTSProvider(Provider):
    """OpenTTS speech API provider."""

    def __init__(self, hass, conf):
        """Init OpenTTS TTS service."""
        self.hass = hass
        self._host = conf.get(CONF_HOST)
        self._port = conf.get(CONF_PORT)
        self._voice = conf.get(CONF_VOICE)
        self._lang = conf.get(CONF_LANG)
        self._quality = conf.get(CONF_QUALITY)
        self._codec = conf.get(CONF_CODEC, DEFAULT_CODEC)
        self._effects = conf.get(CONF_EFFECT, {})
        self.name = "OpenTTS"

    @property
    def default_language(self):
        """Return the default language."""
        return self._lang

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    @property
    def default_options(self):
        """Return dict including default options."""
        return {CONF_EFFECT: self._effects}

    @property
    def supported_options(self):
        """Return a list of supported options."""
        return SUPPORT_OPTIONS

    def get_tts_audio(self, message, language, options):
        """Load TTS from OpenTTS."""
        effects = options.get(CONF_EFFECT, {})
        
        # Ensure correct codec mapping
        audiotype = MAP_OPENTTS_CODEC.get(self._codec, "mp3")

        url = f"http://{self._host}:{self._port}/api/tts"
        params = {
            "voice": self._voice,
            "lang": self._lang,
            "vocoder": self._quality,
            "denoiserStrength": "0.005",
            "text": message,
            "ssml": "true",
            "codec": audiotype,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return audiotype, response.content
