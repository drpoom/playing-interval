<template>
  <div v-if="dialogue" class="fixed bottom-10 left-2 right-2 z-50" @click="handleClick">
    <div class="max-w-lg mx-auto bg-stone-900/95 border-2 border-amber-500 rounded-xl p-4 shadow-2xl backdrop-blur-sm">
      <p class="text-amber-400 font-bold text-sm mb-1">{{ dialogue.speaker }}</p>
      <p class="dialogue-text text-white text-base min-h-[3em]">{{ displayedText }}<span v-if="isTyping" class="animate-pulse">▌</span></p>
      <p class="text-stone-500 text-xs text-right mt-2">
        {{ isTyping ? 'tap to skip ▸▸' : 'tap to continue ▸' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({ dialogue: Object })
const emit = defineEmits(['dismiss'])

const displayedText = ref('')
const isTyping = ref(false)
let typeTimer = null

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
    }, 22) // ~45 chars/sec
  } else {
    displayedText.value = ''
    isTyping.value = false
  }
})

function handleClick() {
  if (isTyping.value) {
    // Skip to full text
    if (typeTimer) clearInterval(typeTimer)
    typeTimer = null
    displayedText.value = props.dialogue?.text || ''
    isTyping.value = false
  } else {
    emit('dismiss')
  }
}

onUnmounted(() => {
  if (typeTimer) clearInterval(typeTimer)
})
</script>