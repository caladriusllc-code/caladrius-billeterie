<template>
    <div class="main-wrapper">
        <div class="content-container">
            
            <div class="description">
                <h1>{{ title }}</h1>
                <!-- 
                    <p class="subtitle">{{ description }}</p>
                    <div class="meta-info">
                        <span class="date">{{ date }}</span>
                        <span class="separator" v-if="date && location">|</span>
                        <span class="location">{{ location }}</span>
                    </div>
                -->
                <mainButton label="S'inscrire" @click="()=>{router.push('auth/registration')}"/>
            </div>

        </div>
    </div>
</template>

<script>
import mainButton from '../buttons/mainButton.vue'
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
export default {
    name: 'WelcomePage',
    props: {
        title: {
            type: String,
            default: 'Gérer vos événements n\'a jamais été aussi simple !'
        },
        description: {
            type: String,
            default: 'Heureux de te revoir parmi nous.'
        },
        date: {
            type: String,
            default: '10 octobre 2023'
        },
        location: {
            type: String,
            default: 'Paris, France'
        }
    },
    components: {
        mainButton
    },
    setup(){
        const router = useRouter();

        return {
            router
        }
    }
}
</script>

<style scoped>
.main-wrapper {
    /* Position relative indispensable pour servir de repère au bloc en absolute */
    position: relative;
    
    /* Force l'image à prendre toute la hauteur de l'écran */
    min-height: 100vh;
    
    /* Dégradé noir semi-transparent superposé à l'image */
    background-image: linear-gradient(
        to bottom, 
        rgba(0, 0, 0, 0.2) 0%, 
        rgba(0, 0, 0, 0.85) 100%
    ),
    url('../../assets/images/pexels-pavel-danilyuk-8761327.jpg');
    
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-color: #000000;
    padding: 2rem;
}

.content-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

.description {
    /* Ancrage en bas à gauche */
    position: absolute;
    bottom: 3rem; /* Espace depuis le bas de l'écran */
    left: 3rem;   /* Espace depuis la gauche de l'écran */
    color: #ffffff;
    text-align: left; /* Aligne le texte à gauche */
    width: 80%;
    max-width: 600px; /* Évite que le texte s'étale trop sur les grands écrans */
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.description h1 {
    color: var(--primary-color);
    font-size: 3.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
}

.subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    margin: 0 0 1rem 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.meta-info {
    display: flex;
    gap: 0.75rem;
    font-size: 1rem;
    opacity: 0.75;
}

.separator {
    color: var(--primary-color);
}

/* Responsive pour les tablettes et smartphones */
@media (max-width: 768px) {
    .main-wrapper {
        padding: 1.5rem;
    }

    .description {
        bottom: 2rem;
        left: 1.5rem;
        right: 1.5rem; /* Évite que le texte dépasse à droite sur mobile */
    }

    .description h1 {
        font-size: 2.2rem;
    }

    .subtitle {
        font-size: 1.1rem;
    }
}
</style>