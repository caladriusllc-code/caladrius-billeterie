<template>
  <div class="create-event-container">
    <header class="top-nav">
      <div class="logo">
        <span class="logo-icon">C</span>
        <span class="logo-text">Calevent</span>
      </div>
      <div class="nav-actions">
        <button class="nav-btn hidden-mobile">🌐</button>
        <button class="nav-btn">🔔</button>
        <div class="user-profile">
          <div class="avatar">MS</div>
          <span class="hidden-mobile">Maria Soniatha</span>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="creation-card">
        
        <div class="form-panel">
          
          <div class="organizer-info">
            <span class="label">Create Under</span>
            <div class="organizer-select">
              <div class="avatar-sm">MS</div>
              <span>Maria Soniatha ⌄</span>
            </div>
          </div>

          <input 
            type="text" 
            class="event-name-input" 
            placeholder="Event Name" 
            v-model="eventData.name"
          />

          <div class="form-group date-time-group">
            <div class="date-badge">
              <span class="month">DEC</span>
              <span class="day">25</span>
            </div>
            <div class="date-inputs">
              <div class="input-row">
                <span class="row-label">Start</span>
                <input type="date" v-model="eventData.startDate" />
                <input type="time" v-model="eventData.startTime" />
              </div>
              <div class="input-row">
                <span class="row-label">End</span>
                <input type="date" v-model="eventData.endDate" />
                <input type="time" v-model="eventData.endTime" />
              </div>
              <div class="input-row timezone-row">
                <span>🌐 GMT +00:00 Abidjan</span>
              </div>
            </div>
          </div>

          <div class="form-group location-group">
            <div class="icon-col">📌</div>
            <div class="input-col">
              <input type="text" placeholder="Add Event Location" v-model="eventData.location" />
              <span class="sub-label">Online or Offline Event</span>
            </div>
          </div>

          <div class="form-group settings-group">
            <div class="icon-col">⚙️</div>
            <div class="settings-list">
              
              <div class="setting-row">
                <div class="setting-label">🎟️ Tickets</div>
                <div class="setting-value">Free ✎</div>
              </div>
              
              <div class="setting-row">
                <div class="setting-label">👤 Require Approval</div>
                <div class="setting-value">
                  <label class="switch">
                    <input type="checkbox" v-model="eventData.requireApproval">
                    <span class="slider round"></span>
                  </label>
                </div>
              </div>
              
              <div class="setting-row">
                <div class="setting-label">👥 Capacity</div>
                <div class="setting-value">Unlimited 🌐</div>
              </div>
              
              <div class="setting-row">
                <div class="setting-label">👁️ Visibility</div>
                <select class="setting-select" v-model="eventData.visibility">
                  <option value="public">Public</option>
                  <option value="private">Private</option>
                </select>
              </div>

            </div>
          </div>

          <button class="btn-primary create-btn" @click="handleCreate">
            Create Event
          </button>
        </div>

        <div class="preview-panel">
          
          <div class="image-preview">
            <div class="ticket-graphic">
               <h3>{{ eventData.name || 'THE PARTY OF YOUR LIFE' }}</h3>
               <div class="ticket-details">
                 <span class="smile">🙂</span>
                 <span class="barcode">|||| || ||| ||||</span>
               </div>
            </div>
          </div>

          <div class="theme-section">
            <h4>Theme</h4>
            <div class="theme-cards">
              <div class="theme-card active" style="background: var(--tertiary-color);"></div>
              <div class="theme-card" style="background: linear-gradient(45deg, #1f7b31, #3b8d50);"></div>
              <div class="theme-card" style="background: linear-gradient(45deg, #1a2a6c, #182848);"></div>
              <div class="theme-card" style="background: linear-gradient(45deg, #ff416c, #ff4b2b);"></div>
            </div>

            <div class="theme-options">
              <div class="option-row">
                <div class="color-picker-label">
                  <div class="color-circle"></div>
                  <span>Color</span>
                </div>
                <span class="option-value">Custom ⌄</span>
              </div>
              <div class="option-row">
                <div class="font-picker-label">
                  <span class="ag-icon">Ag</span>
                  <span>Typeface</span>
                </div>
                <span class="option-value">Default ⌄</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

// État réactif pour le formulaire
const eventData = reactive({
  name: '',
  startDate: '2026-12-25',
  startTime: '09:00',
  endDate: '2026-12-29',
  endTime: '17:00',
  location: '',
  requireApproval: true,
  visibility: 'public',
});

// Méthode de soumission
const handleCreate = () => {
  console.log('Création de l\'évènement en cours...', eventData);
  // Logique d'appel API ici
  alert(`Évènement "${eventData.name || 'Sans nom'}" créé avec succès !`);
};
</script>

<style scoped>
/* Variables */
:root {
  --primary-color: #F2F864;
  --secondary-color: #EFF662;
  --tertiary-color: #222222;
  --background-color: #181818;
  --my-white: #fff;
  --secondary-light-color: #515151;
  --background-green-color: #3b8d50;
  --error-color: rgb(255, 86, 86);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* =========================================
   1. STYLES DE BASE (MOBILE FIRST)
   ========================================= */
.create-event-container {
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--my-white);
  font-family: 'Inter', system-ui, sans-serif;
  display: flex;
  flex-direction: column;
}

/* Navbar */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: transparent;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: bold;
  font-size: 1.2rem;
}

.logo-icon {
  width: 24px;
  height: 24px;
  background-color: var(--primary-color);
  color: var(--background-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-btn {
  background: var(--tertiary-color);
  border: 1px solid var(--secondary-light-color);
  color: var(--my-white);
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--tertiary-color);
  padding: 0.3rem 0.5rem;
  border-radius: 20px;
  border: 1px solid var(--secondary-light-color);
}

.avatar {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: var(--background-green-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
}

.avatar-sm {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: var(--background-green-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
}

.hidden-mobile { display: none; }

/* Main Content */
.main-content {
  flex: 1;
  padding: 1rem;
  display: flex;
  justify-content: center;
}

.creation-card {
  width: 100%;
  max-width: 1000px;
  background-color: var(--tertiary-color);
  border: 1px solid var(--secondary-light-color);
  border-radius: 20px;
  display: flex;
  flex-direction: column; /* S'empile sur mobile */
  overflow: hidden;
}

/* Form Panel */
.form-panel {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.organizer-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.organizer-info .label {
  font-size: 0.8rem;
  color: #a0a0a0;
}

.organizer-select {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.event-name-input {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--secondary-light-color);
  color: var(--my-white);
  font-size: 2rem;
  font-weight: 700;
  padding-bottom: 0.5rem;
  outline: none;
}

.event-name-input::placeholder {
  color: #555;
}

/* Groups (Date, Location, Settings) */
.form-group {
  display: flex;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--secondary-light-color);
  border-radius: 12px;
  padding: 1rem;
  gap: 1rem;
}

.icon-col, .date-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--background-color);
  border-radius: 8px;
  padding: 0.5rem;
  min-width: 50px;
}

.date-badge .month { font-size: 0.7rem; color: #a0a0a0; }
.date-badge .day { font-size: 1.2rem; font-weight: bold; }

.input-col, .date-inputs, .settings-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.input-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.row-label {
  width: 40px;
  color: #a0a0a0;
  font-size: 0.85rem;
}

input[type="date"], input[type="time"], input[type="text"], .setting-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid transparent;
  color: var(--my-white);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  outline: none;
  font-family: inherit;
  flex: 1;
}

input[type="date"]:focus, input[type="time"]:focus, input[type="text"]:focus {
  border-color: var(--secondary-light-color);
}

.timezone-row { font-size: 0.8rem; color: #a0a0a0; margin-top: 0.5rem; }

.location-group .sub-label {
  font-size: 0.8rem;
  color: #a0a0a0;
}

/* Settings List */
.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.setting-row:last-child { border-bottom: none; }

.setting-label { font-size: 0.9rem; color: #d0d0d0; }
.setting-value { font-size: 0.9rem; color: #a0a0a0; cursor: pointer; }

/* Toggle Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
}

.switch input { opacity: 0; width: 0; height: 0; }

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: var(--secondary-light-color);
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider { background-color: var(--primary-color); }
input:checked + .slider:before { transform: translateX(20px); background-color: var(--background-color); }
.slider.round { border-radius: 34px; }
.slider.round:before { border-radius: 50%; }

/* Bouton principal */
.btn-primary {
  background-color: var(--my-white); /* Changé pour correspondre au design (bouton blanc) */
  color: var(--background-color);
  border: none;
  border-radius: 8px;
  padding: 1rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1rem;
}

.btn-primary:hover {
  background-color: var(--primary-color);
}


/* Preview Panel */
.preview-panel {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.image-preview {
  width: 100%;
  aspect-ratio: 1 / 1;
  background-color: #000;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  border: 1px dashed var(--secondary-light-color);
}

.ticket-graphic {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); /* Placeholder holographique */
  width: 100%;
  height: 100%;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: var(--background-color);
  text-align: center;
  padding: 1rem;
  transform: rotate(-5deg);
  box-shadow: 0 10px 20px rgba(0,0,0,0.5);
}

.ticket-graphic h3 {
  font-size: 1.5rem;
  text-transform: uppercase;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1rem;
}

.theme-section h4 {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: var(--my-white);
}

.theme-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.theme-card {
  height: 60px;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
}

.theme-card.active { border-color: var(--primary-color); }

.theme-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: rgba(0,0,0,0.2);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--secondary-light-color);
}

.option-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.color-picker-label, .font-picker-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.color-circle {
  width: 20px; height: 20px;
  background-color: #8e44ad; /* Placeholder color */
  border-radius: 50%;
}

.ag-icon {
  font-weight: bold;
  font-size: 1.1rem;
}

.option-value {
  font-size: 0.9rem;
  color: #a0a0a0;
  cursor: pointer;
}

/* =========================================
   2. STYLES TABLETTE / DESKTOP (>= 1024px)
   ========================================= */
@media (min-width: 1024px) {
  .hidden-mobile { display: flex; }
  
  .top-nav { padding: 1.5rem 3rem; }

  .main-content { padding: 2rem 3rem; }

  .creation-card {
    flex-direction: row; /* Passage en 2 colonnes */
    border: none;
    background: transparent;
    gap: 2rem;
  }

  .form-panel, .preview-panel {
    flex: 1;
    background-color: var(--tertiary-color);
    border: 1px solid var(--secondary-light-color);
    border-radius: 20px;
    padding: 2.5rem;
  }

  .preview-panel {
    justify-content: space-between;
  }

  .event-name-input { font-size: 2.5rem; }
}
</style>