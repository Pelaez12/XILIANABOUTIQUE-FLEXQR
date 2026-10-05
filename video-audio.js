const video = document.querySelector('#hero-video');
const sound = document.querySelector('#video-sound');
const status = document.querySelector('#video-status');

function updateAudio() {
  if (!video || !sound) return;
  sound.textContent = video.muted ? 'Activar audio' : 'Desactivar audio';
  sound.setAttribute('aria-pressed', String(!video.muted));
}

export async function startVideo() {
  if (!video) return;
  try {
    await video.play();
    status.textContent = '';
  } catch (error) {
    if (error.name === 'NotAllowedError' && !video.muted) {
      video.muted = true;
      try {
        await video.play();
        status.textContent = 'Tu navegador bloqueó el sonido automático. Puedes activarlo con el botón de audio.';
      } catch {
        status.textContent = 'Pulsa el botón de audio para iniciar el video.';
      }
    } else {
      status.textContent = 'No se pudo reproducir el video. Pulsa el botón de audio para intentarlo de nuevo.';
    }
  }
  updateAudio();
}

if (video) {
  video.muted = false;
  video.defaultMuted = false;
  video.volume = 1;
  updateAudio();
  video.addEventListener('volumechange', updateAudio);
  video.addEventListener('error', () => { status.textContent = 'No se pudo cargar el video. Comprueba tu conexión e inténtalo de nuevo.'; });
  sound.addEventListener('click', () => {
    video.muted = !video.muted;
    updateAudio();
    status.textContent = '';
    if (video.paused) startVideo();
  });
}
