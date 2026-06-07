<template>
  <div class="create-module" :class="{ 'is-open': isOpen }">
    
    <Teleport to="body">
      <div v-if="isOpen" class="click-outside-overlay" @click="toggleMenu"></div>
    </Teleport>

    <transition name="menu-anim">
      <div v-if="isOpen" class="menu-options">
        <button 
          v-for="action in creationActions" 
          :key="action.id"
          class="option-box"
          @click="handleAction(action.id)"
        >
          <div class="icon-wrapper">
            <component :is="action.icon" class="action-icon" />
          </div>
          <span class="option-label">{{ action.label }}</span>
        </button>
      </div>
    </transition>

    <button 
      class="action-button" 
      @click="toggleMenu"
      :aria-expanded="isOpen"
      aria-label="Menu de création"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      <span class="label">Créer</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineComponent, h } from 'vue'

const emit = defineEmits(['create'])
const isOpen = ref(false)

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const handleAction = (actionId: string) => {
  emit('create', actionId)
  isOpen.value = false
}

const IconEvent = defineComponent({
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', strokeWidth: '1.5', stroke: 'currentColor' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5m-9-6h.008v.008H12v-.008zM12 15h.008v.008H12V15zm0 2.25h.008v.008H12v-.008zM9.75 15h.008v.008H9.75V15zm0 2.25h.008v.008H9.75v-.008zM7.5 15h.008v.008H7.5V15zm0 2.25h.008v.008H7.5v-.008zm6.75-4.5h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V15zm0 2.25h.008v.008h-.008v-.008zm2.25-4.5h.008v.008H16.5v-.008zm0 2.25h.008v.008H16.5V15z' })
  ])
})

const IconTicket = defineComponent({
  render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', fill: 'none', viewBox: '0 0 24 24', strokeWidth: '1.5', stroke: 'currentColor' }, [
    h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 010 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 010-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375z' })
  ])
})

const creationActions = [
  { id: 'event', label: 'Événement', icon: IconEvent },
  { id: 'ticket', label: 'Billet', icon: IconTicket }
]
</script>

<style scoped>
/* ===========================================================
   0. OVERLAY & WRAPPER
   =========================================================== */
:global(.click-outside-overlay) {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9998;
}

.create-module {
  position: fixed;
  bottom: 68px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  border-radius: 999px;
}

/* ===========================================================
   1. LE MENU DES OPTIONS
   =========================================================== */
.menu-options {
  position: absolute;
  bottom: calc(100% + 16px);
  right: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 180px;
}

.option-box {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 16px;
  background-color: #1a1a1a;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #e5e7eb;
  cursor: pointer;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  transition: all 0.2s ease;
}

.option-box:hover {
  background-color: #2a2a2a;
  border-color: var(--primary-color, #ffac13);
  transform: translateX(-4px);
}

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: var(--primary-color, #ffac13);
}

.action-icon {
  width: 40px;
  height: 40px;
}

.option-label {
  font-size: 0.95rem;
  font-weight: 500;
}

/* ===========================================================
   2. BOUTON PRINCIPAL
   =========================================================== */
.action-button {
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: #000000;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.plus-icon {
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ✅ FIX : taille de l'icône protégée explicitement sur mobile */
@media (max-width: 767px) {
  .plus-icon {
    width: 32px;
    height: 32px;
  }
}

.create-module.is-open .plus-icon {
  transform: rotate(135deg);
}

.label {
  display: none;
}

/* ===========================================================
   3. ANIMATIONS VUE
   =========================================================== */
.menu-anim-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.menu-anim-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.menu-anim-enter-from,
.menu-anim-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

/* ===========================================================
   4. TABLETTE & DESKTOP (>= 768px)
   =========================================================== */
@media (min-width: 768px) {
  .create-module {
    position: relative;
    bottom: auto;
    right: auto;
    align-items: center;
  }

  .action-button {
    width: auto;
    height: auto;
    padding: 0.75rem 1.5rem;
    border-radius: 999px;
    flex-direction: row;
    gap: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .label {
    display: block;
    font-weight: 500;
    color: #000000;
  }

  .plus-icon {
    width: 20px;
    height: 20px;
  }

  .menu-options {
    bottom: auto;
    top: calc(100% + 12px);
    right: 0;
  }

  .menu-anim-enter-from,
  .menu-anim-leave-to {
    transform: translateY(-10px) scale(0.95);
  }
}
</style>