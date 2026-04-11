<template>
  <div class="title-scene w-full h-full flex flex-col items-center justify-center relative overflow-hidden">
    <!-- Animated background particles -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div v-for="i in 12" :key="i" class="float-particle"
        :style="{ left: (i * 8) + '%', animationDelay: (i * 0.7) + 's', fontSize: (16 + i * 2) + 'px' }">
        {{ particles[i % particles.length] }}
      </div>
    </div>

    <div class="relative z-10 flex flex-col items-center gap-6 p-8 max-w-md w-full">
      <div class="text-8xl animate-bounce" style="animation-duration: 2s">🍖</div>

      <div class="text-center">
        <h1 class="text-3xl font-bold text-amber-300 leading-tight">The Secret of<br>Moo Yang</h1>
        <p class="text-stone-500 text-xs mt-2 tracking-widest uppercase">A Point-and-Click Adventure</p>
      </div>

      <div class="bg-stone-900/80 border border-amber-700/50 rounded-lg p-4 text-center">
        <p class="text-amber-200 text-sm italic">"Inheritance is just a fancy word for 'someone else's problems.'"</p>
        <p class="text-stone-500 text-xs mt-1">— Hans Müller, shortly before discovering the truth</p>
      </div>

      <div class="flex flex-col gap-3 w-full max-w-xs">
        <button class="tap-target bg-amber-600 hover:bg-amber-500 active:bg-amber-700 text-white font-bold py-4 px-8 rounded-xl text-lg shadow-lg transition-all"
                @click="startGame">
          🎮 New Game
        </button>

        <button v-if="hasSave" class="tap-target bg-stone-600 hover:bg-stone-500 active:bg-stone-700 text-white font-bold py-3 px-8 rounded-xl text-base transition-all"
                @click="continueGame">
          ▶️ Continue
        </button>

        <button class="tap-target bg-stone-700 hover:bg-stone-600 active:bg-stone-800 text-stone-300 font-bold py-3 px-8 rounded-xl text-sm transition-all"
                @click="showAbout">
          📖 About
        </button>
      </div>

      <div v-if="showingAbout" class="bg-stone-900/90 border border-stone-600 rounded-lg p-4 text-sm text-stone-300 leading-relaxed max-h-60 overflow-y-auto">
        <p class="text-amber-400 font-bold mb-2">How to Play:</p>
        <p><strong>Tap</strong> — Contextual action (talk, pick up, open)</p>
        <p><strong>Long Press / Right-Click</strong> — Examine (Hans's inner monologue)</p>
        <p class="mt-2 text-stone-500 text-xs">Made with Vue 3 + Tailwind CSS. Licensed under CC BY-NC-ND 4.0</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['transition'])

const showingAbout = ref(false)
const hasSave = computed(() => !!localStorage.getItem('mooyang_scene') && localStorage.getItem('mooyang_scene') !== 'title')
const particles = ['🔥', '⛏️', '🐖', '🍖', '💾', '🌶️', '📡', '🛺', '🏨', '📜', '💸', '🐄']

function startGame() {
  localStorage.removeItem('mooyang_scene')
  localStorage.removeItem('mooyang_inventory')
  localStorage.removeItem('mooyang_flags')
  emit('transition', { scene: 'hotel' })
}

function continueGame() {
  const savedScene = localStorage.getItem('mooyang_scene') || 'hotel'
  emit('transition', { scene: savedScene })
}

function showAbout() {
  showingAbout.value = !showingAbout.value
}
</script>

<script>
export default { name: 'TitleScene' }
</script>

<style scoped>
.title-scene {
  background: linear-gradient(180deg, #1c1917 0%, #451a03 50%, #1c1917 100%);
}

.float-particle {
  position: absolute;
  bottom: -20px;
  animation: floatUp 8s ease-in-out infinite;
  opacity: 0.2;
}

@keyframes floatUp {
  0% { transform: translateY(0) rotate(0deg); opacity: 0.2; }
  50% { opacity: 0.4; }
  100% { transform: translateY(-110vh) rotate(360deg); opacity: 0; }
}
</style>