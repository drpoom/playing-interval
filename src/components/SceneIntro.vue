<template>
  <Transition name="scene-intro" mode="out-in">
    <div v-if="show" :key="title" class="fixed inset-0 z-[60] flex flex-col items-center justify-center"
         :style="{ background }">
      <div class="text-center px-8">
        <p v-if="subtitle" class="text-stone-400 text-sm tracking-widest uppercase mb-3">{{ subtitle }}</p>
        <h1 class="text-3xl font-bold text-amber-300 leading-tight">{{ title }}</h1>
        <p v-if="location" class="text-stone-500 text-xs mt-3 italic">{{ location }}</p>
        <div class="mt-4 w-16 h-0.5 bg-amber-600/60 mx-auto"></div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: Boolean,
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  location: { type: String, default: '' },
  background: { type: String, default: 'linear-gradient(180deg, #0a0a1a 0%, #1a1a2e 100%)' },
})
</script>

<style scoped>
.scene-intro-enter-active { transition: opacity 0.6s ease; }
.scene-intro-leave-active { transition: opacity 0.8s ease; }
.scene-intro-enter-from { opacity: 0; }
.scene-intro-leave-to { opacity: 0; }
</style>