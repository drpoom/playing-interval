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

    <SceneIntro :show="introShow" :title="introTitle" :subtitle="introSubtitle" :location="introLocation" :background="introBg" />

    <!-- Toast for item pickups -->
    <Transition name="toast">
      <div v-if="toast" class="fixed top-16 left-1/2 -translate-x-1/2 z-50 bg-amber-600/95 text-white font-bold px-5 py-3 rounded-xl shadow-2xl text-base flex items-center gap-2">
        <span class="text-xl">{{ toast.icon }}</span>
        <span>{{ toast.text }}</span>
      </div>
    </Transition>

    <!-- Settings gear button -->
    <button v-if="currentScene !== 'title'" class="fixed top-2 right-2 z-30 tap-target text-lg bg-stone-900/70 rounded-full w-9 h-9 flex items-center justify-center"
            @click="showSettings = !showSettings">
      ⚙️
    </button>
    <SettingsPanel :show="showSettings" :sfx-on="soundOn" :music-on="musicOn"
      @close="showSettings = false"
      @toggle-sfx="toggleSfx"
      @toggle-music="toggleBgm"
      @new-game="restartGame" />

    <InventoryBar :items="inventory" @examine="examineItem" />

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
import SceneIntro from './components/SceneIntro.vue'
import SettingsPanel from './components/SettingsPanel.vue'
import { sfx, isSoundEnabled, toggleSound } from './audio.js'
import { isMusicEnabled, toggleMusic, changeScene } from './music.js'

const SCENES = { title: TitleScene, hotel: HotelScene, tuktuk: TuktukScene, bbqStall: BBQStallScene, victory: VictoryScene }

const currentScene = ref(localStorage.getItem('mooyang_scene') || 'title')
const inventory = reactive(JSON.parse(localStorage.getItem('mooyang_inventory') || '[]'))
const flags = reactive(JSON.parse(localStorage.getItem('mooyang_flags') || '{}'))
const dialogue = ref(null)
const toast = ref(null)
const soundOn = ref(isSoundEnabled())
const musicOn = ref(isMusicEnabled())
const showSettings = ref(false)
let toastTimer = null

const introShow = ref(false)
const introTitle = ref('')
const introSubtitle = ref('')
const introLocation = ref('')
const introBg = ref('')

const SCENE_INTROS = {
  hotel: { title: 'Chapter 1', subtitle: 'The Last Supper of Efficiency', location: '5-Star Hotel, Pattaya, Thailand', bg: 'linear-gradient(180deg, #78350f 0%, #1c1917 100%)' },
  tuktuk: { title: 'Tuk-Tuk to Destiny', subtitle: '', location: 'Pattaya Ring Road', bg: 'linear-gradient(180deg, #1e3a5f 0%, #0f172a 100%)' },
  bbqStall: { title: "Somchai's Crypto-Crackle", subtitle: '"Best BBQ & Crypto Mining in Pattaya"', location: 'Street Food District', bg: 'linear-gradient(180deg, #7f1d1d 0%, #1c1917 100%)' },
  victory: { title: 'MOO YANG PROTOCOL', subtitle: 'ACTIVATED', location: '', bg: 'linear-gradient(180deg, #14532d 0%, #1c1917 100%)' },
}

function showIntro(scene) {
  const intro = SCENE_INTROS[scene]
  if (!intro) return
  introTitle.value = intro.title
  introSubtitle.value = intro.subtitle
  introLocation.value = intro.location
  introBg.value = intro.bg
  introShow.value = true
  setTimeout(() => { introShow.value = false }, 2200)
}

const currentSceneComponent = computed(() => SCENES[currentScene.value])

function handleTransition({ scene, newFlags = {}, clearInventory = false }) {
  sfx.transition()
  const extraFlags = {}
  if (scene === 'bbqStall') extraFlags.visitedBBQ = true
  Object.assign(flags, newFlags, extraFlags)
  if (clearInventory) inventory.length = 0
  currentScene.value = scene
  changeScene(scene)
  showIntro(scene)
  saveGame()
}

function showDialogue(d) { sfx.dialogue(); dialogue.value = d }
function dismissDialogue() { dialogue.value = null }
function toggleSfx() { soundOn.value = toggleSound(); sfx.tap() }
function toggleBgm() { musicOn.value = toggleMusic() }
function restartGame() {
  showSettings.value = false
  handleTransition({ scene: 'title', newFlags: { minersOnline: false }, clearInventory: true })
}

const ITEM_EXAMINES = {
  'greasy-usb': { speaker: 'Hans', text: '"A USB stick covered in pork fat. The label reads: MINER 3000 BOOT DISK. The grease-to-data ratio is... concerning."' },
}
function examineItem(item) {
  sfx.examine()
  const desc = ITEM_EXAMINES[item.id]
  if (desc) {
    showDialogue(desc)
  } else {
    showDialogue({ speaker: 'Hans', text: `"${item.icon} ${item.label}. I should probably find a use for this."` })
  }
}
function pickupItem(item) {
  // Support both string and object format
  const itemObj = typeof item === 'string'
    ? { id: item, icon: item.match(/\p{Emoji_Presentation}/u)?.[0] || '📦', label: item.replace(/\p{Emoji_Presentation}/ug, '').trim() || 'Item' }
    : item
  if (!inventory.some(i => i.id === itemObj.id)) {
    inventory.push(itemObj)
    sfx.pickup()
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