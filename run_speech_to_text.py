import argparse
import keyboard as listening_keyboard
import logging
import pyaudio
import sys

from google.cloud import speech
from pynput import keyboard as typing_keyboard
from six.moves import queue

from utils import find_first_diff


# Set up logging to stdout
controller = typing_keyboard.Controller()
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


# Shortcuts to toggle transcription on and off or terminate completely.
SHORTCUT_TOGGLE = "ctrl+space"
SHORTCUT_TERMINATE = "ctrl+shift+esc"


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """
    Opens a recording stream as a generator yielding the audio chunks.
    """

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self._closed = True

    def __enter__(self):
        """
        Start receiving input audio.
        """

        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self._closed = False

        return self

    def __exit__(self, type, value, traceback):
        """
        Stop receiving input audio.
        """

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """
        Continuously collect data from the audio stream, into the buffer.
        This is called by `self._audio_interface`.
        """
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        """
        Continuously yield data from the audio stream buffer.
        """
        while not self._closed:
            chunk = self._buff.get()
            yield chunk


class SpeechTranscriber:
    """
    Continuously listen to audio input, transcribe speech-to-text, and
    control the keyboard to type out the output.
    """

    def __init__(self, streaming_config):
        self.client = speech.SpeechClient()
        self.streaming_config = streaming_config

    def run(self):
        """
        Start the input audio stream and continuously send requests to Google's
        API for speech to text transcription.
        """

        print("Starting transcription!")

        with MicrophoneStream(RATE, CHUNK) as stream:

            responses = self.client.streaming_recognize(
                self.streaming_config,
                self.requests_generator(stream.generator())
            )

            self.listen_print_loop(responses)

    def requests_generator(self, stream_generator):
        """
        Continuously send requests to Google's API for transcription and yield
        the results.

        Note: It will stop this loop of requests, as well as the input audio
        stream whenever SHORTCUT_TOGGLE is pressed.
        """

        while True:

            # Listen for keyboard events to cut connection and audio stream.
            if listening_keyboard.is_pressed(SHORTCUT_TOGGLE):
                print("Stopping transcription!")
                break

            content = next(stream_generator)
            yield speech.StreamingRecognizeRequest(audio_content=content)
    
    def listen_print_loop(self, responses):
        """
        Iterates through server responses and types out the transcripts. This
        effectively presses the users keyboard so that the current best guess of
        the transcript matches what the user see's by their cursor.
        """

        utterance = "" # What has been currently typed by the keyboard.
        for response in responses:

            result = response.results[0]
            stability = result.stability
            transcript = result.alternatives[0].transcript

            # Find first character doesn't align with the transcript.
            diff_index = find_first_diff(utterance, transcript)
            cursor_index = len(utterance)

            # Delete characters that don't match the current transcript.
            num_to_backspace = cursor_index - diff_index
            for _ in range(0, num_to_backspace):
                controller.tap(typing_keyboard.Key.backspace)

            # Type out the new characters.
            utterance = utterance[:diff_index]
            new_chars = transcript[diff_index:]
            controller.type(new_chars)
            utterance += new_chars

            logger.debug(f"Transcript: (stability={stability:0.2f})")
            logger.debug(f"     Hearing: {transcript}")
            logger.debug(f"     Written: {utterance}")
            logger.debug(f"     Backspaced {num_to_backspace} times and typed '{new_chars}'")

            # Eventually, the guesses converge abd the API recognizes one
            # complete utterance. We can start typing a whole new utterance.
            if result.is_final:

                # Reset utterance.
                utterance = ""

                # Log the confidence of the completed utterance.
                confidence = result.alternatives[0].confidence
                logger.debug(f"Final transcription confidence={confidence:0.2f}")
                logger.debug("------------------\n")


def main():

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US',  # a BCP-47 language tag,
        enable_automatic_punctuation=True,
        enable_spoken_punctuation=True,
        # model="latest_long",
        # use_enhanced=True
    )

    # Interim_results enable a stream of guesses and a smoother flow for typing.
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        # enable_voice_activity_events=True,
        # single_utterance=True,
    )

    # Stream audio to Google's API and type out the transcribe text.
    transcriber = SpeechTranscriber(streaming_config)

    # Start transcribing when shortcut is pressed.
    listening_keyboard.add_hotkey(SHORTCUT_TOGGLE, transcriber.run)
    print(f"Press {SHORTCUT_TOGGLE} to start and stop recording...")
    print(f"Press {SHORTCUT_TERMINATE} to terminate the program...")

    # Listen indefinitely for the user shortcuts to start, stop, and terminate.
    listening_keyboard.wait(SHORTCUT_TERMINATE)
    print("Program terminated...we're done!")


if __name__ == '__main__':

    # Add argument for verbose logging.
    parser = argparse.ArgumentParser(description="A personal speech to text transcriber.")
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help='Enable verbose output for debugging.'
    )

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger(__name__).setLevel(logging.DEBUG)
        # logger.debug("Setting log level |

    # Start the program.
    print("Welcome to your personal speech-to-text tool...!")
    main()
