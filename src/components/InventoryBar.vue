<template>
  <div v-if="items.length" class="fixed top-2 left-2 right-2 z-40 flex gap-2 justify-center pointer-events-none">
    <div v-for="item in items" :key="item"
      class="bg-stone-800/90 border border-stone-600 rounded-lg px-3 py-1 text-lg shadow-lg pointer-events-auto">
      {{ item }}
    </div>
  </div>
</template>

<script setup>
defineProps({ items: Array })
</script>