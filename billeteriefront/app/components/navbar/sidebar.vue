<template>
    <aside class="sidebar">
        <div class="logo hidden-mobile">
            <div class="logo-icon">C</div>
        </div>
        <nav class="nav-menu">
            <button class="nav-item active">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
            </button>
            <button class="nav-item">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
                </svg>
            </button>
            <button class="nav-item">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
                </svg>
            </button>
            <button class="nav-item">📅</button>
            <button class="nav-item hidden-mobile">💬</button>
            <button class="nav-item hidden-mobile">👥</button>
            <button class="nav-item hidden-mobile">⚙️</button>
        </nav>
        <div class="logout hidden-mobile">
            <button class="nav-item">🚪</button>
        </div>
    </aside>
</template>

<script>
export default {

}
</script>

<style scoped>
/* Navigation / Sidebar (Mobile = Barre en bas) */
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

.nav-menu {
  display: flex;
  width: 100%;
  justify-content: space-around;
}

.nav-item {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #a0a0a0;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.nav-item.active, .nav-item:hover { color: var(--primary-color); }

.hidden-mobile { display: none; }
</style>