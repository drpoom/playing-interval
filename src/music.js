// Procedural ambient music using Web Audio API
// Generates gentle looping background music per scene

let musicCtx = null
let musicGain = null
let currentLoop = null
let isPlaying = false

function getMusicCtx() {
  if (!musicCtx) {
    musicCtx = new (window.AudioContext || window.webkitAudioContext)()
    musicGain = musicCtx.createGain()
    musicGain.gain.value = 0.08
    musicGain.connect(musicCtx.destination)
  }
  if (musicCtx.state === 'suspended') musicCtx.resume()
  return musicCtx
}

function isMusicEnabled() {
  return localStorage.getItem('mooyang_music') !== 'off'
}

function setMusicEnabled(on) {
  localStorage.setItem('mooyang_music', on ? 'on' : 'off')
}

function toggleMusic() {
  const now = isMusicEnabled()
  setMusicEnabled(!now)
  if (!now) {
    startAmbient(currentSceneName)
  } else {
    stopAmbient()
  }
  return !now
}

let currentSceneName = 'title'

// Play a single note with ADSR envelope
function playNote(ctx, dest, freq, startTime, duration, type = 'sine', vol = 0.12) {
  const osc = ctx.createOscillator()
  const env = ctx.createGain()
  osc.type = type
  osc.frequency.value = freq
  // ADSR
  env.gain.setValueAtTime(0.001, startTime)
  env.gain.linearRampToValueAtTime(vol, startTime + 0.05)
  env.gain.linearRampToValueAtTime(vol * 0.6, startTime + duration * 0.4)
  env.gain.linearRampToValueAtTime(0.001, startTime + duration)
  osc.connect(env)
  env.connect(dest)
  osc.start(startTime)
  osc.stop(startTime + duration + 0.05)
}

// Scene-specific ambient patterns
const SCENES = {
  title: {
    // Gentle mysterious pentatonic
    notes: [261.6, 293.7, 329.6, 392, 440, 523.3],
    tempo: 1.2,
    type: 'sine',
    vol: 0.08
  },
  hotel: {
    // Warm, mellow — hotel lobby vibes
    notes: [196, 220, 261.6, 293.7, 329.6],
    tempo: 1.5,
    type: 'sine',
    vol: 0.06
  },
  tuktuk: {
    // Slightly anxious, faster
    notes: [293.7, 329.6, 349.2, 392, 440],
    tempo: 0.8,
    type: 'triangle',
    vol: 0.07
  },
  bbqStall: {
    // Warm with a hint of mystery
    notes: [220, 261.6, 293.7, 329.6, 392],
    tempo: 1.3,
    type: 'sine',
    vol: 0.07
  },
  victory: {
    // Bright, triumphant
    notes: [261.6, 329.6, 392, 440, 523.3],
    tempo: 1.0,
    type: 'sine',
    vol: 0.09
  }
}

function scheduleLoop(sceneName) {
  const config = SCENES[sceneName] || SCENES.title
  if (!isMusicEnabled()) return

  const ctx = getMusicCtx()
  const notes = config.notes
  const beatLen = config.tempo

  // Schedule 8 notes per loop
  const now = ctx.currentTime + 0.1
  for (let i = 0; i < 8; i++) {
    const noteIdx = Math.floor(Math.random() * notes.length)
    const freq = notes[noteIdx]
    const startTime = now + i * beatLen
    playNote(ctx, musicGain, freq, startTime, beatLen * 0.8, config.type, config.vol)
  }

  // Schedule next loop
  const loopDuration = beatLen * 8
  currentLoop = setTimeout(() => {
    if (isPlaying && isMusicEnabled()) {
      scheduleLoop(sceneName)
    }
  }, loopDuration * 1000 - 200) // slight overlap for seamless
}

function startAmbient(sceneName) {
  currentSceneName = sceneName
  if (!isMusicEnabled()) return

  stopAmbient()
  isPlaying = true

  // Small delay to let AudioContext settle
  setTimeout(() => {
    if (isPlaying) scheduleLoop(sceneName)
  }, 100)
}

function stopAmbient() {
  isPlaying = false
  if (currentLoop) {
    clearTimeout(currentLoop)
    currentLoop = null
  }
}

function changeScene(sceneName) {
  if (sceneName === currentSceneName && isPlaying) return
  stopAmbient()
  // Brief fade gap between scenes
  setTimeout(() => {
    startAmbient(sceneName)
  }, 300)
}

export { isMusicEnabled, toggleMusic, startAmbient, stopAmbient, changeScene }