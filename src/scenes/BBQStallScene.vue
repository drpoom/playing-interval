<template>
  <div class="scene bbq-scene w-full h-full flex flex-col items-center justify-center relative overflow-hidden">

    <!-- Background: Night market glow -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute inset-0" style="background: radial-gradient(ellipse at 50% 70%, rgba(220, 50, 20, 0.15) 0%, transparent 60%)
"></div>
    </div>

    <!-- Smoke particles -->
    <div class="smoke-container absolute inset-0 pointer-events-none overflow-hidden">
      <div v-for="i in 5" :key="i" class="smoke-particle" :style="{ animationDelay: (i * 0.8) + 's', left: (35 + i * 6) + '%' }"></div>
    </div>

    <!-- Ember particles -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div v-for="i in 6" :key="'e'+i" class="ember-particle" :style="{ left: (40 + i*4) + '%', animationDelay: (i*0.6) + 's', animationDuration: (2 + i*0.3) + 's' }"></div>
    </div>

    <!-- Content -->
    <div class="relative z-10 flex flex-col items-center gap-3 p-6 max-w-md w-full">

      <h1 class="text-amber-300 text-xl font-bold text-center leading-tight">
        Somchai's Crypto-Crackle
      </h1>
      <p class="text-stone-400 text-sm text-center italic">"Best BBQ & Crypto Mining in Pattaya"</p>

      <!-- Stall Owner -->
      <div class="tap-target text-7xl transition-transform relative"
           @click="talkToOwner" @contextmenu.prevent="examineOwner"
           v-longpress="examineOwner">
        👨‍🍳
        <ActionLabel action="talk" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
      </div>

      <p class="text-amber-200 text-sm italic text-center min-h-[2.5em]">{{ narration }}</p>

      <!-- Interactive items -->
      <div class="flex gap-3 flex-wrap justify-center">
        <div class="tap-target bg-red-900/50 rounded-xl p-3 text-3xl border border-red-700/40 transition-all relative"
             :class="{ 'ring-2 ring-amber-400 opacity-40 cursor-not-allowed': hasUSB, 'hover:bg-red-800/50': !hasUSB }"
             @click="pickupUSB" @contextmenu.prevent="examineUSB"
             v-longpress="examineUSB">
          💾
          <ActionLabel v-if="!hasUSB" action="pickup" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
          <ActionLabel v-else action="examine" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
        <div class="tap-target bg-red-900/50 rounded-xl p-3 text-3xl border border-red-700/40 hover:bg-red-800/50 relative"
             @click="examineGrill" @contextmenu.prevent="examineGrill"
             v-longpress="examineGrill">
          🔥
          <ActionLabel action="examine" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
        <div class="tap-target bg-red-900/50 rounded-xl p-3 text-3xl border border-red-700/40 hover:bg-red-800/50 relative"
             @click="examineSign" @contextmenu.prevent="examineSign"
             v-longpress="examineSign">
          🪧
          <ActionLabel action="examine" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
        <div class="tap-target bg-red-900/50 rounded-xl p-3 text-3xl border border-red-700/40 relative"
             :class="{ 'ring-2 ring-green-400 animate-pulse': hasUSB && !minerInitialized, 'hover:bg-red-800/50': !hasUSB || minerInitialized }"
             @click="examineMiner" @contextmenu.prevent="examineMiner"
             v-longpress="examineMiner">
          ⛏️
          <ActionLabel :action="minerInitialized ? 'examine' : 'use'" class="absolute -bottom-1 left-1/2 -translate-x-1/2" />
        </div>
      </div>

      <MinerTerminal :show="showTerminal" @complete="onTerminalComplete" @close="onTerminalComplete" />

      <!-- USB insertion action -->
      <button v-if="hasUSB && !minerInitialized"
              class="tap-target bg-purple-700 hover:bg-purple-600 active:bg-purple-800 text-white font-bold py-3 px-6 rounded-lg text-base animate-pulse shadow-lg"
              @click="initializeMiner">
        💾 Initialize Miners
      </button>

      <div v-if="minerInitialized"
           class="bg-green-800/80 border border-green-500 rounded-lg px-4 py-2 text-green-300 font-bold text-center">
        ✅ Miners Online! Moo Yang Protocol Activated! 🐄⛏️
      </div>

      <!-- Proceed to victory after miners are online -->
      <button v-if="minerInitialized"
              class="tap-target bg-green-700 hover:bg-green-600 active:bg-green-800 text-white font-bold py-3 px-8 rounded-lg text-base shadow-lg animate-pulse"
              @click="proceedToVictory">
        🎉 Continue →
      </button>

      <!-- Navigation -->
      <div class="flex gap-3 mt-1">
        <button class="tap-target bg-stone-700 hover:bg-stone-600 text-white py-2 px-5 rounded-lg text-sm"
                @click="goBack">
          ← Hotel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ActionLabel from '../components/ActionLabel.vue'
import MinerTerminal from '../components/MinerTerminal.vue'

const props = defineProps({ inventory: Array, flags: Object })
const emit = defineEmits(['transition', 'dialogue', 'pickup'])

const hasVisitedBefore = computed(() => props.flags.visitedBBQ)
const narration = ref('')

function onEnter() {
  if (hasVisitedBefore.value) {
    narration.value = '"Back at Somchai\'s stall. The smoke, the crypto, the pork fat — some things never change."'
  } else {
    narration.value = ''
  }
}
onEnter()
const hasUSB = computed(() => props.inventory.some(i => i.id === 'greasy-usb'))
const minerInitialized = computed(() => props.flags.minersOnline)

function talkToOwner() {
  if (!hasUSB.value) {
    narration.value = '"Welcome welcome! You want BBQ? Very good! Also... I have this USB stick, very greasy, very special. You take, free of charge!" 🤲💾'
  } else if (!minerInitialized.value) {
    narration.value = '"You found the USB! Now plug it into the miner! This is the way!"'
  } else {
    narration.value = '"The miners are running! Moo Yang protocol is GO! 🐄⛏️"'
  }
}

function examineOwner() {
  emit('dialogue', {
    speaker: 'Uncle Somchai (Examined)',
    text: '"A cheerful Thai man with an apron stained in 15 years of BBQ grease. His smile suggests he knows more than he lets on. The words \'Somchai\' and \'Crypto-Crackle\' are embroidered on his hat in Comic Sans."'
  })
}

function examineUSB() {
  if (hasUSB.value) {
    emit('dialogue', { speaker: 'Hans', text: '"A USB stick covered in pork fat. The label reads: MINER 3000 BOOT DISK. The grease-to-data ratio is... concerning."' })
  } else {
    emit('dialogue', { speaker: 'Hans', text: '"A USB stick glistening with what appears to be Moo Yang drippings. The craftsmanship of the label suggests it was printed on a Nokia 3310."' })
  }
}

function pickupUSB() {
  if (!hasUSB.value) {
    emit('pickup', { id: 'greasy-usb', icon: '💾', label: 'Greasy USB' })
    narration.value = '"Acquired: Greasy USB Stick. It smells like Moo Yang. The label says MINER 3000 BOOT DISK." 🤲💾'
  }
}

function examineGrill() {
  emit('dialogue', { speaker: 'Hans', text: '"The grill is working overtime. The aroma of charcoal and pork is overwhelming. Is that... a hash rate display next to the temperature gauge? The thermal efficiency is actually impressive."' })
}

function examineSign() {
  emit('dialogue', { speaker: 'Hans', text: '"The sign reads: MOO YANG MINER 3000 — Best BBQ & Crypto Mining in Pattaya. Below it, in much smaller text: \'Side channels may contain trace amounts of blockchain.\'"' })
}

function examineMiner() {
  if (minerInitialized.value) {
    emit('dialogue', { speaker: 'Hans', text: '"The miner hums contentedly at 400 terahashes per second. Green lights everywhere. It is mining Moo Yang tokens at full capacity, and the exhaust heat is being used to grill pork. This is... actually brilliant thermal engineering."' })
  } else {
    emit('dialogue', { speaker: 'Hans', text: '"A dusty mining rig with a USB port that is screaming for that greasy stick. The cooling system appears to be a bucket of iced tea. INSERT USB TO BEGIN."' })
  }
}

const showTerminal = ref(false)

function initializeMiner() {
  showTerminal.value = true
}

function onTerminalComplete() {
  showTerminal.value = false
  emit('transition', { scene: 'bbqStall', newFlags: { minersOnline: true } })
}

function proceedToVictory() {
  emit('transition', { scene: 'victory', newFlags: {} })
}

function goBack() {
  emit('transition', { scene: 'hotel' })
}
</script>

<script>
export default { name: 'BBQStallScene' }
</script>

<style scoped>
.bbq-scene {
  background: linear-gradient(180deg, #7f1d1d 0%, #451a03 40%, #1c1917 100%);
}

.smoke-particle {
  position: absolute;
  bottom: 40%;
  width: 8px;
  height: 8px;
  background: rgba(200, 200, 200, 0.15);
  border-radius: 50%;
  animation: rise 4s ease-out infinite;
}

.ember-particle {
  position: absolute;
  bottom: 35%;
  width: 3px;
  height: 3px;
  background: #ff6b35;
  border-radius: 50%;
  animation: emberRise 2.5s ease-out infinite;
}

@keyframes rise {
  0% { transform: translateY(0) scale(1); opacity: 0.4; }
  100% { transform: translateY(-200px) scale(4); opacity: 0; }
}

@keyframes emberRise {
  0% { transform: translateY(0); opacity: 0.8; }
  50% { opacity: 0.4; }
  100% { transform: translateY(-80px) translateX(10px); opacity: 0; }
}
</style>