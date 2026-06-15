<template>
  <div class="modern-ticket">
    
    <div class="ticket-body">
      <div class="ticket-header">
        <span class="badge-nature">{{ eventData.nature || 'ÉVÉNEMENT' }}</span>
        <span class="ticket-date">🗓️ {{ displayDate }}</span>
      </div>
      
      <h3 class="ticket-title">
        {{ eventData.name || 'Le nom de votre événement apparaîtra ici' }}
      </h3>
      
      <div class="ticket-infos">
        <div class="info-line">
          <span class="icon">📍</span>
          <span class="text truncate">{{ eventData.location || 'Lieu à définir' }}</span>
        </div>
        <div class="info-line">
          <span class="icon">⏰</span>
          <span class="text">{{ eventData.startTime || '--:--' }}</span>
        </div>
      </div>
    </div>

    <div class="ticket-cutout">
      <div class="dashed-line"></div>
    </div>

    <div class="ticket-stub">
      <div class="stub-price">
        <span class="price-label">Tarif</span>
        <span class="price-value">{{ displayPrice }}</span>
      </div>
      <div class="barcode-mockup">
        ||||| | ||| |||| | ||
      </div>
    </div>
    
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, type PropType } from 'vue';

export default defineComponent({
  name: 'TicketPreview',
  props: {
    eventData: {
      type: Object as PropType<any>,
      required: true
    }
  },
  setup(props) {
    const displayDate = computed(() => {
      if (!props.eventData.startDate) return '25 DÉC. 2026';
      const d = new Date(props.eventData.startDate);
      return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();
    });

    const displayPrice = computed(() => {
      const tickets = props.eventData.tickets;
      if (!tickets || tickets.length === 0) return 'Gratuit';
      const minPrice = Math.min(...tickets.map((t: any) => t.price || 0));
      return minPrice === 0 ? 'Gratuit' : `Dès ${minPrice} FCFA`;
    });

    return { displayDate, displayPrice };
  }
});
</script>

<style scoped>
.modern-ticket {
  width: 100%;
  max-width: 320px;
  background: linear-gradient(135deg, var(--primary-color, #3b8d50) 0%, #173d22 100%);
  border-radius: 16px;
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  transform: rotate(-2deg);
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.modern-ticket:hover { transform: rotate(0deg) scale(1.03); }

.ticket-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1.2rem; }
.ticket-header { display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; font-weight: 600; color: rgba(255, 255, 255, 0.8); }
.badge-nature { background: rgba(255, 255, 255, 0.15); padding: 0.3rem 0.6rem; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px; font-size: 0.7rem; }
.ticket-title { font-size: 1.4rem; font-weight: 800; line-height: 1.2; margin: 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

.ticket-infos { display: flex; flex-direction: column; gap: 0.5rem; }
.info-line { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: rgba(255, 255, 255, 0.9); }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; }

.ticket-cutout { position: relative; height: 30px; width: 100%; display: flex; align-items: center; }
.ticket-cutout::before, .ticket-cutout::after {
  content: ''; position: absolute; width: 30px; height: 30px; background-color: #0d0d12; border-radius: 50%; top: 0; z-index: 2;
}
.ticket-cutout::before { left: -15px; }
.ticket-cutout::after { right: -15px; }
.dashed-line { width: calc(100% - 40px); margin: 0 auto; border-top: 2px dashed rgba(255, 255, 255, 0.3); }

.ticket-stub { padding: 1.2rem 1.5rem 1.5rem; display: flex; justify-content: space-between; align-items: center; }
.stub-price { display: flex; flex-direction: column; }
.price-label { font-size: 0.7rem; text-transform: uppercase; color: rgba(255, 255, 255, 0.6); letter-spacing: 1px; }
.price-value { font-size: 1.2rem; font-weight: 800; color: white; }
.barcode-mockup { font-family: 'Courier New', Courier, monospace; font-size: 1rem; font-weight: bold; letter-spacing: 2px; color: rgba(255, 255, 255, 0.5); transform: scaleY(1.5); }
</style>