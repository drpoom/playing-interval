<template>
  <div class="scene hotel-scene w-full h-full flex flex-col items-center justify-center relative overflow-hidden">

    <!-- Background ambience -->
    <div class="absolute inset-0 flex items-center justify-center opacity-10 text-[140px] select-none pointer-events-none">🏨</div>

    <!-- Slow ceiling fan animation -->
    <div class="absolute top-4 right-8 text-4xl opacity-30 animate-spin" style="animation-duration:8s">🌀</div>

    <!-- Content -->
    <div class="relative z-10 flex flex-col items-center gap-5 p-6 max-w-md w-full">

      <!-- Scene title -->
      <h1 class="text-amber-300 text-xl font-bold text-center leading-tight">
        Chapter 1 — The Last Supper of Efficiency
      </h1>
      <p class="text-stone-400 text-sm text-center">5-Star Hotel, Pattaya, Thailand</p>

      <!-- Hans -->
      <div class="tap-target text-8xl transition-transform"
           @click="talkToHans" @contextmenu.prevent="examineHans"
           v-longpress="examineHans">🧔
      </div>
      <p class="text-amber-200 text-sm italic text-center">{{ narration }}</p>

      <!-- Interactive items row -->
      <div class="flex gap-3 flex-wrap justify-center">
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all"
             :class="{ 'ring-2 ring-amber-400': hovered === 'minibar' }"
             @click="examine('minibar')" @contextmenu.prevent="examine('minibar')"
             @pointerenter="hovered='minibar'" @pointerleave="hovered=''">
          🍺
        </div>
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all"
             :class="{ 'ring-2 ring-amber-400': hovered === 'bed' }"
             @click="examine('bed')" @contextmenu.prevent="examine('bed')"
             @pointerenter="hovered='bed'" @pointerleave="hovered=''">
          🛏️
        </div>
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all"
             :class="{ 'ring-2 ring-amber-400': hovered === 'window' }"
             @click="lookWindow" @contextmenu.prevent="examine('window')"
             @pointerenter="hovered='window'" @pointerleave="hovered=''">
          🪟
        </div>
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all"
             :class="{ 'ring-2 ring-amber-400': hovered === 'letter' }"
             @click="examine('letter')" @contextmenu.prevent="examine('letter')"
             @pointerenter="hovered='letter'" @pointerleave="hovered=''">
          📜
        </div>
      </div>

      <!-- Exit -->
      <button class="tap-target mt-2 bg-green-700 hover:bg-green-600 active:bg-green-800 text-white font-bold py-3 px-8 rounded-lg text-base shadow-lg"
              @click="goOutside">
        🚪 Go Outside →
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ inventory: Array, flags: Object })
const emit = defineEmits(['transition', 'dialogue', 'pickup'])

const narration = ref('"I came here for a conference... and somehow ended up in Pattaya. The hotel is... adequate."')
const hovered = ref('')

const EXAMINES = {
  minibar: '"600 baht for a small Chang beer? Even by Stuttgart standards, that is an affront to the concept of value."',
  bed: '"The bed has 14 decorative pillows. None of them are the correct thickness for actual sleep. This is the Thailand efficiency paradox."',
  window: '"Through the window, the unmistakable aroma of charcoal and grilled pork rises from the street below. Someone is cooking with... passion."',
  letter: '"A letter from Uncle Somchai. It mentions a \'High-Performance Thermal Energy Enterprise\' with \'integrated hardware\' and \'organic supply chains.\' This sounds like a data-center-backed green-energy plant. Finally — something worthy of my expertise."',
}

function talkToHans() {
  emit('dialogue', {
    speaker: 'Hans Müller',
    text: '"According to Uncle Somchai\'s letter, I am to inherit a high-performance thermal energy enterprise. He mentions integrated hardware and organic supply chains. It sounds like a data-center-backed green-energy plant. My German heritage demands I bring order to this tropical chaos."'
  })
}

function examineHans() {
  emit('dialogue', {
    speaker: 'Hans (Examined)',
    text: '"A distinguished German engineer from Stuttgart. His Hawaiian shirt suggests he has already surrendered to the local climate, if not the local cuisine. He smells faintly of SPF 50 and Sparkling Water (carbonated to exactly 3.5 bar)."'
  })
}

function examine(id) {
  narration.value = EXAMINES[id] || '"Nothing of note. Move along."'
}

function lookWindow() {
  narration.value = '"Through the window, the sweet smell of charcoal and grilled pork wafts up... Is that... a BBQ stall? The efficiency of street-side thermal food processing is... intriguing."'
}

function goOutside() {
  emit('transition', { scene: 'tuktuk', newFlags: { leftHotel: true } })
}
</script>

<script>
export default { name: 'HotelScene' }
</script>

<style scoped>
.hotel-scene {
  background: linear-gradient(180deg, #78350f 0%, #451a03 50%, #1c1917 100%);
}
</style>