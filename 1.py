import streamlit as st
import sounddevice as sd
import soundfile as sf
import streamlit as st
import tempfile
import gtts
import os
from translation_functions import (
    transcribe_audio,
    translate_text,
    text_to_speech,
    get_speech_recognition_language_code
)



LANGUAGE_OPTIONS = {
    'en': 'English',
    'hi': 'Hindi',
}

# Set page config
st.set_page_config(
    page_title="Audio Translator",
    page_icon="🎙️",
    layout="wide"
)

# Title and description
st.title("🎙️ Audio Translator")
st.markdown("""
Record audio from your microphone, select the source and target languages, and get a translated audio file!
""")

# Language selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox(
        "Source Language",
        options=list(LANGUAGE_OPTIONS.keys()),
        format_func=lambda x: LANGUAGE_OPTIONS[x],
        index=0,
        help="Select the language you will speak in"
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        options=[k for k in LANGUAGE_OPTIONS if k != 'auto'],
        format_func=lambda x: LANGUAGE_OPTIONS[x],
        index=list(LANGUAGE_OPTIONS).index('en'),
        help="Select the language you want to translate to"
    )

# Audio recording
if 'audio_recorded' not in st.session_state:
    st.session_state['audio_recorded'] = False

def record_audio():
    duration = 5  # Recording duration in seconds
    sample_rate = 48000
    recording = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=1)
    st.info("Recording... Speak now!")
    sd.wait()
    return recording, sample_rate

# Record button
if st.button("Start Recording (5 seconds)"):
    with st.spinner("Recording..."):
        recording, sample_rate = record_audio()
        
        # Save recording to temporary file
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
        sf.write(temp_wav, recording, sample_rate)
        st.session_state['audio_recorded'] = True
        st.session_state['temp_wav'] = temp_wav
        st.success("Recording completed!")

# Process the recording
if st.session_state.get('audio_recorded', False):
    try:
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        temp_wav = st.session_state['temp_wav']
        
        # Create temporary output file
        temp_output = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        
        # Step 1: Transcribe
        status_text.text("Step 1/3: Transcribing audio...")
        try:
            language_code = get_speech_recognition_language_code(source_lang)
            transcribed_text = transcribe_audio(temp_wav, language_code)
            progress_bar.progress(33)
            st.write(f"Transcribed text: {transcribed_text}")
        except Exception as e:
            st.error(f"Error in transcription: {str(e)}")
            raise

        # Step 2: Translate
        status_text.text("Step 2/3: Translating text...")
        try:
            translated_text = translate_text(transcribed_text, source_lang, target_lang)
            progress_bar.progress(66)
            st.write(f"Translated text: {translated_text}")
        except Exception as e:
            st.error(f"Error in translation: {str(e)}")
            raise

        # Step 3: Convert to speech
        status_text.text("Step 3/3: Converting to speech...")
        try:
            text_to_speech(translated_text, temp_output, language=target_lang)
            progress_bar.progress(100)
        except Exception as e:
            st.error(f"Error in text-to-speech conversion: {str(e)}")
            raise

        # Display results
        st.success("Translation completed!")
        
        # Play the translated audio
        st.audio(temp_output, format='audio/mp3')

        # Download button
        with open(temp_output, 'rb') as f:
            st.download_button(
                label="Download Translated Audio",
                data=f,
                file_name=f"translated_{target_lang}.mp3",
                mime="audio/mp3"
            )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    finally:
        # Clean up temporary files
        try:
            os.remove(temp_wav)
            os.remove(temp_output)
        except:
            pass

# Add some helpful information
st.markdown("""
### How to use:
1. Click on Record button to start recording
2. Select the source language 
3. Select the target language
4. Click 'Translate' and wait for the processing to complete
5. Listen to the translated audio or download it

### Supported Languages:
- English (en)
- Hindi (hi)
- And Many More            
            

### Troubleshooting:
1. Make sure Microphone is Connected properly 
2. Ensure you have a stable internet connection
3. Ensure the project have Microphone access
4. The audio should be in the language you selected as the source language
""")         