<template>
    <div class="main-wrapper">
            
        <div class="description w-full">
            <h1>{{ title }}</h1> 
            <p class="subtitle">{{ description }}</p>
            <mainButton label="Derniers évènements" @click="()=>{router.push('auth/registration')}"/>
        </div>

        <lookingEventForm/>

    </div>
</template>

<script>
import mainButton from '../buttons/mainButton.vue'
import lookingEventForm from '../forms/lookingEventForm.vue'
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
export default {
    name: 'WelcomePage',
    props: {
        title: {
            type: String,
            default: 'Alors quel évènement souhaitez-vous découvrir aujourd\'hui?'
        },
        description: {
            type: String,
            default: 'Consulter tous nos derniers évènements et réservez vos billets en quelques clics seulement !'
        },
    },
    components: {
        mainButton,
        lookingEventForm
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
    width: 100%;
    
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
    padding: 6rem 0.5rem 1rem 0.5rem;
    display: flex;
    flex-direction: column;
    justify-content:center;
    align-items: center;
    gap: 2rem;
}

.content-container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

.description {
    /* Ancrage en bas à gauche */
    color: #ffffff;
    text-align: left; /* Aligne le texte à gauche */
    width: 100%;
    max-width: 600px; /* Évite que le texte s'étale trop sur les grands écrans */
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.description h1 {
    color: var(--primary-color);
    font-size: 2.75rem;
    font-weight: 600;
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
@media (min-width: 768px) {
    .main-wrapper {
        padding: 1.5rem;
        display: grid;
        grid-template-columns: 1fr;
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

@media (min-width: 1024px) {
    .main-wrapper {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        padding: 3rem;
    }

    .description {
        bottom: 3rem;
        left: 3rem;
        right: auto; /* Permet au texte de s'étendre sur la gauche sur les grands écrans */
    }

    .description h1 {
        font-size: 3rem;
    }

    .subtitle {
        font-size: 1.25rem;
    }
}
</style>