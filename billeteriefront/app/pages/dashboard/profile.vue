<template>
  <div class="dashboard-container">
    
    <sidebar />

    <main class="main-content">
        
        <navHead />

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
                        <svg viewBox="0 0 300 100" class="line-chart" preserveAspectRatio="none">
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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import navHead from '../../components/header/navHead.vue';
import sidebar from '../../components/navbar/sidebar.vue';

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
/* =========================================
 1. STYLES DE BASE (MOBILE FIRST)
 ========================================= */

.dashboard-container {
display: flex;
flex-direction: column;
height: 100vh;
background-color: var(--background-color);
color: var(--my-white);
font-family: 'Inter', system-ui, sans-serif;
overflow: hidden;
}

/* Main Content avec gestion Safe Area pour les écrans sans bordures */
.main-content {
flex: 1;
padding: 1rem;
overflow-y: auto;
padding-bottom: calc(80px + env(safe-area-inset-bottom)); 
}

.avatar {
width: 35px;
height: 35px;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
font-size: 0.8rem;
font-weight: bold;
}
.user-avatar { background-color: var(--background-green-color); }

/* Dashboard Grid (Mobile = 1 colonne) */
.dashboard-grid {
display: grid;
grid-template-columns: 1fr;
gap: 1.5rem;
}

.left-column, .right-column {
display: flex;
flex-direction: column;
gap: 1.5rem;
}

/* Stats (Grille fluide automatique) */
.stats-row {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
gap: 1rem;
}

.stat-card {
background-color: var(--tertiary-color);
border: 1px solid var(--secondary-light-color);
border-radius: 12px;
padding: 1rem;
display: flex;
align-items: center;
gap: 1rem;
}

.stat-icon {
width: 40px;
height: 40px;
border-radius: 50%;
background-color: var(--background-color);
display: flex;
align-items: center;
justify-content: center;
font-weight: bold;
border: 1px solid var(--secondary-light-color);
}

.stat-info h3 { font-size: 0.9rem; margin-bottom: 0.2rem; }
.stat-info p { font-size: 0.75rem; color: #a0a0a0; }
.stat-info strong { color: var(--my-white); }

/* Events Section & En-têtes */
.section-header, .widget-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 1rem;
}

.section-header h2, .widget-header h2 { font-size: 1.1rem; }

/* Zones de clic optimisées (44x44px minimum) */
.more-options { 
background: none; 
border: none; 
color: #a0a0a0; 
cursor: pointer; 
min-width: 44px;
min-height: 44px;
display: flex;
align-items: center;
justify-content: center;
}

/* Scroll Horizontal (Swipe) pour les événements sur mobile */
.events-row {
display: flex;
overflow-x: auto;
gap: 1rem;
padding-bottom: 1rem;
scroll-snap-type: x mandatory;
-webkit-overflow-scrolling: touch;
scrollbar-width: none; /* Cache la scrollbar sur Firefox */
}
.events-row::-webkit-scrollbar { display: none; } /* Cache la scrollbar sur Chrome/Safari */

.event-card, .widget {
background-color: var(--tertiary-color);
border: 1px solid var(--secondary-light-color);
border-radius: 12px;
padding: 1rem;
}

.event-card {
min-width: 260px; /* Largeur fixe pour le swipe */
scroll-snap-align: start;
flex-shrink: 0;
}

.event-image {
width: 100%;
height: 120px;
border-radius: 8px;
margin-bottom: 1rem;
}

.event-card h3 { font-size: 0.95rem; margin-bottom: 0.5rem; }
.event-card p { font-size: 0.8rem; color: #a0a0a0; }

.date-badge {
color: var(--primary-color);
font-size: 0.85rem;
font-weight: 600;
margin-bottom: 0.8rem;
}

.attendees { display: flex; margin-top: 1rem; }
.avatar-sm {
width: 25px; height: 25px;
border-radius: 50%;
border: 2px solid var(--tertiary-color);
margin-left: -8px;
}
.avatar-sm:first-child { margin-left: 0; }

/* Widgets */
.notification-item { display: flex; gap: 1rem; margin-bottom: 1rem; }
.notif-content p { font-size: 0.85rem; margin-bottom: 0.3rem; }
.notif-content .time { font-size: 0.7rem; color: #a0a0a0; }

.line-chart { width: 100%; height: 80px; overflow: visible; }
.chart-labels { display: flex; justify-content: space-between; margin-top: 1rem; font-size: 0.7rem; color: #a0a0a0; }
.show-more-btn { 
background: none; 
border: none; 
color: var(--primary-color); 
font-weight: 600; 
display: flex;
align-items: center;
justify-content: center;
margin: 1rem auto 0; 
min-height: 44px; /* Zone de clic optimisée */
cursor: pointer;
}

/* =========================================
 2. STYLES DESKTOP (>= 1024px)
 ========================================= */
@media (min-width: 1024px) {
.dashboard-container {
  flex-direction: row;
}

.main-content {
  padding: 2rem;
  padding-bottom: 2rem; /* Réinitialisation car plus de navbar en bas */
}

/* Grille Principale Desktop (2 colonnes) */
.dashboard-grid {
  grid-template-columns: 2.5fr 1fr;
  gap: 2rem;
}

/* Désactivation du swipe, retour à la grille pour les événements */
.events-row { 
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
  overflow-x: visible;
  padding-bottom: 0;
}

.event-card {
  min-width: auto;
}

.icon-btn {
  background: none; border: none; font-size: 1.2rem; cursor: pointer;
}
}
</style>