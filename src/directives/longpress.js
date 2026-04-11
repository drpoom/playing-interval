// Long-press directive for mobile "Examine" action
// Minimum 500ms hold triggers the examine callback
export const vLongpress = {
  mounted(el, binding) {
    if (typeof binding.value !== 'function') return

    let timer = null
    let triggered = false

    const start = (e) => {
      triggered = false
      timer = setTimeout(() => {
        triggered = true
        binding.value(e)
      }, 500)
    }

    const cancel = () => {
      if (timer) {
        clearTimeout(timer)
        timer = null
      }
    }

    const end = (e) => {
      cancel()
      // If long-press was triggered, prevent the click event that follows
      if (triggered) {
        e.preventDefault()
      }
    }

    // Prevent context menu on long press (Android)
    const preventContextMenu = (e) => {
      if (triggered) e.preventDefault()
    }

    el.addEventListener('touchstart', start, { passive: true })
    el.addEventListener('touchend', end)
    el.addEventListener('touchmove', cancel, { passive: true })
    el.addEventListener('contextmenu', preventContextMenu)

    el._longpressCleanup = () => {
      el.removeEventListener('touchstart', start)
      el.removeEventListener('touchend', end)
      el.removeEventListener('touchmove', cancel)
      el.removeEventListener('contextmenu', preventContextMenu)
    }
  },
  unmounted(el) {
    if (el._longpressCleanup) el._longpressCleanup()
  }
}