<template>
  <div class="form-fields-wrapper">
    
    <div class="organizer-info">
      <span class="label">Create Under</span>
      <div class="organizer-select">
        <div class="avatar-sm">MS</div>
        <span>Maria Soniatha ⌄</span>
      </div>
    </div>

    <BaseInput
      type="text"
      class="event-name-input"
      placeholder="Event Name"
      v-model="formData.name"
    />

    <div class="form-group date-time-group">
      <div class="date-badge">
        <span class="month">{{ currentMonth }}</span>
        <span class="day">{{ currentDay }}</span>
      </div>
      <div class="date-inputs">
        <div class="input-row">
          <span class="row-label">Start</span>
          <BaseInput type="date" v-model="formData.startDate" :min="today" />
          <BaseInput type="time" v-model="formData.startTime" />
        </div>
        <div class="input-row">
          <span class="row-label">End</span>
          <BaseInput type="date" v-model="formData.endDate" :min="today" />
          <BaseInput type="time" v-model="formData.endTime" />
        </div>
        <div class="input-row timezone-row">
          <span>🌐 GMT +00:00 Abidjan</span>
        </div>
      </div>
    </div>

    <div class="form-group location-group">
      <div class="icon-col">📌</div>
      <div class="input-col">
        <BaseInput type="text" placeholder="Add Event Location" v-model="formData.location" />
        <span class="sub-label">Online or Offline Event</span>
      </div>
    </div>

    <div class="form-group settings-group">
      <div class="icon-col">⚙️</div>
      <div class="settings-list">
        
        <div class="setting-row">
          <div class="setting-label">📂 Category</div>
          <BaseSelect  v-model="formData.category">
            <option value="CONCERT">Concert</option>
            <option value="SPORT">Sport</option>
            <option value="CONFERENCE">Conférence</option>
            <option value="OTHER">Autre</option>
          </BaseSelect>
        </div>
        
        <div class="setting-row">
          <div class="setting-label">👤 Require Approval</div>
          <div class="setting-value">
            <label class="switch">
              <input type="checkbox" v-model="formData.requireApproval">
              <span class="slider round"></span>
            </label>
          </div>
        </div>
        
        <div class="setting-row">
          <div class="setting-label">👥 Capacity</div>
          <BaseInput type="number" v-model="formData.capacity" />
        </div>

      </div>
    </div>

    <textarea 
      class="description-area" 
      placeholder="Tell us more about the event..." 
      v-model="formData.description"
    ></textarea>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import BaseInput from '../input/BaseInput.vue';
import BaseSelect from '../input/BaseSelect.vue';

// On déclare que ce composant reçoit un objet 'formData' depuis son parent
const props = defineProps({
  formData: {
    type: Object,
    required: true
  }
});

// Calcul de la date d'aujourd'hui au format 'YYYY-MM-DD'
const today = useState('todayDate', () => new Date().toISOString().split('T')[0]);// Sécurisation : on vérifie si la date existe avant de la formater
const currentMonth = computed(() => {
  if (!props.formData.startDate) return 'MM';
  const d = new Date(props.formData.startDate);
  return d.toLocaleString('default', { month: 'short' }).toUpperCase();
});

const currentDay = computed(() => {
  if (!props.formData.startDate) return '--';
  return new Date(props.formData.startDate).getDate().toString().padStart(2, '0');
});
</script>

<style scoped>
.form-fields-wrapper { display: flex; flex-direction: column; gap: 1.2rem; }

.organizer-info { display: flex; flex-direction: column; gap: 0.3rem; }
.organizer-info .label { font-size: 0.8rem; color: #a0a0a0; }
.organizer-select { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; }

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
.event-name-input::placeholder { color: #555; }

.form-group { display: flex; background: rgba(0, 0, 0, 0.2); border: 1px solid var(--secondary-light-color); border-radius: 12px; padding: 1rem; gap: 1rem; }
.icon-col, .date-badge { 
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    justify-content: center; 
    background: var(--background-color); 
    border-radius: 8px; 
    padding: 0.5rem; 
    min-width: 60px; 
}
.date-badge .month { font-size: 0.7rem; color: var(--primary-color); }
.date-badge .day { font-size: 1.2rem; font-weight: bold; }

.date-inputs, .input-col, .settings-list { flex: 1; display: flex; flex-direction: column; gap: 0.5rem; }
.input-row { display: flex; align-items: center; gap: 0.5rem; }
.row-label { width: 40px; color: #a0a0a0; font-size: 0.8rem; }
.timezone-row { font-size: 0.8rem; color: #a0a0a0; margin-top: 0.5rem; }

input[type="date"], input[type="time"], input[type="text"], input[type="number"], .description-area {
  background: rgba(255, 255, 255, 0.05); border: 1px solid transparent; color: white; padding: 5px 10px; border-radius: 6px; outline: none; font-family: inherit; width: 100%;
}
input[type="text"]:focus, .description-area:focus { border-color: var(--primary-color); }

.setting-row { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.setting-row:last-child { border-bottom: none; }
.setting-label { font-size: 0.9rem; color: #d0d0d0; }

.description-area { min-height: 100px; resize: vertical; border: 1px solid var(--secondary-light-color); }

/* Switch Toggle */
.switch { position: relative; display: inline-block; width: 34px; height: 20px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #515151; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; }
input:checked + .slider { background-color: var(--primary-color); }
input:checked + .slider:before { transform: translateX(14px); }
</style>