// static/js/main.js

let mediaRecorder;
let audioChunks = [];

const micBtn = document.getElementById("mic-btn");
const micLabel = document.getElementById("mic-label");
const responseText = document.getElementById("response-text");
const langSelect = document.getElementById("lang");

micBtn.addEventListener("click", async () => {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    startRecording();
  } else {
    stopRecording();
  }
});

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];
      mediaRecorder.start();
      micLabel.innerText = "Recording...";

      mediaRecorder.addEventListener("dataavailable", event => {
        audioChunks.push(event.data);
      });

      mediaRecorder.addEventListener("stop", () => {
        sendAudio();
        stream.getTracks().forEach(t => t.stop());
      });
    })
    .catch(err => {
      console.error("getUserMedia error:", err);
      responseText.innerText = "Microphone access denied.";
    });
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    micLabel.innerText = "Processing...";
  }
}

function sendAudio() {
  const blob = new Blob(audioChunks, { type: "audio/wav" });
  const fd = new FormData();
  fd.append("audio", blob, "recording.wav");
  fd.append("lang", langSelect.value || "en");

  fetch("/process_audio", { method: "POST", body: fd })
    .then(r => r.json())
    .then(data => {
      if (data.ok) {
        responseText.innerText = data.response;
        speakResponse(data.response, langSelect.value);
      } else {
        responseText.innerText = "Error: " + (data.error || "unknown");
      }
      micLabel.innerText = "Start";
    })
    .catch(err => {
      console.error(err);
      responseText.innerText = "Network error.";
      micLabel.innerText = "Start";
    });
}

function speakResponse(text, lang) {
  // Use browser TTS as a fallback; backend already tries pyttsx3
  try {
    const utter = new SpeechSynthesisUtterance(text);
    if (lang === "hi") utter.lang = "hi-IN";
    else if (lang === "kn") utter.lang = "kn-IN";
    else utter.lang = "en-US";
    speechSynthesis.speak(utter);
  } catch (e) {
    console.warn("Browser TTS failed:", e);
  }
}
