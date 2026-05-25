<template>
    <article class="pro-card">
        <div 
            class="card-bg" 
            :style="{ backgroundImage: `url(${image})` }"
        ></div>

        <div class="overlay"></div>

        <div class="card-info">
            <h4 class="pro-name">{{ title }}</h4>
            <p class="pro-info">{{ description }}</p>
            <p class="pro-specialty" >{{ subtitle }}</p>
        </div>

        <div class="btn-container">
            <button @click.stop="()=>{$emit('buy')}">
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
                    </svg>
                </span>
            </button>
        </div>
        <div class="btn_container2">
            <button @click.stop="()=>{$emit('view')}">
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                </span>
            </button>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import defaultImg from '../../assets/images/pexels-jibarofoto-14664084.jpg';

export default defineComponent({
    name: 'ContratCards',
    props: {
        title: {
            type: String,
            default: 'James Benjamin'
        },
        subtitle: {
            type: String,
            default: 'CEO @ Framify'
        },
        description: {
            type: String,
            default: 'bienvenue au pays mon fils'
        },
        image: {
            type: String,
            default: defaultImg
        }
    },
    emits:['buy', 'view'],
    setup(props, {emit}){

        function buyContrat(){
            console.log('vous avez cliqué')
        }
        function viewContrat(){
            console.log('vous avez cliqué pour voir')
        }
        return{
            buyContrat,
            viewContrat
        }
    }
});
</script>

<style scoped>
.pro-card {
    position: relative;
    width: 100%;
    /* On garde un ratio vertical élégant */
    aspect-ratio: 1 / 1.25; 
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    background-color: #1a1a1a;
}

/* Image de fond avec effet de zoom au survol */
.card-bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center;
    transition: transform 0.7s cubic-bezier(0.25, 1, 0.5, 1);
    z-index: 1;
}

.pro-card:hover .card-bg {
    transform: scale(1.1);
}

/* Overlay : sombre en bas (pour le texte) et transparent en haut */
.overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to top, 
        rgba(0, 0, 0, 0.8) 0%, 
        rgba(0, 0, 0, 0.4) 40%, 
        transparent 100%
    );
    z-index: 2;
}

/* Positionnement du texte */
.card-info {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 1.5rem;
    z-index: 3;
    color: #ffffff;
}

.pro-name {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.02em;
}

.pro-info {
    font-size: 0.80rem;
    font-weight: 500;
    color: #d1d1d1; /* Un gris clair pour le texte descriptif */
}

.pro-specialty {
    margin: 0.5rem 0 0 0;
    font-size: 0.9rem;
    font-weight: 700;
    background: var(--primary-color);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    width: fit-content;
    max-width: 80%;
    color: #ffffff;
}

/* Optionnel : petite barre d'accentuation au survol */
.pro-name::after {
    content: '';
    display: block;
    width: 0;
    height: 2px;
    background: #34d399; /* Ton vert d'accentuation */
    margin-top: 4px;
    transition: width 0.3s ease;
}

.pro-card:hover .pro-name::after {
    width: 40px;
}

.btn-container {
    z-index: 4;
    position: absolute;
    bottom: 9px;
    right: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-color);
    border-radius: 999px;
    width: 45px;
    height: 45px;
}
.btn_container2 {
    z-index: 3;
    position:absolute;
    bottom: 9px;
    right: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border-radius: 999px;
    width: 45px;
    height: 45px;
}

.pro-card button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    color: #ffffff;
    background: transparent;
    transition: transform 0.3s ease;
    flex-shrink: 0;
}

.pro-card button:hover {
    transform: scale(1.1) rotate(5deg);
}

.pro-card button svg {
    width: 20px;  /* Taille explicite de l'icône */
    height: 20px;
}

.size-6 {
    width: 18px;
    height: 18px;
}
</style>