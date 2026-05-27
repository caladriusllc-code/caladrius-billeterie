<template>
  <aside class="sidebar" :class="{ 'expanded': isSidebarExpanded }">
    <div class="sidebar-header hidden-mobile">
      <div class="logo-icon">C</div>
      <h2 class="logo-text" v-if="isSidebarExpanded">Company</h2>
      
      <button class="toggle-btn" v-if="isSidebarExpanded" @click="toggleSidebar">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 20px; height: 20px;">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
        </svg>
      </button>
    </div>
    
    <button class="toggle-btn expand-btn hidden-mobile" v-if="!isSidebarExpanded" @click="toggleSidebar">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 24px; height: 24px;">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
      </svg>
    </button>

    <nav class="nav-menu">
        <button class="nav-item" :class="{ active: activeTab === 'dashboard' }" @click="activeTab = 'dashboard'">
            <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
                </svg>
            </span>
            <span class="nav-text">Dashboard</span>
        </button>
        <button class="nav-item" :class="{ active: activeTab === 'verification' }" @click="activeTab = 'verification'">
            <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
                </svg>
            </span>
            <span class="nav-text">Vérification</span>
        </button>
        <button class="nav-item" :class="{ active: activeTab === 'historique' }" @click="activeTab = 'historique'">
            <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                </svg>
            </span>
            <span class="nav-text">Historique</span>
        </button>
        <button class="nav-item hidden-mobile" :class="{ active: activeTab === 'parametres' }" @click="activeTab = 'parametres'">
            <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 0 1 1.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.559.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.894.149c-.424.07-.764.383-.929.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 0 1-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.398.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 0 1-.12-1.45l.527-.737c.25-.35.272-.806.108-1.204-.165-.397-.506-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.108-1.204l-.526-.738a1.125 1.125 0 0 1 .12-1.45l.773-.773a1.125 1.125 0 0 1 1.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>
            </span>
            <span class="nav-text">Paramètres</span>
        </button>
    </nav>

    <div class="logout hidden-mobile">
        <button class="nav-item">
            <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                </svg>
            </span>
            <span class="nav-text">Déconnexion</span>
        </button>
    </div>
  </aside>
</template>

<script lang="ts">
import { ref } from 'vue';

export default{

    // État local de la sidebar
    setup(){

        const isSidebarExpanded = ref(false);
        const activeTab = ref('dashboard');

        const toggleSidebar = () => {
            isSidebarExpanded.value = !isSidebarExpanded.value;
        };

        return{
            isSidebarExpanded,
            activeTab,
            toggleSidebar
        }

    }

}


</script>

<style scoped>
/* =========================================
   STYLE MOBILE (Fixé en bas)
   ========================================= */
.sidebar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: var(--tertiary-color);
  border-top: 1px solid var(--secondary-light-color);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 100;
}

.hidden-mobile { display: none; }
.nav-text { display: none; } /* On cache le texte sur mobile */

.nav-menu {
  display: flex;
  width: 100%;
  justify-content: space-around;
}

.nav-item {
  background: none;
  border: none;
  font-size: 1.2rem; /* Taille de l'icône sur mobile */
  color: #a0a0a0;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-item.active, .nav-item:hover { color: var(--primary-color); }

/* =========================================
   STYLE DESKTOP (Vertical + Réductible)
   ========================================= */
@media (min-width: 1024px) {
  .hidden-mobile { display: flex; }
  
  .sidebar {
    position: static; /* Reprend sa place dans le flex parent */
    width: 80px;
    height: 100vh;
    flex-direction: column;
    justify-content: flex-start;
    padding: 1.5rem 0;
    border-top: none;
    border-right: 1px solid var(--secondary-light-color);
    transition: width 0.3s ease;
    overflow: hidden;
  }

  .sidebar.expanded { width: 240px; }

  .sidebar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1rem;
    margin-bottom: 2rem;
    height: 40px;
  }

  .logo-icon {
    min-width: 40px;
    height: 40px;
    background-color: var(--primary-color);
    color: var(--background-color);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
  }

  .logo-text {
    font-size: 1.2rem;
    font-weight: bold;
    margin-left: 10px;
    color: var(--my-white);
  }

  .toggle-btn {
    background: none; border: none; color: var(--my-white);
    cursor: pointer; display: flex; align-items: center;
  }

  .expand-btn { margin: 0 auto 2rem auto; }

  .nav-menu {
    flex-direction: column;
    justify-content: flex-start;
    gap: 0.5rem;
    padding: 0 0.5rem;
  }

  .nav-item {
    font-size: 0.95rem;
    justify-content: center;
    padding: 0.8rem;
    width: 100%;
    border-radius: 8px;
    transition: all 0.2s;
  }

  .sidebar.expanded .nav-item {
    justify-content: flex-start;
    padding-left: 1rem;
  }

  .sidebar.expanded .nav-text { display: block; }
  
  .nav-item.active {
    background-color: rgba(242, 248, 100, 0.1);
  }

  .logout {
    margin-top: auto;
    width: 100%;
    padding: 0 0.5rem;
  }
}
</style>