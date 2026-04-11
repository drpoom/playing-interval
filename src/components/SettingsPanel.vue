<template>
  <Transition name="settings">
    <div v-if="show" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/70" @click.self="$emit('close')">
      <div class="bg-stone-900 border-2 border-amber-500/60 rounded-xl p-5 w-[90%] max-w-sm shadow-2xl">
        <h2 class="text-amber-400 font-bold text-lg mb-4 text-center">⚙️ Settings</h2>

        <div class="flex flex-col gap-3">
          <!-- Sound -->
          <button class="tap-target flex items-center justify-between bg-stone-800 rounded-lg px-4 py-3 border border-stone-700"
                  @click="$emit('toggle-sfx')">
            <span class="text-white text-sm">Sound Effects</span>
            <span class="text-xl">{{ sfxOn ? '🔊' : '🔇' }}</span>
          </button>

          <!-- Music -->
          <button class="tap-target flex items-center justify-between bg-stone-800 rounded-lg px-4 py-3 border border-stone-700"
                  @click="$emit('toggle-music')">
            <span class="text-white text-sm">Music</span>
            <span class="text-xl">{{ musicOn ? '🎵' : '🔕' }}</span>
          </button>

          <!-- Save info -->
          <div class="text-center text-stone-500 text-xs mt-2">
            <p>Progress auto-saves</p>
          </div>

          <!-- New Game -->
          <button class="tap-target bg-red-900/60 hover:bg-red-800/60 active:bg-red-700/60 text-red-300 font-bold py-3 px-4 rounded-lg text-sm border border-red-700/40 mt-2"
                  @click="confirmNewGame = true">
            🔄 New Game
          </button>

          <!-- Confirm new game -->
          <div v-if="confirmNewGame" class="bg-red-950/80 border border-red-500/40 rounded-lg p-3 text-center">
            <p class="text-red-200 text-sm mb-2">Erase save and start over?</p>
            <div class="flex gap-2 justify-center">
              <button class="tap-target bg-red-700 text-white font-bold py-2 px-4 rounded text-sm" @click="$emit('new-game'); confirmNewGame = false">Yes, reset</button>
              <button class="tap-target bg-stone-700 text-stone-300 font-bold py-2 px-4 rounded text-sm" @click="confirmNewGame = false">Cancel</button>
            </div>
          </div>
        </div>

        <button class="tap-target w-full mt-4 bg-stone-800 hover:bg-stone-700 text-stone-300 font-bold py-2 rounded-lg text-sm"
                @click="$emit('close')">
          Close
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ show: Boolean, sfxOn: Boolean, musicOn: Boolean })
defineEmits(['close', 'toggle-sfx', 'toggle-music', 'new-game'])

const confirmNewGame = ref(false)
</script>

<style scoped>
.settings-enter-active { transition: opacity 0.2s ease; }
.settings-leave-active { transition: opacity 0.2s ease; }
.settings-enter-from, .settings-leave-to { opacity: 0; }
</style>