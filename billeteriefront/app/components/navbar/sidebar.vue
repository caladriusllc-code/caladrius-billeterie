<template>
  <aside class="sidebar" :class="{ 'is-reduced': isReduced }">

    <div class="logo hidden-mobile">
      <span class="logo-text" v-if="!isReduced">Caladrius</span>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6" @click="toggleReduce">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
      </svg>

    </div>

    <nav class="nav-menu">
      <button class="nav-item active">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Accueil</span>
      </button>

        <button class="nav-item">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
          </svg>
            <span class="nav-label" v-if="!isReduced">Analyses</span>
        </button>

        <button class="nav-item">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-12.75h.008v.008H7.5V5.25Zm0 3h.008v.008H7.5v-.008Zm0 3h.008v.008H7.5v-.008Zm0 3h.008v.008H7.5v-.008Z" />
            </svg>
            <span class="nav-label" v-if="!isReduced">Billetterie</span>
        </button>

        <button class="nav-item">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
            </svg>
            <span class="nav-label" v-if="!isReduced">Événements</span>
        </button>

      <button class="nav-item hidden-mobile">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Notifications</span>
      </button>

      <button class="nav-item hidden-mobile">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.43l-1.003.767c-.3.23-.452.617-.432.998.003.074.005.147.005.22s-.002.146-.005.22c-.02.381.13.768.432.998l1.003.767a1.125 1.125 0 0 1 .26 1.43l-1.296 2.247a1.125 1.125 0 0 1-1.37.49l-1.216-.456c-.356-.133-.751-.072-1.076.124a6.57 6.57 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.43l1.004-.767c.301-.23.452-.617.432-.998-.003-.074-.005-.147-.005-.22s.002-.146.005-.22c.02-.381-.13-.768-.432-.998L2.26 9.17a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.49l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Paramètres</span>
      </button>
    </nav>

    <div class="logout hidden-mobile">
      <button class="nav-item">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15M12 9l-3 3m0 0 3 3m-3-3h12.75" />
        </svg>
        <span class="nav-label" v-if="!isReduced">Déconnexion</span>
      </button>
    </div>
  </aside>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
  name: 'Sidebar',
  setup() {
    const isReduced = ref(false);

    const toggleReduce = () => {
      isReduced.value = !isReduced.value;
    };

    return { isReduced, toggleReduce };
  }
}
</script>

<style scoped>
/* =========================================
   1. STRUCTURE MOBILE (Barre en bas)
   ========================================= */
.sidebar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: calc(60px + env(safe-area-inset-bottom));
  background-color: var(--tertiary-color);
  border-top: 1px solid var(--secondary-light-color);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding-bottom: env(safe-area-inset-bottom);
  z-index: 100;
}

.nav-menu {
  display: flex;
  width: 100%;
  justify-content: space-around;
}

.nav-item {
  background: none;
  border: none;
  color: #a0a0a0;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 44px;
  min-height: 44px;
  font-size: 0.75rem;
}

.icon {
  width: 24px;
  height: 24px;
}

.nav-item.active, .nav-item:hover { 
  color: var(--primary-color); 
}

.hidden-mobile { 
  display: none; 
}

/* =========================================
   2. STRUCTURE DESKTOP (À droite, extensible)
   ========================================= */
@media (min-width: 1024px) {
  .hidden-mobile { 
    display: flex; 
  }

  .sidebar {
    position: relative;
    bottom: auto;
    left: auto;
    width: 260px; /* Largeur par défaut déployée */
    height: 100vh;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    padding: 2rem 1rem;
    border-top: none;
    border-left: 1px solid var(--secondary-light-color); /* Séparation côté gauche */
    gap: 2.5rem;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* État Réduit sur Desktop */
  .sidebar.is-reduced {
    width: 85px;
    padding: 2rem 0.5rem;
  }

  /* Bouton Reduce */
  .toggle-btn {
    position: absolute;
    top: 20px;
    left: -15px; /* Chevauche la bordure gauche */
    width: 30px;
    height: 30px;
    background-color: var(--primary-color);
    border: none;
    border-radius: 50%;
    color: var(--background-color);
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    z-index: 105;
    align-items: center;
    justify-content: center;
  }

  .toggle-icon {
    width: 16px;
    height: 16px;
    transition: transform 0.3s ease;
    transform: rotate(180deg); /* Pointe vers la droite par défaut */
  }

  .rotate-icon {
    transform: rotate(0deg); /* Miroir quand réduit */
  }

  /* Alignement Logo */
  .logo {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-left: 0.75rem;
  }
  
  .sidebar.is-reduced .logo {
    justify-content: center;
    padding-left: 0;
  }

  .logo svg{
    color:var(--primary-color)
  }

  .logo:hover svg {
    background: var(--secondary-light-color);
  }

  .logo-icon {
    width: 50px; 
    height: 50px;
    background-color: var(--primary-color);
    color: var(--background-color);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
    flex-shrink: 0;
  }

  .logo-text {
    font-weight: 700;
    font-size: 1.2rem;
    letter-spacing: 0.5px;
  }

  /* Menu vertical & Items */
  .nav-menu {
    flex-direction: column;
    width: 100%;
    gap: 0.75rem;
  }

  .nav-item {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    gap: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: background-color 0.2s ease;
  }

  .nav-item:hover, .nav-item.active {
    background-color: rgba(255, 255, 255, 0.03);
  }

  /* Ajustements en mode réduit */
  .sidebar.is-reduced .nav-item {
    justify-content: center;
    padding: 0.75rem 0;
  }

  .nav-label {
    white-space: nowrap;
    animation: fadeIn 0.2s ease forwards;
  }

  .logout {
    margin-top: auto;
    width: 100%;
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-5px); }
  to { opacity: 1; transform: translateX(0); }
}
</style>