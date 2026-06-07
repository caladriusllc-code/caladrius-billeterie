<template>
    <div 
        class="search-container" 
        :class="{ 'is-expanded': isExpanded || !isMobile, 'is-mobile': isMobile }"
        v-click-outside="closeSearch"
    >
        <button 
            v-if="isMobile && !isExpanded" 
            class="search-trigger" 
            @click.stop="expandSearch"
            aria-label="Ouvrir la recherche"
        >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="search-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.604 10.604z" />
            </svg>
        </button>

        <div class="search-input-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="search-icon internal-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.604 10.604z" />
            </svg>
            
            <input
            ref="inputRef"
            type="search"
            class="search-input"
            :value="modelValue"
            @input="handleInput"
            :placeholder="placeholder"
            @focus="$emit('focus')"
            @blur="handleBlur"
            />

            <button v-if="modelValue" class="clear-button" @click="clearSearch" aria-label="Effacer">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="clear-icon">
                    <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                </svg>
            </button>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

export default {
  name: 'SearchInput',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Rechercher...'
    }
  },
  emits: ['update:modelValue', 'focus', 'blur'],
  
  // Directive personnalisée locale pour fermer la recherche si on clique ailleurs
  directives: {
    clickOutside: {
      mounted(el, binding) {
        el.clickOutsideEvent = (event) => {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value();
          }
        };
        document.addEventListener('click', el.clickOutsideEvent);
      },
      unmounted(el) {
        document.removeEventListener('click', el.clickOutsideEvent);
      }
    }
  },

  setup(props, { emit }) {
  const isExpanded = ref(false);
  const inputRef = ref(null);

  // CORRECTION : On détecte tout de suite au lieu de mettre 'false' par défaut
  const isMobile = ref(typeof window !== 'undefined' ? window.innerWidth < 768 : false);

  const checkBreakpoint = () => {
    isMobile.value = window.innerWidth < 768;
    // Si on repasse sur écran large, on réinitialise l'état étendu
    if (!isMobile.value) isExpanded.value = false;
  };

  onMounted(() => {
    // Double vérification par sécurité au montage
    checkBreakpoint();
    window.addEventListener('resize', checkBreakpoint);
  });

  onUnmounted(() => {
    window.removeEventListener('resize', checkBreakpoint);
  });

  const expandSearch = async () => {
    isExpanded.value = true;
    await nextTick();
    inputRef.value?.focus();
  };

  const closeSearch = () => {
    if (!props.modelValue) {
      isExpanded.value = false;
    }
  };

  const handleInput = (event) => {
    emit('update:modelValue', event.target.value);
  };

  const clearSearch = () => {
    emit('update:modelValue', '');
    inputRef.value?.focus();
  };

  return {
    isExpanded,
    isMobile,
    inputRef,
    expandSearch,
    closeSearch,
    handleInput,
    clearSearch
  };
  }
}
</script>

<style scoped>
.search-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  font-family: sans-serif;
  transition: all 0.3s ease;
  width: auto;
}

/* Style de la loupe seule sur Mobile */
.search-trigger {
  background-color: transparent; /* Sécurité : force le fond transparent */
  border: 1px solid #ffac13;
  border-radius: 999px;
  width: 2.8rem;
  height: 2.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #ffac13;
  transition: background-color 0.2s;
}

/* Hover amélioré : un fond légèrement orangé au lieu du gris */
.search-trigger:hover {
  background-color: rgba(255, 172, 19, 0.1); 
}

/* On force la couleur orange spécifiquement pour la loupe du bouton */
.search-trigger .search-icon {
  color: #ffac13;
}

.search-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Wrapper du champ de saisie */
.search-input-wrapper {
  position: relative;
  display: none; /* Caché par défaut sur mobile */
  align-items: center;
  width: 100%;
}

.internal-icon {
  position: absolute;
  left: 1rem;
  color: #ffac13;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.7rem 2.5rem 0.7rem 2.7rem;
  font-size: 1rem;
  border: 1px solid #ffac13;
  border-radius: 1.5rem; /* Reprise du style arrondi du BaseInput */
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.search-input:focus {
  border-color: #ffac13;
  box-shadow: 0 0 0 3px rgba(255, 172, 19, 0.25);
}

.clear-button {
  position: absolute;
  right: 0.8rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 2px;
  display: flex;
}

.clear-icon {
  width: 1.2rem;
  height: 1.2rem;
}

/* --- LOGIQUE RESPONSIVE (MOBILE EXPANDED & TABLETTE+) --- */

/* Quand la loupe est cliquée sur mobile */
.search-container.is-mobile.is-expanded {
  width: 100%;
}

.search-container.is-mobile.is-expanded .search-input-wrapper {
  display: flex;
  animation: fadeIn 0.2s ease-out;
}

/* Rendu naturel sur Tablette et Desktop (>= 768px) */
@media (min-width: 768px) {
  .search-container {
    width: 100%;
    max-width: 400px; /* S'affiche proprement dans une barre d'outils */
  }

  .search-trigger {
    display: none; /* Plus besoin du bouton déclencheur */
  }

  .search-input-wrapper {
    display: flex; /* Toujours visible */
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>