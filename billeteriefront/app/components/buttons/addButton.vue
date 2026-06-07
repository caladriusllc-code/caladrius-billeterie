<template>
  <div class="add-button-wrapper">
    
    <button 
      class="add-button" 
      :class="{ 'is-active': isOpen }" 
      @click="toggleDropdown"
      aria-label="Ajouter un nouvel élément"
    >
      <span class="btn-text">Nouveau</span>
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24" 
        stroke-width="2" 
        stroke="currentColor" 
        class="plus-icon"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
      </svg>
    </button>

    <Teleport to="body">
      <div v-if="isOpen" class="click-outside-overlay" @click="closeDropdown"></div>
    </Teleport>

    <transition name="dropdown-anim">
      <div v-if="isOpen" class="drop-down">
        <ul class="dropdown-list">
          <li class="dropdown-item" @click="handleAction('Evenement')">
            <svg class="item-icon" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
            </svg>
            Événement
          </li>
          <li class="dropdown-item" @click="handleAction('Billet')">
            <svg class="item-icon" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 0 1 0 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 0 1 0-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375Z" />
            </svg>
            Billet
          </li>
          <li class="dropdown-item" @click="handleAction('Utilisateur')">
            <svg class="item-icon" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
            </svg>
            Utilisateur
          </li>
        </ul>
      </div>
    </transition>
    
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const handleAction = (type) => {
  console.log(`Création d'un nouveau : ${type}`)
  // Ici tu pourras émettre un événement vers ton parent : emit('create', type)
  closeDropdown()
}
</script>

<style scoped>
/* Variables globales (à titre indicatif si tu ne les as pas déjà) */
.add-button-wrapper {
  --primary-color: #ffac13;
  --background-color: #1a1a1a;
  --text-color: #ffffff;
  
  position: relative;
  display: inline-block;
}

/* =========================================
   1. LE BOUTON
   ========================================= */
.add-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.5rem;
  
  background: var(--primary-color);
  color: #000000; /* Toujours noir sur l'orange pour un contraste optimal */
  
  border: none;
  border-radius: 999px; /* Forme pilule parfaite */
  font-size: 1rem;
  font-weight: 600;
  text-transform: capitalize;
  cursor: pointer;
  
  /* Ombre subtile avec la couleur primaire */
  box-shadow: 0 4px 12px rgba(255, 172, 19, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.add-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 172, 19, 0.4);
}

.add-button:active {
  transform: translateY(0);
}

/* L'icône qui tourne */
.plus-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.add-button.is-active .plus-icon {
  transform: rotate(135deg); /* Transforme le "+" en "x" */
}

/* =========================================
   2. LE MENU DÉROULANT
   ========================================= */
.drop-down {
  position: absolute;
  top: calc(100% + 10px); /* Juste en dessous du bouton */
  right: 5px; /* Ou 'right: 0' si tu veux l'aligner à droite */
  min-width: 200px;
  
  background: var(--background-color);
  border: 1px solid #333; /* Bordure discrète */
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  z-index: 100;
}

.dropdown-list {
  list-style: none;
  padding: 0.5rem;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.75rem 1rem;
  
  color: #e5e7eb;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #2a2a2a;
  color: var(--primary-color);
  transform: translateX(4px); /* Petit effet de glissement vers la droite */
}

.item-icon {
  width: 18px;
  height: 18px;
  opacity: 0.8;
}

.dropdown-item:hover .item-icon {
  opacity: 1;
}

/* =========================================
   3. ANIMATIONS & OVERLAY
   ========================================= */
/* Animation d'apparition du menu */
.dropdown-anim-enter-active,
.dropdown-anim-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-anim-enter-from,
.dropdown-anim-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* Overlay invisible pour capturer le clic extérieur */
:global(.click-outside-overlay) {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 99; /* Juste en dessous du z-index 100 du dropdown */
}
</style>