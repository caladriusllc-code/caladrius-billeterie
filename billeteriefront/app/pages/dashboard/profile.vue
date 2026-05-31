<template>
    <div class="dashboard-container">
    
        <main class="main-content">
            <header class="top-header">
                <div class="mobile-header-top">
                    <h1>Dashboard</h1>
                    <div class="user-profile">
                    <div class="avatar user-avatar">MS</div>
                    </div>
                </div>

                <div class="header-actions">
                    <div class="search-bar">
                    <span>🔍</span>
                    <input type="text" placeholder="Search event..." />
                    </div>
                    <button class="btn-primary" @click="router.push('/event/addEvent')">+ Add Event</button>
                    <button class="icon-btn hidden-mobile">🔔</button>
                </div>
            </header>

            <div class="dashboard-grid">
            
                <div class="left-column">
                    
                    <div class="stats-row">
                    <div class="stat-card" v-for="(stat, index) in stats" :key="index">
                        <div class="stat-icon" :style="{ color: stat.color }">{{ stat.initials }}</div>
                        <div class="stat-info">
                        <h3>{{ stat.title }}</h3>
                        <p>Capacity : <strong>{{ stat.current }}</strong>/{{ stat.total }} Tickets</p>
                        </div>
                    </div>
                    </div>

                    <section class="events-section">
                    <div class="section-header">
                        <h2>Ongoing Event</h2>
                        <button class="more-options">•••</button>
                    </div>
                    <div class="events-row">
                        <div class="event-card" v-for="(event, index) in ongoingEvents" :key="index">
                        <div class="event-image" :style="{ background: event.bg }"></div>
                        <h3>{{ event.title }}</h3>
                        <p>🕒 {{ event.time }}</p>
                        </div>
                    </div>
                    </section>

                    <section class="events-section">
                    <div class="section-header">
                        <h2>Upcoming Event</h2>
                        <button class="more-options">•••</button>
                    </div>
                    <div class="events-row upcoming-row">
                        <div class="event-card upcoming-card" v-for="(event, index) in upcomingEvents" :key="index">
                        <div class="date-badge">{{ event.date }}</div>
                        <h3>{{ event.title }}</h3>
                        <p>🕒 {{ event.time }}</p>
                        <div class="attendees">
                            <div class="avatar-sm" style="background: #e74c3c;"></div>
                            <div class="avatar-sm" style="background: #3498db;"></div>
                            <div class="avatar-sm" style="background: #2ecc71;"></div>
                            <div class="avatar-sm" style="background: #f1c40f;"></div>
                        </div>
                        </div>
                    </div>
                    </section>

                </div>

                <div class="right-column">
                    
                    <aside class="widget notifications-widget">
                        <div class="widget-header">
                            <h2>Notification</h2>
                            <button class="more-options">•••</button>
                        </div>
                        <div class="notification-list">
                            <div class="notification-item" v-for="(notif, index) in notifications" :key="index">
                            <div class="avatar-sm" style="background: #95a5a6;"></div>
                            <div class="notif-content">
                                <p><strong>{{ notif.name }}</strong> has bought <span :style="{ color: notif.highlightColor }">{{ notif.action }}</span></p>
                                <span class="time">{{ notif.time }}</span>
                            </div>
                            </div>
                        </div>
                    </aside>

                    <aside class="widget chart-widget">
                        <div class="widget-header">
                            <h2>Ticket Selling</h2>
                            <button class="more-options">•••</button>
                        </div>
                        <div class="chart-container">
                            <svg viewBox="0 0 300 100" class="line-chart">
                            <path d="M 0 80 Q 20 50, 40 60 T 80 40 T 120 70 T 160 30 T 200 40 T 240 20 T 300 10" 
                                fill="none" stroke="var(--primary-color)" stroke-width="3" stroke-linecap="round"/>
                            </svg>
                            <div class="chart-labels">
                            <span>06.00</span>
                            <span>07.00</span>
                            <span>08.00</span>
                            <span>09.00</span>
                            </div>
                        </div>
                        <button class="show-more-btn">Show More ></button>
                    </aside>

                </div>
            </div>
        </main>

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
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const stats = ref([
  { initials: 'EC', title: 'Economy Class', current: 128, total: 240, color: '#3498db' },
  { initials: 'MC', title: 'Master Class', current: 80, total: 150, color: 'var(--primary-color)' },
  { initials: 'BC', title: 'Business Class', current: 64, total: 120, color: 'var(--background-green-color)' }
]);

const ongoingEvents = ref([
  { title: 'Justin Bieber Concert', time: '30 Mar 2026, 07:30 PM', bg: 'linear-gradient(45deg, #1a2a6c, #b21f1f, #fdbb2d)' },
  { title: 'Tony Quefara Concert', time: '30 Mar 2026, 08:00 PM', bg: 'linear-gradient(45deg, #000000, #434343)' },
  { title: 'Charlie Puth Concert', time: '30 Mar 2026, 08:30 PM', bg: 'linear-gradient(45deg, #4b6cb7, #182848)' },
  { title: 'Firework Concert Fest', time: '30 Mar 2026, 09:00 PM', bg: 'linear-gradient(45deg, #ff416c, #ff4b2b)' }
]);

const upcomingEvents = ref([
  { date: '27 Apr 2026', title: 'Doel Sumbang Concert', time: '10:00 PM - 11.30 PM' },
  { date: '28 Apr 2026', title: 'Air Baloon Festival', time: '08:00 AM - 10.00 AM' },
  { date: '29 Apr 2026', title: 'Global Firework Fest', time: '08:30 PM - 11.30 PM' },
  { date: '30 Apr 2026', title: 'Selena Gomez Concert', time: '09:00 PM - 10.30 PM' }
]);

const notifications = ref([
  { name: 'Roberto Ahman', action: '3 economy class', time: '2 minute ago', highlightColor: '#3498db' },
  { name: 'Greysia Polii', action: '2 master class', time: '3 minute ago', highlightColor: 'var(--primary-color)' },
  { name: 'Stephanie Angelina', action: '2 business class', time: '3 minute ago', highlightColor: 'var(--background-green-color)' }
]);
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Base Layout */
.dashboard-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--background-color);
  color: var(--my-white);
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden;
}

.main-content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  padding-bottom: 80px;
}

/* Header mis à jour */
.top-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 1.5rem; 
  width: 100%;
}
.header-title h1 { font-size: 1.5rem; font-weight: 700; }
.header-actions { display: flex; align-items: center; gap: 1rem; }

.search-bar { display: flex; align-items: center; background-color: var(--tertiary-color); border: 1px solid var(--secondary-light-color); border-radius: 8px; padding: 0.5rem; flex: 1; min-width: 200px; }
.search-bar input { background: none; border: none; color: var(--my-white); outline: none; margin-left: 0.5rem; width: 100%; }
.btn-primary { background-color: var(--primary-color); color: var(--background-color); border: none; border-radius: 8px; padding: 0.6rem 1rem; font-weight: 600; cursor: pointer; flex-shrink: 0; width: 100%; }
.avatar { width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: bold; }
.user-avatar { background-color: var(--background-green-color); }

/* Dashboard Grid */
.dashboard-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
.left-column, .right-column { display: flex; flex-direction: column; gap: 1.5rem; }
.stats-row { display: grid; grid-template-columns: 1fr; gap: 1rem; }

/* Cards & Widgets */
.stat-card, .event-card, .widget { background-color: var(--tertiary-color); border: 1px solid var(--secondary-light-color); border-radius: 12px; padding: 1rem; }
.stat-card { display: flex; align-items: center; gap: 1rem; }
.stat-icon { width: 40px; height: 40px; border-radius: 50%; background-color: var(--background-color); display: flex; align-items: center; justify-content: center; font-weight: bold; border: 1px solid var(--secondary-light-color); }
.stat-info h3 { font-size: 0.9rem; margin-bottom: 0.2rem; }
.stat-info p { font-size: 0.75rem; color: #a0a0a0; }
.stat-info strong { color: var(--my-white); }

.section-header, .widget-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.section-header h2, .widget-header h2 { font-size: 1.1rem; }
.more-options { background: none; border: none; color: #a0a0a0; cursor: pointer; }

.events-row { display: grid; grid-template-columns: 1fr; gap: 1rem; }
.event-image { width: 100%; height: 120px; border-radius: 8px; margin-bottom: 1rem; }
.event-card h3 { font-size: 0.95rem; margin-bottom: 0.5rem; }
.event-card p { font-size: 0.8rem; color: #a0a0a0; }
.date-badge { color: var(--primary-color); font-size: 0.85rem; font-weight: 600; margin-bottom: 0.8rem; }

.attendees { display: flex; margin-top: 1rem; }
.avatar-sm { width: 25px; height: 25px; border-radius: 50%; border: 2px solid var(--tertiary-color); margin-left: -8px; }
.avatar-sm:first-child { margin-left: 0; }

.notification-item { display: flex; gap: 1rem; margin-bottom: 1rem; }
.notif-content p { font-size: 0.85rem; margin-bottom: 0.3rem; }
.notif-content .time { font-size: 0.7rem; color: #a0a0a0; }

.line-chart { width: 100%; height: 80px; overflow: visible; }
.chart-labels { display: flex; justify-content: space-between; margin-top: 1rem; font-size: 0.7rem; color: #a0a0a0; }
.show-more-btn { background: none; border: none; color: var(--primary-color); font-weight: 600; display: block; margin: 1rem auto 0; }

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

/* Tablette (1 colonne sur la grille principale conservée) */
@media (min-width: 768px) {
  .stats-row { grid-template-columns: repeat(3, 1fr); }
  .events-row { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop (2 colonnes) */
@media (min-width: 1024px) {
  .dashboard-container { flex-direction: row; }
  .main-content { padding: 2rem; padding-bottom: 2rem; }
  .hidden-mobile { display: block; } /* Modifié pour le bouton icon-btn */
  .top-header h1 { font-size: 1.8rem; }
  
  /* Grille à 2 colonnes confirmée */
  .dashboard-grid { grid-template-columns: 2.5fr 1fr; gap: 2rem; }
  .events-row { grid-template-columns: repeat(4, 1fr); }
  .icon-btn { background: none; border: none; font-size: 1.2rem; cursor: pointer; color: var(--my-white); display: flex; align-items: center; justify-content: center; }
  .icon-btn svg { width: 24px; height: 24px; }
}
</style>