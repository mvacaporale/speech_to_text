# Speech to Text on Desktop

This is tool for enabling fast speech-to-text transcription on your desktop. It
was inspired by the Pixel phone's excellent dictation and the desire to have
something similar on my personal computer.

It uses Google Cloud's speech transcriber, and therefore require connection to
the internet for use, but the performance is still quite good despite the
latency to send and receive transcription requests.

# Usage

You can can configure the shortcut at the top of the script. By default, press
`ctrl+space` to start and stop transcribing and `ctrl+shift+esc` to exit the
program completely.

<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/556de9342df641d5b19322218ea3dc3a?sid=10f323e6-1ab7-4eb9-a7b5-536a1e7fe275" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

<div>
    <a href="https://www.loom.com/share/556de9342df641d5b19322218ea3dc3a">
      <p> Loom speech to text demo draft 4 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/556de9342df641d5b19322218ea3dc3a">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/556de9342df641d5b19322218ea3dc3a-with-play.gif">
    </a>
  </div>

The script takes control of your keyboard as if it was physically tapping the
keys. Be careful to avoid pressing extraneous keys as it's transcribing.
Otherwise you may enter unwanted combinations (e.g.
`ctrl+<something>`).

# Setup

1. Install python dependencies
```
pip install requirements.txt
```

2. Set up an account with Google Cloud

* Create a Google Cloud account
* Create a new project in the Google Cloud Console
* Enable the Speech-to-Text API for your project
* Install the `gcloud` CLI ([link](https://cloud.google.com/sdk/docs/install))
  and configure to your new project


3. Run the program!
```
python run_speech_to_text.py
```

