<template>
  <div class="game-root w-full h-full relative overflow-hidden">
    <Transition name="scene" mode="out-in">
      <component :is="currentSceneComponent"
        :inventory="inventory"
        :flags="flags"
        @transition="handleTransition"
        @dialogue="showDialogue"
        @pickup="pickupItem"
      />
    </Transition>

    <DialogueBox v-if="dialogue" :dialogue="dialogue" @dismiss="dismissDialogue" />

    <!-- Toast for item pickups -->
    <Transition name="toast">
      <div v-if="toast" class="fixed top-16 left-1/2 -translate-x-1/2 z-50 bg-amber-600/95 text-white font-bold px-5 py-3 rounded-xl shadow-2xl text-base flex items-center gap-2">
        <span class="text-xl">{{ toast.icon }}</span>
        <span>{{ toast.text }}</span>
      </div>
    </Transition>

    <!-- Examine hint (mobile) -->
    <div v-if="!dialogue && currentScene !== 'title'" class="fixed top-2 right-2 z-30 pointer-events-none">
      <span class="text-stone-600 text-[10px] bg-stone-900/60 rounded px-2 py-1">Long press = Examine</span>
    </div>

    <InventoryBar :items="inventory" />

    <footer class="footer-license fixed bottom-0 left-0 right-0 text-center p-1 pointer-events-none">
      Licensed under CC BY-NC-ND 4.0
    </footer>
  </div>
</template>

<script setup>
import { reactive, computed, ref, watch } from 'vue'
import TitleScene from './scenes/TitleScene.vue'
import HotelScene from './scenes/HotelScene.vue'
import TuktukScene from './scenes/TuktukScene.vue'
import BBQStallScene from './scenes/BBQStallScene.vue'
import VictoryScene from './scenes/VictoryScene.vue'
import DialogueBox from './components/DialogueBox.vue'
import InventoryBar from './components/InventoryBar.vue'

const SCENES = { title: TitleScene, hotel: HotelScene, tuktuk: TuktukScene, bbqStall: BBQStallScene, victory: VictoryScene }

const currentScene = ref(localStorage.getItem('mooyang_scene') || 'title')
const inventory = reactive(JSON.parse(localStorage.getItem('mooyang_inventory') || '[]'))
const flags = reactive(JSON.parse(localStorage.getItem('mooyang_flags') || '{}'))
const dialogue = ref(null)
const toast = ref(null)
let toastTimer = null

const currentSceneComponent = computed(() => SCENES[currentScene.value])

function handleTransition({ scene, newFlags = {}, clearInventory = false }) {
  Object.assign(flags, newFlags)
  if (clearInventory) inventory.length = 0
  currentScene.value = scene
  saveGame()
}

function showDialogue(d) { dialogue.value = d }
function dismissDialogue() { dialogue.value = null }
function pickupItem(item) {
  // Support both string and object format
  const itemObj = typeof item === 'string'
    ? { id: item, icon: item.match(/\p{Emoji_Presentation}/u)?.[0] || '📦', label: item.replace(/\p{Emoji_Presentation}/ug, '').trim() || 'Item' }
    : item
  if (!inventory.some(i => i.id === itemObj.id)) {
    inventory.push(itemObj)
    toast.value = { icon: itemObj.icon, text: 'Got: ' + itemObj.label }
    clearTimeout(toastTimer)
    toastTimer = setTimeout(() => { toast.value = null }, 2200)
    saveGame()
  }
}

function saveGame() {
  localStorage.setItem('mooyang_scene', currentScene.value)
  localStorage.setItem('mooyang_inventory', JSON.stringify([...inventory]))
  localStorage.setItem('mooyang_flags', JSON.stringify({ ...flags }))
}

// Auto-save on changes
watch(currentScene, saveGame)
</script>