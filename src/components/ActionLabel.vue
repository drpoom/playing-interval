<template>
  <span class="action-label text-[10px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded"
    :class="colorClass">{{ text }}</span>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ action: { type: String, default: 'examine' } })

const ACTION_MAP = {
  talk: { text: 'Talk', color: 'bg-blue-700/80 text-blue-100' },
  pickup: { text: 'Pick Up', color: 'bg-amber-600/80 text-amber-100' },
  examine: { text: 'Look', color: 'bg-stone-600/80 text-stone-200' },
  use: { text: 'Use', color: 'bg-purple-700/80 text-purple-100' },
  open: { text: 'Open', color: 'bg-green-700/80 text-green-100' },
  go: { text: 'Go', color: 'bg-green-700/80 text-green-100' },
}

const text = computed(() => (ACTION_MAP[props.action] || ACTION_MAP.examine).text)
const colorClass = computed(() => (ACTION_MAP[props.action] || ACTION_MAP.examine).color)
</script>

<style scoped>
.action-label { line-height: 1.2; white-space: nowrap; }
</style>