import { useRef, useState } from 'react';

export default function useAudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);

      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.start();
      mediaRecorderRef.current = mediaRecorder;
      setIsRecording(true);

      console.log('Recording started.');
    } catch (err) {
      console.error('Error accessing microphone:', err);
      alert('Microphone access was denied or not possible.');
    }
  };

  // Stop recording
  const stopRecording = () => {
    const mediaRecorder = mediaRecorderRef.current;
    if (mediaRecorder) {
      mediaRecorder.stop();
      console.log('Recording stopped.');
    }
    setIsRecording(false);
  };

  // Return the recorded Blob
  const getAudioBlob = () => {
    return new Blob(audioChunksRef.current, { type: 'audio/webm' });
  };

  return {
    isRecording,
    startRecording,
    stopRecording,
    getAudioBlob
  };
}
