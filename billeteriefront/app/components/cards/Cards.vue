<template>
    <article class="card-wrapper" @click="toggleFlip">
        <div :class="['card-inner', { 'is-flipped': isFlipped }]">
            
            <div class="card-face card-front glass">
                <div class="front-content">
                    <span class="card-number">{{ cardNumber }}</span>
                    <h2>{{ frontTitle }}</h2>
                    <p class="click-hint">Cliquez pour retourner <span>↺</span></p>
                </div>
            </div>

            <div class="card-face card-back glass">
                <slot></slot>
            </div>

        </div>
    </article>
</template>

<script lang="ts">
import { ref } from 'vue';
export default{
    name: 'AboutCard',
    components: {},
    props: {
        cardNumber: {
            type: String,
            required: true
        },
        frontTitle: {
            type: String,
            required: true
        }
    },
    setup() {
        // État local : chaque carte gère son propre retournement !
        const isFlipped = ref<boolean>(false);

        const toggleFlip = () => {
            isFlipped.value = !isFlipped.value;
        };

        return {
            isFlipped,
            toggleFlip
        };
    }
};
</script>

<style scoped>
/* ── La mécanique de la carte 3D ── */
.card-wrapper {
    perspective: 1200px;
    width: 100%;
    max-width: 450px; 
    aspect-ratio: 1.6 / 1; 
    cursor: pointer;
}

.card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    transform-style: preserve-3d;
}

.card-inner.is-flipped {
    transform: rotateY(180deg);
}

.card-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 1.5rem;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
}

.card-back {
    transform: rotateY(180deg);
    align-items: flex-start;
    text-align: left;
}

/* ── Le design Glassmorphism ── */
.glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2), inset 0 0 10px rgba(255, 255, 255, 0.05);
}

/* ── Typographie (Recto) ── */
.front-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.5rem;
}

.card-number {
    font-size: 3rem;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.1);
    position: absolute;
    top: 1rem;
    right: 1.5rem;
}

.card-front h2 {
    font-size: clamp(1.4rem, 4vw, 1.8rem);
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.click-hint {
    margin-top: 1rem;
    font-size: 0.85rem;
    color: #34d399;
    opacity: 0.8;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── Typographie (Verso injecté par le slot) ── */
/* On utilise :deep() pour cibler les éléments injectés par le parent */
:deep(.card-back h3) {
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0 0 1rem 0;
    color: #34d399;
}

:deep(.card-back p) {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #e2e8f0;
    margin: 0;
}

:deep(.benefits-list) {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

:deep(.benefits-list li) {
    font-size: 0.95rem;
    color: #e2e8f0;
}

:deep(.benefits-list strong) {
    color: #ffffff;
}

/* ── Responsive Mobile ── */
@media (max-width: 768px) {
    .card-wrapper {
        aspect-ratio: 1.4 / 1;
    }
}
</style>