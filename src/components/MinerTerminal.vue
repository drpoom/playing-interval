<template>
  <!-- Miner boot terminal overlay -->
  <Transition name="terminal">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80" @click.self="close">
      <div class="w-[90%] max-w-md bg-stone-950 border-2 border-green-500/60 rounded-xl overflow-hidden shadow-2xl shadow-green-500/20">
        <!-- Terminal header -->
        <div class="flex items-center gap-2 px-4 py-2 bg-green-900/30 border-b border-green-500/30">
          <span class="text-green-400 text-xs font-mono">⛏️ MOO YANG MINER 3000 — BOOT SEQUENCE</span>
          <span class="ml-auto text-green-600 text-xs font-mono animate-pulse">● LIVE</span>
        </div>
        <!-- Terminal body -->
        <div class="p-4 font-mono text-xs leading-relaxed h-52 overflow-y-auto" ref="termBody">
          <div v-for="(line, i) in visibleLines" :key="i" class="whitespace-pre-wrap"
               :class="{ 'text-green-400': !line.error, 'text-red-400': line.error, 'text-amber-400': line.warn, 'text-green-300 font-bold': line.success }">
            <span v-if="line.prompt" class="text-green-600">{{ line.prompt }}</span>{{ line.text }}
          </div>
          <span v-if="typing" class="animate-pulse text-green-400">▌</span>
        </div>
        <!-- Terminal footer -->
        <div class="px-4 py-2 bg-green-900/20 border-t border-green-500/30 flex items-center justify-between">
          <span class="text-green-600 text-xs font-mono">{{ progress }}%</span>
          <div class="w-32 h-2 bg-stone-800 rounded-full overflow-hidden">
            <div class="h-full bg-green-500 transition-all duration-300" :style="{ width: progress + '%' }"></div>
          </div>
          <button v-if="complete" class="tap-target text-green-400 font-mono text-xs border border-green-500/40 rounded px-2 py-1 hover:bg-green-900/40"
                  @click="close">
            ✓ COMPLETE
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, nextTick, onUnmounted } from 'vue'
import { sfx } from '../audio.js'

const props = defineProps({ show: Boolean })
const emit = defineEmits(['complete', 'close'])

const termBody = ref(null)
const visibleLines = ref([])
const typing = ref(false)
const progress = ref(0)
const complete = ref(false)

const BOOT_LINES = [
  { prompt: '> ', text: 'Inserting USB device... [GREASY]' },
  { prompt: '> ', text: 'Mounting /dev/usb0 ✓' },
  { prompt: '> ', text: 'Loading MINER3000.BOOT... ✓' },
  { text: '', warn: true, text: '⚠ WARNING: Thermal grease detected on USB contacts' },
  { prompt: '> ', text: 'Initializing ASIC hash cores...' },
  { prompt: '> ', text: 'Core 1: ONLINE ✓' },
  { prompt: '> ', text: 'Core 2: ONLINE ✓' },
  { prompt: '> ', text: 'Core 3: ONLINE ✓' },
  { prompt: '> ', text: 'Core 4: ONLINE ✓' },
  { prompt: '> ', text: 'Configuring Moo Yang Protocol v4.2...' },
  { text: '  ↳ Loading pork-optimized hashing algorithm... ✓' },
  { text: '  ↳ Calibrating grill-to-exhaust thermal bridge... ✓' },
  { prompt: '> ', text: 'Starting mining daemon...' },
  { prompt: '> ', text: 'Connecting to Moo Yang Network... ✓' },
  { text: '', error: true, text: '⚡ Hash rate: 400 TH/s' },
  { prompt: '> ', text: 'Mining address: 0xBEEF...MOOY' },
  { prompt: '> ', text: 'Exhaust temperature: 87°C (optimal for grilling)' },
  { success: true, text: '🟢 MOO YANG PROTOCOL ACTIVATED 🟢' },
  { success: true, text: '🐄⛏️ Miners ONLINE. Mining at 400 TH/s' },
]

let lineIdx = 0
let timerId = null

function startBoot() {
  visibleLines.value = []
  progress.value = 0
  complete.value = false
  lineIdx = 0
  advanceLine()
}

function advanceLine() {
  if (lineIdx >= BOOT_LINES.length) {
    typing.value = false
    complete.value = true
    progress.value = 100
    sfx.success()
    return
  }
  const line = BOOT_LINES[lineIdx]
  typing.value = true
  progress.value = Math.round((lineIdx / BOOT_LINES.length) * 100)

  const delay = line.success ? 600 : line.error ? 400 : 200
  timerId = setTimeout(() => {
    visibleLines.value.push(line)
    typing.value = false
    lineIdx++
    nextTick(() => {
      if (termBody.value) termBody.value.scrollTop = termBody.value.scrollHeight
    })
    advanceLine()
  }, delay)
}

watch(() => props.show, (val) => {
  if (val) startBoot()
})

onUnmounted(() => { if (timerId) clearTimeout(timerId) })

function close() {
  emit('complete')
  emit('close')
}
</script>

<style scoped>
.terminal-enter-active { transition: opacity 0.3s ease; }
.terminal-leave-active { transition: opacity 0.4s ease; }
.terminal-enter-from, .terminal-leave-to { opacity: 0; }
</style>