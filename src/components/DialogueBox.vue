<template>
  <div v-if="dialogue" class="fixed bottom-10 left-2 right-2 z-50" @click="dismiss">
    <div class="max-w-lg mx-auto bg-stone-900/95 border-2 border-amber-500 rounded-xl p-4 shadow-2xl backdrop-blur-sm">
      <p class="text-amber-400 font-bold text-sm mb-1">{{ dialogue.speaker }}</p>
      <p class="dialogue-text text-white text-base">{{ dialogue.text }}</p>
      <p class="text-stone-500 text-xs text-right mt-2">tap to continue ▸</p>
    </div>
  </div>
</template>

<script setup>
defineProps({ dialogue: Object })
const emit = defineEmits(['dismiss'])
</script>