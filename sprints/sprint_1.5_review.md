- **PWA support added** — `manifest.json` with standalone display/portrait orientation, service worker (`sw.js`) for offline caching (cache-first assets, network-first navigation), and iOS/Android meta tags for home screen installation.

- **Full audio system live** — Procedural SFX via `audio.js` (tap, pickup, dialogue, transition, success, examine, error) and per-scene ambient music via `music.js` (pentatonic generative loops), with 🔊/🎵 toggle buttons persisted in localStorage.

- **Complete prologue loop deployed** — Title → Hotel → Tuktuk → BBQ (pick up USB, initialize miner) → Victory, with typewriter dialogue, speaker icons, action labels (Talk/Pick Up/Look/Use), localStorage save/restore, and structured inventory — all at `https://www.drpoom.com/playing-interval/`.