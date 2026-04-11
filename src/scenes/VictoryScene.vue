<template>
  <div class="victory-scene w-full h-full flex flex-col items-center justify-center relative overflow-hidden">

    <!-- Celebration particles -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div v-for="i in 20" :key="i" class="confetti"
        :style="{
          left: (Math.random() * 100) + '%',
          animationDelay: (i * 0.15) + 's',
          animationDuration: (2 + Math.random() * 2) + 's',
          backgroundColor: confettiColors[i % confettiColors.length]
        }">
      </div>
    </div>

    <div class="relative z-10 flex flex-col items-center gap-5 p-6 max-w-md w-full">

      <div class="text-7xl">🎉</div>

      <h1 class="text-3xl font-bold text-amber-300 text-center leading-tight">
        MOO YANG<br>PROTOCOL<br>ACTIVATED!
      </h1>

      <div class="bg-stone-900/80 border-2 border-amber-500 rounded-xl p-5 text-center">
        <p class="text-2xl mb-2">🐄⛏️🍖</p>
        <p class="text-amber-200 text-base leading-relaxed">
          The miners hum to life at <strong>400 TH/s</strong>. The exhaust heat is being channeled directly into the grill.
        </p>
        <p class="text-stone-400 text-sm mt-3 italic">
          "The thermal efficiency of this system is... actually impressive. 
          I would never admit this in Stuttgart, but... this is the most 
          efficient pork-based blockchain operation I have ever seen."
        </p>
        <p class="text-amber-400 text-xs mt-2">— Hans Müller, Chief Efficiency Officer</p>
      </div>

      <div class="bg-green-900/60 border border-green-500/50 rounded-lg px-4 py-2 text-center">
        <p class="text-green-300 font-bold">✅ Prologue Complete!</p>
        <p class="text-green-400 text-xs mt-1">Miners: Online | BBQ: Operational | Moo Yang: Mining</p>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-3 gap-3 w-full text-center">
        <div class="bg-stone-800/80 rounded-lg p-2">
          <p class="text-amber-400 text-lg font-bold">3</p>
          <p class="text-stone-500 text-xs">Scenes</p>
        </div>
        <div class="bg-stone-800/80 rounded-lg p-2">
          <p class="text-amber-400 text-lg font-bold">1</p>
          <p class="text-stone-500 text-xs">Puzzle Solved</p>
        </div>
        <div class="bg-stone-800/80 rounded-lg p-2">
          <p class="text-amber-400 text-lg font-bold">1</p>
          <p class="text-stone-500 text-xs">USB Stick</p>
        </div>
      </div>

      <button class="tap-target bg-amber-600 hover:bg-amber-500 active:bg-amber-700 text-white font-bold py-3 px-8 rounded-xl text-base shadow-lg"
              @click="restartGame">
        🔄 Play Again
      </button>

      <p class="text-stone-600 text-xs text-center">
        To be continued in Chapter 2: "The Hash Rate of Destiny" 🚀
      </p>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['transition'])

const confettiColors = ['#f59e0b', '#ef4444', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#f97316']

function restartGame() {
  emit('transition', { scene: 'title', newFlags: { minersOnline: false }, clearInventory: true })
}
</script>

<script>
export default { name: 'VictoryScene' }
</script>

<style scoped>
.victory-scene {
  background: linear-gradient(180deg, #14532d 0%, #1c1917 50%, #1c1917 100%);
}

.confetti {
  position: absolute;
  top: -10px;
  width: 8px;
  height: 8px;
  border-radius: 2px;
  animation: confettiFall 3s ease-in infinite;
}

@keyframes confettiFall {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}
</style>