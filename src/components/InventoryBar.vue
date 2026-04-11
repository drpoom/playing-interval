<template>
  <div v-if="items.length" class="fixed top-2 left-2 right-2 z-40 flex gap-2 justify-center pointer-events-none">
    <div v-for="item in items" :key="item.id || item.icon"
      class="inv-slot bg-stone-900/90 border border-amber-600/60 rounded-lg px-3 py-1.5 shadow-lg pointer-events-auto flex items-center gap-1.5 cursor-pointer active:scale-95 transition-transform"
      @click="$emit('examine', item)" @contextmenu.prevent="$emit('examine', item)"
      v-longpress="() => $emit('examine', item)">
      <span class="text-xl">{{ item.icon }}</span>
      <span v-if="item.label" class="text-amber-200 text-xs font-medium">{{ item.label }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { vLongpress } from '../directives/longpress.js'
const props = defineProps({ items: Array })
defineEmits(['examine'])
</script>