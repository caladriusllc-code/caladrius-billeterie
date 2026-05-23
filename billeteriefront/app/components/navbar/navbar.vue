<template>
    <!-- Ajout de la classe dynamique au scroll -->
    <header :class="['main-header', { 'is-scrolled': isScrolled }]">
        <nav class="nav-container">

            <!-- Logo -->
            <h3 class="logo">
                <span class="logo-accent">Cal</span>Event
            </h3>

            <!-- CTA desktop -->
            <navBarButtonVue/>
                

            <!-- Hamburger (caché sur desktop) -->
            <Hamburger
                :class="['mobile-only', { 'is-active': isMenuOpen }]"
                :isOpen="isMenuOpen"
                @toggle="toggleMenu"
            />
        </nav>

        <!-- Menu mobile avec transition -->
        <transition name="slide-down">
            <div v-if="isMenuOpen" class="nav-mobile-menu">
                <ul class="nav-links-mobile">
                    
                </ul>
                <a href="#" class="cta-mobile" @click="toggleMenu">Connexion</a>
            </div>
        </transition>
    </header>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Hamburger from '../buttons/hamburger.vue';
import navBarButtonVue from '../buttons/navBarButton.vue';

export default {
    name: 'MainHeader',
    components: { Hamburger, navBarButtonVue },

    setup() {
        const isMenuOpen = ref<boolean>(false);
        const isScrolled = ref<boolean>(false);

        const toggleMenu = () => {
            isMenuOpen.value = !isMenuOpen.value;
        };

        // Gestion propre du scroll avec l'API Composition de Vue 3
        const handleScroll = () => {
            if (window.scrollY > 20) {
                isScrolled.value = true;
            } else {
                isScrolled.value = false;
            }
        };

        onMounted(() => {
            window.addEventListener('scroll', handleScroll);
            // Appel initial pour vérifier la position au chargement de la page
            handleScroll();
        });

        onUnmounted(() => {
            window.removeEventListener('scroll', handleScroll);
        });

        return { isMenuOpen, isScrolled, toggleMenu };
    },
};
</script>

<style scoped>
/* =============================================
   BASE — Mobile first (Tout en haut)
   ============================================= */
   .main-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
    
    /* Écritures flottantes : fond, flou et ombres invisibles */
    background: rgba(255, 255, 255, 0); 
    backdrop-filter: blur(0px);
    -webkit-backdrop-filter: blur(0px); 
    border-bottom: 1px solid rgba(255, 255, 255, 0);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0);

    /* Animation fluide lors de l'apparition du verre */
    transition: background 0.3s ease, 
                backdrop-filter 0.3s ease, 
                border 0.3s ease, 
                box-shadow 0.3s ease,
                top 0.3s ease;
}

/* État actif dès que l'on commence à scroller */
.main-header.is-scrolled {
    background: rgba(255, 255, 255, 0.75); 
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px); 
    border-bottom: 1px solid rgba(255, 255, 255, 0.80);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
    padding: 0 1.5rem;
}

/* --- Logo --- */
.logo {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary-color);
    white-space: nowrap;
}

.logo-accent {
    background: var(--primary-color);
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    margin-right: 2px;
}

/* --- Liens desktop : cachés par défaut (mobile first) --- */
.nav-links-desktop {
    display: none;
}

.cta-desktop {
    display: none;
}

/* --- Hamburger : visible sur mobile --- */
.mobile-only {
    display: flex; 
}

/* =============================================
   MENU MOBILE
   ============================================= */
.nav-mobile-menu {
    position: absolute;
    top: 70px;
    left: 0;
    width: 100%;
    /* On garde le menu mobile compact en mode glass lorsqu'il s'ouvre */
    background: rgba(255, 255, 255);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem 1.5rem 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.4);
}

.nav-links-mobile li a {
    display: block;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(0, 0, 0, 0.04);
    color: var(--primary-color);
    text-decoration: none;
    transition: opacity 0.2s;
}

.nav-links-mobile li:last-child a {
    border-bottom: none;
}

.nav-links-mobile li a:hover {
    opacity: 0.6;
}

.nav-mobile-menu .cta-mobile{
    align-self: center;
}

.cta-mobile {
    display: block;
    text-align: center;
    background: var(--primary-color);
    width: 70%;
    align-items: center;
    color: var(--background-color);
    padding: 0.85rem 1.5rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    transition: opacity 0.2s, background 0.2s, color 0.2s;
}
.cta-mobile2 {
    display: block;
    text-align: center;
    background: transparent;
    color: var(--primary-color);
    padding: 0.85rem 1.5rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    transition: opacity 0.2s, background 0.2s, color 0.2s;
}

.cta-mobile:hover {
    opacity: 0.85;
}

/* =============================================
   ANIMATIONS MENU MOBILE
   ============================================= */
.slide-down-enter-active,
.slide-down-leave-active {
    transition: all 0.28s ease-out;
}

.slide-down-enter-from,
.slide-down-leave-to {
    transform: translateY(-12px);
    opacity: 0;
}

/* =============================================
   BREAKPOINT DESKTOP — ≥ 1024px
   ============================================= */
@media (min-width: 1024px) {
    .main-header {
        top: 16px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 1200px;
        border-radius: 50px;
        
        /* État initial Desktop (tout en haut) : Pas de fond ni de bordure pour la pilule */
        background: rgba(255, 255, 255, 0);
        backdrop-filter: blur(0px);
        -webkit-backdrop-filter: blur(0px);
        border: 1px solid rgba(255, 255, 255, 0);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0);
    }

    /* La pilule magique de verre se matérialise ici au défilement */
    .main-header.is-scrolled {
        top: 16px; 
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.45);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.06);
    }

    .nav-container {
        padding: 0 2rem;
        width: 100%;
        gap: 1rem;
        flex: 1;
        justify-content: space-between;
        align-items: center;
    }

    .nav-links-desktop {
        display: flex;
        list-style: none;
        padding: 0;
        margin: 0;
        gap: 0.5rem;
        flex: 1; 
        justify-content: center;
    }

    .nav-links-desktop li a {
        display: flex;
        align-items: center;
        white-space: nowrap;  
        font-size: 0.9rem;
        gap:0.2rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        color: var(--tertiary-color);
        text-decoration: none;
        transition: background 0.2s, opacity 0.2s;
    }

    .nav-links-desktop li a:hover {
        background: rgba(255, 255, 255, 0.4);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    .cta-desktop {
        display: block;
        white-space: nowrap;
        background: var(--primary-color);
        color: var(--background-color);
        padding: 0.6rem 1.25rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.88rem;
        text-decoration: none;
        transition: opacity 0.2s, transform 0.2s;
    }

    .cta-desktop2 {
        display: block;
        white-space: nowrap;
        background: transparent;
        color: var(--primary-color);
        padding: 0.6rem 1.25rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 0.88rem;
        text-decoration: none;
        transition: opacity 0.2s, background 0.2s, color 0.2s;
    }

    .cta-desktop:hover {
        opacity: 0.85;
        transform: scale(1.02);
    }
    .cta-desktop2:hover {
        opacity: 0.85;
        background: var(--primary-color);
        color: white;
    }

    .mobile-only {
        display: none !important;
    }

    .nav-mobile-menu {
        display: none !important;
    }
}

.main-header.is-scrolled .nav-links-desktop li a {
    /* L'écriture devient ton bleu primaire au scroll ! */
    color: var(--primary-color);
}
</style>