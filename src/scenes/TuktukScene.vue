<template>
  <Transition name="scene" mode="out-in">
    <div v-if="phase === 'riding'" key="riding" class="tuktuk-scene w-full h-full flex flex-col items-center justify-center relative overflow-hidden">

    <!-- Animated road -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="road-lines"></div>
    </div>

    <!-- Tuktuk -->
    <div class="relative z-10 flex flex-col items-center gap-4 p-6 max-w-md w-full">
      <div class="text-7xl animate-bounce" style="animation-duration: 0.6s">🛺</div>
      <h1 class="text-amber-300 text-xl font-bold text-center">Tuk-Tuk to Destiny</h1>
      <p class="text-stone-400 text-sm text-center italic">"The driver has no seatbelt. The vehicle has no suspension. The traffic has no rules. This is... efficient?"</p>

      <!-- Progress bar -->
      <div class="w-full bg-stone-800 rounded-full h-3 mt-4">
        <div class="bg-amber-500 h-3 rounded-full transition-all duration-300" :style="{ width: progress + '%' }"></div>
      </div>

      <!-- Fun facts cycling -->
      <div class="bg-stone-900/80 border border-stone-700 rounded-lg p-3 w-full text-center min-h-[5em] flex items-center justify-center">
        <p class="text-amber-200 text-sm">{{ currentFact }}</p>
      </div>

      <p class="text-stone-500 text-xs">{{ Math.floor(progress) }}% to destination</p>

      <button class="tap-target bg-stone-700 hover:bg-stone-600 active:bg-stone-800 text-stone-300 py-2 px-5 rounded-lg text-xs transition-all"
              @click="skipToArrived">
        ⏩ Skip ride
      </button>
    </div>
  </div>

  <div v-else key="arrived" class="arrived-scene w-full h-full flex flex-col items-center justify-center relative overflow-hidden">
    <div class="absolute inset-0 flex items-center justify-center opacity-10 text-[140px] select-none pointer-events-none">🍖</div>

    <div class="relative z-10 flex flex-col items-center gap-5 p-6 max-w-md w-full">
      <div class="text-6xl">😱💨</div>
      <h1 class="text-amber-300 text-xl font-bold text-center">You have arrived.</h1>
      <p class="text-stone-300 text-sm text-center italic">"The 'business' is a wooden shack with a sign that says<br><strong>Somchai's Crypto-Crackle: Pork at 400 Terahashes.</strong>"</p>
      <p class="text-stone-400 text-xs text-center">Hans's left eye twitches involuntarily.</p>

      <button class="tap-target bg-green-700 hover:bg-green-600 active:bg-green-800 text-white font-bold py-3 px-8 rounded-lg text-base shadow-lg"
              @click="enterStall">
        🍖 Enter the Stall
      </button>
    </div>
  </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

defineProps({ inventory: Array, flags: Object })
const emit = defineEmits(['transition', 'dialogue', 'pickup'])

const phase = ref('riding')
const progress = ref(0)
const factIndex = ref(0)
let intervalId = null

const FACTS = [
  '"The tuktuk driver just overtook a garbage truck on the LEFT. We are in the RIGHT lane. I am mentally drafting a complaint to the Bundesverkehrsministerium."',
  '"The seat cushion appears to be repurposed from a 1987 kitchen chair. I can feel every pothole in my Spine Efficiency Index."',
  '"The driver is simultaneously: driving, eating som tum, watching a Thai soap opera on his phone, and conducting a phone call. Multitasking: 4/10."',
  '"We just passed a temple, a 7-Eleven, and a shop selling both fireworks and massage oil. This country has no zoning laws. It has vibes."',
  '"The exhaust is being channeled directly into the cabin. If I survive this, I am writing a strongly-worded letter to TripAdvisor."',
  '"Fun fact: the tuktuk has more USB ports than the last German train I took. Das ist... surprising."',
  '"The fare meter appears to be a calculator with the number 400 typed in permanent marker."',
  '"I can see the smoke now. Someone is grilling something with Industrial Enthusiasm. The smell is... actually... quite good."',
]

const currentFact = computed(() => FACTS[factIndex.value])

onMounted(() => {
  intervalId = setInterval(() => {
    if (progress.value < 100) {
      progress.value += 2.5
      if (progress.value % 25 < 3) {
        factIndex.value = (factIndex.value + 1) % FACTS.length
      }
    } else {
      clearInterval(intervalId)
      phase.value = 'arrived'
    }
  }, 80)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

function enterStall() {
  emit('transition', { scene: 'bbqStall', newFlags: { tuktukRide: true } })
}

function skipToArrived() {
  if (intervalId) clearInterval(intervalId)
  progress.value = 100
  phase.value = 'arrived'
}
</script>

<script>
export default { name: 'TuktukScene' }
</script>

<style scoped>
.tuktuk-scene {
  background: linear-gradient(180deg, #1e3a5f 0%, #0f172a 50%, #1c1917 100%);
}

.arrived-scene {
  background: linear-gradient(180deg, #7f1d1d 0%, #1c1917 100%);
}

.road-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 40%,
    rgba(255, 255, 255, 0.05) 40%,
    rgba(255, 255, 255, 0.05) 42%
  );
  animation: roadScroll 0.8s linear infinite;
}

@keyframes roadScroll {
  0% { transform: translateY(0); }
  100% { transform: translateY(10%); }
}
</style>