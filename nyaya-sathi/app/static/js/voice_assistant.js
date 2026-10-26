/**
 * Nyaya Sathi - Voice Assistant Module
 * Multilingual speech recognition (STT) and text-to-speech (TTS)
 * Bridges browser Web Speech API with backend Sarvam AI endpoints.
 */

class VoiceAssistant {
  constructor() {
    this.recognition = null;
    this.isRecording = false;
    this.currentLanguage = "mr-IN";
    this.synth = window.speechSynthesis || null;
    this.setupSpeechRecognition();
  }

  setLanguage(langCode) {
    this.currentLanguage = langCode;
    if (this.recognition) {
      this.recognition.lang = langCode;
    }
  }

  setupSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = true;
      this.recognition.lang = this.currentLanguage;

      this.recognition.onstart = () => {
        this.isRecording = true;
        this.updateMicUI(true);
      };

      this.recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }

        const inputEl = document.getElementById('chat-query-input');
        if (inputEl) {
          inputEl.value = finalTranscript || interimTranscript;
        }
      };

      this.recognition.onerror = (event) => {
        console.warn("Speech recognition notice/error:", event.error);
        this.isRecording = false;
        this.updateMicUI(false);
      };

      this.recognition.onend = () => {
        this.isRecording = false;
        this.updateMicUI(false);
      };
    } else {
      console.log("Web Speech API not supported; using simulated / text fallback.");
    }
  }

  toggleRecording() {
    if (!this.recognition) {
      // Simulate quick dictation for accessibility/testing
      this.simulateVoiceDictation();
      return;
    }

    if (this.isRecording) {
      this.recognition.stop();
    } else {
      try {
        this.recognition.lang = this.currentLanguage;
        this.recognition.start();
      } catch (err) {
        console.error("Error starting speech recognition:", err);
        this.simulateVoiceDictation();
      }
    }
  }

  simulateVoiceDictation() {
    const statusEl = document.getElementById('mic-status');
    const inputEl = document.getElementById('chat-query-input');
    if (statusEl) statusEl.innerText = "माइक सक्रिय (Simulating speech input)...";
    
    // Choose phrase based on language
    const samplePhrases = {
      "mr-IN": "माझ्या मालकाने गेल्या दोन महिन्यांपासून माझा पगार दिलेला नाही. मी काय करू शकतो?",
      "hi-IN": "मेरे नियोक्ता ने मुझे दो महीने से वेतन नहीं दिया है। मैं क्या कर सकता हूँ?",
      "en-IN": "My employer has not paid my wages for two months. What can I do?"
    };

    setTimeout(() => {
      if (inputEl) inputEl.value = samplePhrases[this.currentLanguage] || samplePhrases["mr-IN"];
      if (statusEl) statusEl.innerText = "माईक बंद (भाषण ओळखले गेले / Ready)";
    }, 600);
  }

  updateMicUI(recording) {
    const micBtn = document.getElementById('mic-btn');
    const micStatus = document.getElementById('mic-status');
    if (!micBtn) return;

    if (recording) {
      micBtn.classList.add('recording');
      if (micStatus) micStatus.innerText = "🔴 ऐकत आहे... बोला / Listening... Speak now";
    } else {
      micBtn.classList.remove('recording');
      if (micStatus) micStatus.innerText = "माईक दाबा आणि आपली समस्या सांगा / Press mic and speak";
    }
  }

  speak(text) {
    if (!text) return;

    // Check if Sarvam TTS is preferred or fallback to browser speechSynthesis
    fetch('/api/voice/tts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text.slice(0, 400), language: this.currentLanguage })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success && data.audio_base64) {
        // Play base64 audio returned by Sarvam AI
        const audio = new Audio("data:audio/wav;base64," + data.audio_base64);
        audio.play();
      } else {
        // Resilient browser Web Speech synthesis fallback
        this.speakBrowserSynthesis(text);
      }
    })
    .catch(() => {
      this.speakBrowserSynthesis(text);
    });
  }

  speakBrowserSynthesis(text) {
    if (!this.synth) {
      alert("ऑडिओ उपलब्ध नाही / Audio playback not supported in this browser.");
      return;
    }
    // Cancel ongoing speech
    this.synth.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = this.currentLanguage;
    utterance.rate = 0.95; // Clear natural pace for legal clarity

    // Select voice if available
    const voices = this.synth.getVoices();
    const langPrefix = this.currentLanguage.slice(0, 2);
    const matchedVoice = voices.find(v => v.lang.startsWith(langPrefix));
    if (matchedVoice) {
      utterance.voice = matchedVoice;
    }

    this.synth.speak(utterance);
  }
}

window.voiceAssistant = new VoiceAssistant();
