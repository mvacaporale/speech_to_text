# Speech to Text on Windows + Linux

This is a tool for enabling fast speech-to-text transcription on your computer. It
was inspired by the Pixel phone's excellent dictation and the desire to have
something similar on my laptop for day-to-day use.

It uses Google Cloud's speech transcriber and therefore requires a connection to
the internet for use, but the performance is still quite good despite the
latency to send and receive transcription requests.

**Note:** As of now, it only definitely works on Windows due to limitations of the
`keyboard` package on Mac OS. It has not been tested on Linux but should work.

# Usage

You can configure the shortcut at the top of the script. By default, press
`ctrl+space` to start and stop transcribing and `ctrl+shift+esc` to exit the
program completely.

The script takes control of your keyboard as if it were physically tapping the
keys. Be careful of pressing extraneous keys while it's working to avoid
unwanted key combinations (e.g. `ctrl+<something>`).

<div>
    <a href="https://www.loom.com/share/84d579d54a4746a9831868a5b560627d">
      <p>Speech-to-text demo - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/84d579d54a4746a9831868a5b560627d">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/84d579d54a4746a9831868a5b560627d-with-play.gif">
    </a>
  </div>

# Setup

1. Follow the instructions to install `pyaudio` [here](https://pypi.org/project/PyAudio/)

2. Install remaining python dependencies
```
pip install -r requirements.txt
```

3. Set up an account with Google Cloud

* Create a Google Cloud account
* Create a new project in the Google Cloud Console
* Enable the Speech-to-Text API for your project
* Install the `gcloud` CLI ([link](https://cloud.google.com/sdk/docs/install))
  and configure to your new project


4. Run the program!
```
python run_speech_to_text.py
```

