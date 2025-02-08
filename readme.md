# OpenTTS Custom "legacy" Component for Home Assistant

## Description
This is a custom "legacy" component for integrating OpenTTS with Home Assistant, allowing you to generate speech using various text-to-speech (TTS) engines supported by OpenTTS.

## Features
- Full support for SSML (Speech Synthesis Markup Language), allowing for advanced speech control and formatting
- Supports multiple TTS engines via OpenTTS
- Customizable voices, languages, and audio formats
- Integration with Home Assistant's TTS service
- Configurable SSML support for enhanced speech synthesis

## Prerequisites
1. **Home Assistant** – Ensure you have a running instance of Home Assistant.
2. **OpenTTS Server** – Install and configure OpenTTS. You can find more details at [OpenTTS GitHub](https://github.com/synesthesiam/opentts).
     - Running in docker is the simplest method
     - I used this setup running as a deamon (* The :all option gives you support for all languages)
          ```bash
          docker run -dit --restart unless-stopped --name="opentts" -p 5500:5500 synesthesiam/opentts:all
          ```
3. **Required Dependencies** – The component requires `requests` for handling HTTP requests.

## Installation
### Manual Installation
1. Navigate to your Home Assistant configuration directory:
   ```sh
   cd config/custom_components
   ```
2. Create a new folder for OpenTTS:
   ```sh
   mkdir opentts
   ```
3. Copy the following files into the `opentts` directory:
   - `__init__.py`
   - `tts.py`
   - `manifest.json`
4. Restart Home Assistant to detect the new component.

## Configuration
To enable OpenTTS in Home Assistant, add the following to your `configuration.yaml`:

```yaml
tts:
  - platform: opentts 
    host: "[host name or ip]" 
    voice: "larynx:rdh-glow_tts"
    service_name: opentts_nl
```

### Supported Languages
This integration supports multiple languages via OpenTTS instead of the marytts option thats very limited. Below are some of the available options:

```yaml
SUPPORTED_LANGUAGES = [
    "en_US", "nl", "de", "fr", "es", "it", "ru", "sv", "pl", "pt",
    "tr", "ja", "zh", "ko", "cs", "ar", "hi"
]
```

### Supported Codecs
The integration supports various audio formats:
```yaml
SUPPORTED_CODEC = ["MP3_FILE", "WAVE_FILE", "AIFF_FILE", "AU_FILE"]
```

## SSML Support

Unlike MaryTTS, which had issues processing complex SSML inputs, this OpenTTS integration provides limited SSML support, following the structure defined in [OpenTTS SSML Example](https://github.com/synesthesiam/opentts/blob/master/etc/ssml_example.xml). While it allows for speech synthesis customization, its capabilities are constrained by the supported engines and their individual implementations. Some SSML features such as pauses (`<break>`), emphasis, and language switching are supported, but advanced SSML elements may not work as expected.
OpenTTS provides limited SSML support, following the structure defined in [OpenTTS SSML Example](https://github.com/synesthesiam/opentts/blob/master/etc/ssml_example.xml). While it allows for speech synthesis customization, its capabilities are constrained by the supported engines and their individual implementations. Some SSML features such as pauses (`<break>`), emphasis, and language switching are supported, but advanced SSML elements may not work as expected.
Unlike MaryTTS, which had issues processing complex SSML inputs, this OpenTTS integration fully supports SSML, enabling detailed speech synthesis customization. You can include elements such as pauses, different voices, and language-specific pronunciations.

### Example SSML Usage
OpenTTS supports a subset of SSML features. The following example demonstrates basic SSML functionality, including text structuring and pauses:

```xml
<speak>
    <s>Hello, this is an SSML test.</s>
    <break time="1s"/>
    <s>Here is another sentence.</s>
</speak>
```
```
```

## Usage
- Once configured, you can use OpenTTS via Home Assistant's built-in TTS services.
- Example automation:

```yaml
alias: Speak Time
trigger:
  - platform: time_pattern
    minutes: "*/10"
action:
  - service: tts.speak
    data:
      entity_id: media_player.living_room
      message: "The current time is {{ now().strftime('%H:%M') }}."
```

## Troubleshooting
- If TTS audio does not play, ensure OpenTTS is running and accessible at the configured host and port.
- Check Home Assistant logs for errors related to TTS.
- Verify that the correct voice and codec are set in `configuration.yaml`.

## Contributing
Feel free to contribute by submitting a pull request or reporting issues on GitHub.

## License
This project is licensed under the MIT License.

