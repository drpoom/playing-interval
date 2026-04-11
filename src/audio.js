// Ambient sound system using Web Audio API (no audio files needed)
// Generates procedural sounds for game events

let ctx = null

function getCtx() {
  if (!ctx) {
    ctx = new (window.AudioContext || window.webkitAudioContext)()
  }
  if (ctx.state === 'suspended') ctx.resume()
  return ctx
}

// Simple tone beep
function playTone(freq, duration, type = 'sine', volume = 0.15) {
  if (!isSoundEnabled()) return
  try {
    const c = getCtx()
    const osc = c.createOscillator()
    const gain = c.createGain()
    osc.type = type
    osc.frequency.value = freq
    gain.gain.setValueAtTime(volume, c.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + duration)
    osc.connect(gain)
    gain.connect(c.destination)
    osc.start(c.currentTime)
    osc.stop(c.currentTime + duration)
  } catch (_) { /* audio not available */ }
}

// Noise burst (for UI taps)
function playNoise(duration, volume = 0.05) {
  if (!isSoundEnabled()) return
  try {
    const c = getCtx()
    const bufferSize = c.sampleRate * duration
    const buffer = c.createBuffer(1, bufferSize, c.sampleRate)
    const data = buffer.getChannelData(0)
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * volume
    }
    const source = c.createBufferSource()
    const gain = c.createGain()
    source.buffer = buffer
    gain.gain.setValueAtTime(volume, c.currentTime)
    gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + duration)
    source.connect(gain)
    gain.connect(c.destination)
    source.start()
  } catch (_) { /* audio not available */ }
}

function isSoundEnabled() {
  return localStorage.getItem('mooyang_sound') !== 'off'
}

function setSoundEnabled(on) {
  localStorage.setItem('mooyang_sound', on ? 'on' : 'off')
}

function toggleSound() {
  const now = isSoundEnabled()
  setSoundEnabled(!now)
  return !now
}

// Named sound effects
export const sfx = {
  // UI tap / click
  tap() {
    playTone(880, 0.08, 'sine', 0.1)
  },
  // Item pickup
  pickup() {
    playTone(523, 0.1, 'sine', 0.12)
    setTimeout(() => playTone(784, 0.15, 'sine', 0.1), 80)
  },
  // Dialogue appear
  dialogue() {
    playNoise(0.04, 0.04)
  },
  // Scene transition whoosh
  transition() {
    playTone(200, 0.3, 'sine', 0.06)
  },
  // Success fanfare (puzzle solved)
  success() {
    playTone(523, 0.15, 'sine', 0.12)
    setTimeout(() => playTone(659, 0.15, 'sine', 0.12), 120)
    setTimeout(() => playTone(784, 0.25, 'sine', 0.12), 240)
  },
  // Error buzz
  error() {
    playTone(200, 0.15, 'square', 0.08)
  },
  // Examine (curious sound)
  examine() {
    playTone(440, 0.06, 'triangle', 0.08)
    setTimeout(() => playTone(520, 0.08, 'triangle', 0.06), 60)
  },
}

export { isSoundEnabled, toggleSound }