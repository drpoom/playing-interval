<template>
  <div v-if="items.length" class="fixed top-2 left-2 right-2 z-40 flex gap-2 justify-center pointer-events-none">
    <div v-for="item in items" :key="item.id || item.icon"
      class="inv-slot bg-stone-900/90 border border-amber-600/60 rounded-lg px-3 py-1.5 shadow-lg pointer-events-auto flex items-center gap-1.5">
      <span class="text-xl">{{ item.icon }}</span>
      <span v-if="item.label" class="text-amber-200 text-xs font-medium">{{ item.label }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ items: Array })
</script>