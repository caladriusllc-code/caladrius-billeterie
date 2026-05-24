<template>
  <div class="stepper-wrapper">
    <!-- Rangée des cercles + connecteurs -->
    <div class="stepper-track">
      <template v-for="(step, index) in steps" :key="index">
        <!-- Cercle -->
        <div
          class="step__circle"
          :class="{
            'step__circle--active': step.isActive,
            'step__circle--completed': isCompleted(index)
          }"
        >
          <svg
            v-if="isCompleted(index)"
            class="step__check"
            viewBox="0 0 12 10"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M1 5L4.5 8.5L11 1.5"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <span v-else class="step__number">{{ index + 1 }}</span>
        </div>

        <!-- Connecteur entre deux cercles -->
        <div
          v-if="index < steps.length - 1"
          class="step__connector"
          :class="{ 'step__connector--filled': isCompleted(index) }"
        >
          <span class="step__connector-fill"></span>
        </div>
      </template>
    </div>

    <!-- Rangée des labels, alignée sous les cercles -->
    <div class="stepper-labels">
      <template v-for="(step, index) in steps" :key="index">
        <span
          class="step__label"
          :class="{
            'step__label--active': step.isActive,
            'step__label--completed': isCompleted(index)
          }"
        >{{ step.name }}</span>

        <!-- Espaceur vide calé sur le connecteur -->
        <span v-if="index < steps.length - 1" class="step__label-spacer"></span>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    steps: {
      type: Array,
      required: true
    }
  },
  computed: {
    activeIndex() {
      return this.steps.findIndex(s => s.isActive);
    }
  },
  methods: {
    isCompleted(index) {
      return index < this.activeIndex;
    }
  }
}
</script>

<style scoped>
/* ── Variables locales ── */
.stepper-wrapper {
  --circle-size: 36px;
  --connector-h: 2px;
  width: 100%;
  padding: 2rem 1rem;
}

/* ══════════════════════════════════════════
   TRACK : cercles + connecteurs sur une seule ligne
   Chaque cercle a flex:0 (taille fixe) et
   chaque connecteur a flex:1 (remplit l'espace restant).
   ══════════════════════════════════════════ */
.stepper-track {
  display: flex;
  align-items: center;   /* centrage vertical parfait */
  width: 100%;
  max-width: 500px;
}

/* ── Cercle ── */
.step__circle {
  flex: 0 0 var(--circle-size);
  width: var(--circle-size);
  height: var(--circle-size);
  border-radius: 50%;
  border: 2px solid color-mix(in srgb, var(--primary-color) 25%, transparent);
  background-color: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease,
    box-shadow 0.3s ease,
    transform 0.25s ease;
}

.step__circle--active {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  box-shadow:
    0 0 0 4px color-mix(in srgb, var(--primary-color) 18%, transparent),
    0 4px 14px color-mix(in srgb, var(--primary-color) 35%, transparent);
  transform: scale(1.08);
}

.step__circle--completed {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

/* ── Numéro ── */
.step__number {
  font-size: 0.8rem;
  font-weight: 600;
  color: color-mix(in srgb, var(--primary-color) 70%, transparent);
  line-height: 1;
  letter-spacing: 0.02em;
}

.step__circle--active .step__number {
  color: var(--background-color);
}

/* ── Checkmark ── */
.step__check {
  width: 12px;
  height: 10px;
  color: #fff;
}

/* ── Connecteur ── */
.step__connector {
  flex: 1 1 0;           /* remplit tout l'espace entre deux cercles */
  height: var(--connector-h);
  background-color: color-mix(in srgb, var(--primary-color) 20%, transparent);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.step__connector-fill {
  display: block;
  height: 100%;
  width: 0%;
  background-color: var(--primary-color);
  border-radius: 999px;
  transition: width 0.5s cubic-bezier(0.65, 0, 0.35, 1);
}

.step__connector--filled .step__connector-fill {
  width: 100%;
}

/* ══════════════════════════════════════════
   LABELS : rangée séparée, alignée sous le track.
   Même structure flex : label(flex:0) + spacer(flex:1)
   Les labels sont centrés sur leur cercle via text-align.
   ══════════════════════════════════════════ */
.stepper-labels {
  display: flex;
  align-items: flex-start;
  width: 100%;
  margin-top: 0.55rem;
}

.step__label {
  flex: 0 0 var(--circle-size);
  width: var(--circle-size);
  display: flex;
  text-align: center;
  justify-content: center;
  font-size: 0.72rem;
  font-weight: 500;
  color: #9ca3af;
  letter-spacing: 0.03em;
  line-height: 1.3;
  transition: color 0.3s ease;

  /* Débordement du texte centré sur le cercle */
  overflow: visible;
  white-space: nowrap;
  /*transform: translateX(-50%) translateX(calc(var(--circle-size) / 2));*/
}

.step__label--active {
  color: var(--primary-color);
  font-weight: 600;
}

.step__label--completed {
  color: color-mix(in srgb, var(--primary-color) 70%, #374151);
}

/* Espaceur calé sur les connecteurs */
.step__label-spacer {
  flex: 1 1 0;
}
</style>