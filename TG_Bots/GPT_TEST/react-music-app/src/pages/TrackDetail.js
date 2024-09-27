import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import AudioPlayer from '../components/AudioPlayer';
import axios from 'axios';

const TrackDetail = () => {
  const { id } = useParams();
  const [track, setTrack] = useState(null);

  useEffect(() => {
    const fetchTrack = async () => {
      try {
        const response = await axios.get(`/api/music/tracks/${id}/`);
        setTrack(response.data);
      } catch (error) {
        console.error('Ошибка при загрузке трека:', error);
      }
    };

    fetchTrack();
  }, [id]);

  if (!track) return <div>Загрузка...</div>;

  return (
    <div>
      <h2>{track.title}</h2>
      <p>Исполнитель: {track.album.artist.name}</p>
      <p>Альбом: {track.album.title}</p>
      <AudioPlayer src={track.audio_file} />
    </div>
  );
};

export default TrackDetail;