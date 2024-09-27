import React, { useRef, useState } from 'react';
import './AudioPlayer.css'; // Создайте файл стилей по необходимости

const AudioPlayer = ({ src }) => {
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (audio) {
      if (isPlaying) {
        audio.pause();
      } else {
        audio.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    const audio = audioRef.current;
    if (audio) {
      setProgress(audio.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    const audio = audioRef.current;
    if (audio) {
      setDuration(audio.duration);
    }
  };

  const handleSeek = (event) => {
    const audio = audioRef.current;
    if (audio) {
      const seekTime = event.target.value;
      audio.currentTime = seekTime;
      setProgress(seekTime);
    }
  };

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        src={src}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
      />
      <button onClick={togglePlayPause}>
        {isPlaying ? 'Пауза' : 'Воспроизвести'}
      </button>
      <input
        type="range"
        min="0"
        max={duration}
        value={progress}
        onChange={handleSeek}
      />
      <div>
        {Math.floor(progress)} / {Math.floor(duration)} секунд
      </div>
    </div>
  );
};

export default AudioPlayer;