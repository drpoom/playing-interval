<template>
  <div v-if="dialogue" class="fixed bottom-10 left-2 right-2 z-50" @click="handleClick">
    <div class="max-w-lg mx-auto bg-stone-900/95 border-2 border-amber-500 rounded-xl p-4 shadow-2xl backdrop-blur-sm">
      <div class="flex items-start gap-3">
        <div class="text-3xl shrink-0 mt-0.5">{{ speakerIcon }}</div>
        <div class="flex-1 min-w-0">
          <p class="text-amber-400 font-bold text-sm mb-1">{{ dialogue.speaker }}</p>
          <p class="dialogue-text text-white text-base min-h-[3em]">{{ displayedText }}<span v-if="isTyping" class="animate-pulse">▌</span></p>
        </div>
      </div>
      <p class="text-stone-500 text-xs text-right mt-2">
        {{ isTyping ? 'tap to skip ▸▸' : 'tap to continue ▸' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onUnmounted } from 'vue'
import { sfx } from '../audio.js'

const props = defineProps({ dialogue: Object })
const emit = defineEmits(['dismiss'])

const displayedText = ref('')
const isTyping = ref(false)
let typeTimer = null

const SPEAKER_ICONS = {
  'Hans Müller': '🧔',
  'Hans': '🧔',
  'Hans (Examined)': '🧔',
  'Uncle Somchai': '👨‍🍳',
  'Uncle Somchai (Examined)': '👨‍🍳',
  'System': '⚙️',
}

const speakerIcon = computed(() => SPEAKER_ICONS[props.dialogue?.speaker] || '💬')

watch(() => props.dialogue, (newVal) => {
  if (typeTimer) clearInterval(typeTimer)
  if (newVal && newVal.text) {
    displayedText.value = ''
    isTyping.value = true
    const chars = [...newVal.text]
    let i = 0
    typeTimer = setInterval(() => {
      if (i < chars.length) {
        displayedText.value += chars[i]
        i++
      } else {
        clearInterval(typeTimer)
        typeTimer = null
        isTyping.value = false
      }
    }, 22)
  } else {
    displayedText.value = ''
    isTyping.value = false
  }
})

function handleClick() {
  if (isTyping.value) {
    if (typeTimer) clearInterval(typeTimer)
    typeTimer = null
    displayedText.value = props.dialogue?.text || ''
    isTyping.value = false
  } else {
    sfx.tap()
    emit('dismiss')
  }
}

onUnmounted(() => {
  if (typeTimer) clearInterval(typeTimer)
})
</script>