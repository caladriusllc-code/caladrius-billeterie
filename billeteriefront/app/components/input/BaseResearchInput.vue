<template>
  <div class="research-wrapper">
    
    <Teleport to="body">
      <transition name="fade">
        <div v-if="isActive" class="glass-overlay" @click="toggleSearch"></div>
      </transition>
    </Teleport>

    <div class="btn-wrapper" :class="{ 'is-elevated': isActive }">
      <button class="research-btn" @click="toggleSearch" aria-label="Ouvrir la recherche">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
      </button>

      <transition name="slide-fade">
        <div v-show="isActive || isDesktop" class="input-container" :class="{ active: isActive }">
          
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="desktop-search-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>

          <input 
            ref="searchInput"
            type="text" 
            v-model="research" 
            placeholder="Rechercher un événement..." 
            class="research-input"
            @keyup.esc="toggleSearch"
          >

          <button v-if="research.length > 0" class="clear-btn" @click="clearSearch" aria-label="Effacer">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'

export default {
  emits: ['input:research'],

  setup(props, { emit }) {
    const research = ref<string>("")
    const isActive = ref<boolean>(false)
    const searchInput = ref<HTMLInputElement | null>(null)
    const isDesktop = ref<boolean>(false)

    // Émettre la valeur à chaque frappe
    watch(research, (newVal) => {
      emit('input:research', newVal)
    })

    // Gérer le redimensionnement pour forcer l'affichage sur desktop
    const checkWidth = () => {
      isDesktop.value = window.innerWidth >= 768
      if (isDesktop.value) isActive.value = false // Reset l'état mobile
    }

    onMounted(() => {
      checkWidth()
      window.addEventListener('resize', checkWidth)
    })

    onUnmounted(() => {
      window.removeEventListener('resize', checkWidth)
    })

    // L'Auto-focus UX
    const toggleSearch = async () => {
      isActive.value = !isActive.value
      if (isActive.value) {
        await nextTick() // On attend que le champ soit dans le DOM
        searchInput.value?.focus() // On ouvre le clavier du mobile directement !
      }
    }

    // Fonction pour la croix "Clear"
    const clearSearch = () => {
      research.value = ""
      searchInput.value?.focus() // On remet le focus après avoir effacé
    }

    return {
      research,
      isActive,
      searchInput,
      isDesktop,
      toggleSearch,
      clearSearch
    }
  }
}
</script>

<style scoped>
/* =========================================
   COMPOSANT DE BASE
   ========================================= */
.btn-wrapper {
  position: relative;
}

.btn-wrapper.is-elevated {
  z-index: 9999;
}

/* Bouton Mobile */
.research-btn {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.5rem;
  background-color: var(--primary-color);
  color: black;
  border: none;
  border-radius: 8px; /* Plus doux */
  cursor: pointer;
  transition: transform 0.2s ease;
}

.research-btn:active {
  transform: scale(0.95); /* Micro-interaction au clic */
}

.size-6 {
  width: 24px;
  height: 24px;
}

/* =========================================
   CHAMP DE RECHERCHE MOBILE
   ========================================= */
.input-container {
  position: absolute;
  top: 60px;
  right: 0;
  width: 280px;
  display: flex;
  align-items: center;
}

.research-input {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem; /* Espace à droite pour la croix */
  border: 1px solid var(--primary-color);
  background-color: var(--tertiary-color, #ffffff); /* Fallback blanc important sur mobile pour contraster avec le fond noir flouté */
  color: var(--primary-color, #1a1a1a);
  border-radius: 12px; /* Coins plus modernes */
  font-size: 1rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); /* Effet d'élévation sur le glassmorphism */
  transition: all 0.3s ease;
}

.research-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(255, 172, 19, 0.2), 0 10px 25px -5px rgba(0, 0, 0, 0.3); /* Halo glowy */
}

.desktop-search-icon {
  display: none; /* Caché sur mobile */
}

/* Croix d'effacement */
.clear-btn {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.clear-btn:hover {
  color: var(--primary-color);
}

.clear-btn svg {
  width: 18px;
  height: 18px;
}

/* =========================================
   ANIMATIONS (VUE TRANSITIONS)
   ========================================= */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-fade-enter-from, .slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* =========================================
   GLASSMORPHISM
   ========================================= */
:global(.glass-overlay) {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 9998;
  cursor: pointer;
}

/* =========================================
   TABLETTE ET DESKTOP (>= 768px)
   ========================================= */
@media (min-width: 768px) {
  
  :global(.glass-overlay) {
    display: none !important;
  }

  .research-btn {
    display: none;
  }

  .input-container {
    position: static; /* Annule l'absolu du mobile */
    width: 300px;
  }

  .research-input {
    padding: 0.7rem 2.5rem 0.7rem 2.5rem; /* Padding GAUCHE pour l'icone, DROITE pour la croix */
    border-radius: 999px; /* Ton design en "Pill" */
    background-color: var(--tertiary-color);
    box-shadow: none; /* Pas d'ombre portée sur desktop sauf au focus */
  }

  .research-input:focus {
    box-shadow: 0 0 0 2px rgba(255, 172, 19, 0.2);
  }

  /* Affichage de la petite loupe dans le champ */
  .desktop-search-icon {
    display: block;
    position: absolute;
    left: 14px;
    width: 20px;
    height: 20px;
    color: var(--primary-color);
    pointer-events: none; /* Pour ne pas bloquer le clic sur l'input */
  }
}
</style>