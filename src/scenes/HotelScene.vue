<template>
  <div class="scene hotel-scene w-full h-full flex flex-col items-center justify-center relative overflow-hidden">

    <!-- Background ambience -->
    <div class="absolute inset-0 flex items-center justify-center opacity-10 text-[140px] select-none pointer-events-none">🏨</div>

    <!-- Slow ceiling fan animation -->
    <div class="absolute top-4 right-8 text-4xl opacity-30 animate-spin" style="animation-duration:8s">🌀</div>

    <!-- Content -->
    <div class="relative z-10 flex flex-col items-center gap-4 p-6 max-w-md w-full">

      <!-- Scene title -->
      <h1 class="text-amber-300 text-xl font-bold text-center leading-tight">
        Chapter 1 — The Last Supper of Efficiency
      </h1>
      <p class="text-stone-400 text-sm text-center">5-Star Hotel, Pattaya, Thailand</p>

      <!-- Hans -->
      <div class="tap-target text-8xl transition-transform relative"
           @click="talkToHans" @contextmenu.prevent="examineHans"
           v-longpress="examineHans">
        🧔
        <ActionLabel action="talk" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
      </div>
      <p class="text-amber-200 text-sm italic text-center min-h-[2.5em]">{{ narration }}</p>

      <!-- Interactive items row -->
      <div class="flex gap-3 flex-wrap justify-center">
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all relative"
             @click="examine('minibar')" @contextmenu.prevent="examine('minibar')"
             v-longpress="() => examine('minibar')">
          🍺
          <ActionLabel action="examine" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all relative"
             @click="examine('bed')" @contextmenu.prevent="examine('bed')"
             v-longpress="() => examine('bed')">
          🛏️
          <ActionLabel action="examine" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all relative"
             @click="lookWindow" @contextmenu.prevent="examine('window')"
             v-longpress="() => examine('window')">
          🪟
          <ActionLabel action="examine" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
        <div class="tap-target bg-amber-800/50 rounded-xl p-3 text-3xl border border-amber-700/40 transition-all relative"
             @click="readLetter" @contextmenu.prevent="examine('letter')"
             v-longpress="() => examine('letter')">
          📜
          <ActionLabel action="examine" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
      </div>

      <!-- Exit -->
      <button class="tap-target mt-1 bg-green-700 hover:bg-green-600 active:bg-green-800 text-white font-bold py-3 px-8 rounded-lg text-base shadow-lg"
              @click="goOutside">
        🚪 Go Outside →
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ActionLabel from '../components/ActionLabel.vue'

const props = defineProps({ inventory: Array, flags: Object })
const emit = defineEmits(['transition', 'dialogue', 'pickup'])

const hasLeftBefore = computed(() => props.flags.leftHotel)
const narration = ref(hasLeftBefore.value ? '"Back at the hotel. The minibar still overcharges, the bed still has 14 useless pillows, and the BBQ smell still haunts me."' : '"I came here for a conference... and somehow ended up in Pattaya. The hotel is... adequate."')

const EXAMINES = {
  minibar: '"600 baht for a small Chang beer? Even by Stuttgart standards, that is an affront to the concept of value."',
  bed: '"The bed has 14 decorative pillows. None of them are the correct thickness for actual sleep. This is the Thailand efficiency paradox."',
  window: '"Through the window, the unmistakable aroma of charcoal and grilled pork rises from the street below. Someone is cooking with... passion."',
  letter: '"A letter from Uncle Somchai. It mentions a \'High-Performance Thermal Energy Enterprise\' with \'integrated hardware\' and \'organic supply chains.\' This sounds like a data-center-backed green-energy plant. Finally — something worthy of my expertise."',
}

const REVISIT_EXAMINES = {
  minibar: '"Still 600 baht. The price has not improved. Neither has the beer."',
  bed: '"The 14 decorative pillows mock me. They know I cannot sleep. They have always known."',
  window: '"The BBQ smell persists. It is eternal. Like taxes, but delicious."',
  letter: '"Uncle Somchai\'s letter. I have read it so many times the paper is getting greasy. Wait — that might be from the USB stick."',
}

function talkToHans() {
  if (hasLeftBefore.value) {
    emit('dialogue', { speaker: 'Hans Müller', text: '"I am back. The hotel has not gotten cheaper, the pillows have not gotten useful, and I still smell BBQ. At least I am making progress on Uncle Somchai\'s mystery."' })
  } else {
    emit('dialogue', { speaker: 'Hans Müller', text: '"According to Uncle Somchai\'s letter, I am to inherit a high-performance thermal energy enterprise. He mentions integrated hardware and organic supply chains. It sounds like a data-center-backed green-energy plant. My German heritage demands I bring order to this tropical chaos."' })
  }
}

function examineHans() {
  if (hasLeftBefore.value) {
    emit('dialogue', { speaker: 'Hans (Examined)', text: '"The Hawaiian shirt is now thoroughly wrinkled from the tuktuk ride. His resolve, however, remains perfectly pressed. He smells of SPF 50, street food, and determination."' })
  } else {
    emit('dialogue', { speaker: 'Hans (Examined)', text: '"A distinguished German engineer from Stuttgart. His Hawaiian shirt suggests he has already surrendered to the local climate, if not the local cuisine. He smells faintly of SPF 50 and Sparkling Water (carbonated to exactly 3.5 bar)."' })
  }
}

function examine(id) {
  if (hasLeftBefore.value && REVISIT_EXAMINES[id]) {
    narration.value = REVISIT_EXAMINES[id]
  } else {
    narration.value = EXAMINES[id] || '"Nothing of note. Move along."'
  }
}

function lookWindow() {
  narration.value = '"Through the window, the sweet smell of charcoal and grilled pork wafts up... Is that... a BBQ stall? The efficiency of street-side thermal food processing is... intriguing."'
}

function readLetter() {
  emit('dialogue', { speaker: 'Hans', text: EXAMINES.letter })
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