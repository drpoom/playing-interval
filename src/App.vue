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

    <InventoryBar :items="inventory" />

    <footer class="footer-license fixed bottom-0 left-0 right-0 text-center p-1 pointer-events-none">
      Licensed under CC BY-NC-ND 4.0
    </footer>
  </div>
</template>

<script setup>
import { reactive, computed, ref } from 'vue'
import HotelScene from './scenes/HotelScene.vue'
import BBQStallScene from './scenes/BBQStallScene.vue'
import DialogueBox from './components/DialogueBox.vue'
import InventoryBar from './components/InventoryBar.vue'

const SCENES = { hotel: HotelScene, bbqStall: BBQStallScene }

const currentScene = ref('hotel')
const inventory = reactive([])
const flags = reactive({})
const dialogue = ref(null)

const currentSceneComponent = computed(() => SCENES[currentScene.value])

function handleTransition({ scene, newFlags = {} }) {
  Object.assign(flags, newFlags)
  currentScene.value = scene
}

function showDialogue(d) { dialogue.value = d }
function dismissDialogue() { dialogue.value = null }
function pickupItem(item) {
  if (!inventory.includes(item)) inventory.push(item)
}
</script>