<template>
    <form @submit.prevent="handleLogin">

        <h3>Connexion</h3>

        <BaseInputVue 
            label="Email/username"
            v-model="credentials.username"
            :errorMessage="errorMessage.username"
        />

        <BaseInputVue 
            label="Mot de passe"
            v-model="credentials.password"
            :errorMessage="errorMessage.password"
            type="password"
        />

        <mainButton 
            label="Connexion" 
            type="submit"
            :isLoading="authStore.isLoading"
        />

        <div class="err-message-wrapper" v-if="authStore.error" >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
            </svg>
            <p class="error-message">
                {{ authStore.error }}
            </p>
        </div>

        <divider orientation="horizontal" :thickness="2" color="#515151" length="100%" />

        <p>J'ai pas de compte</p>

        <secondButton label="Ouvrir son compte"/>

    </form>
</template>

<script lang="ts">
import BaseInputVue from '../input/BaseInput.vue'
import mainButton from '../buttons/mainButton.vue';
import secondButton from '../buttons/secondButton.vue';
import divider from '../tools/divider.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/authStore';

interface ErrorMessage{
    username: string,
    password: string
}

interface Credentials{
    username: string,
    password: string,
    email: string
}

export default {
    components:{
        BaseInputVue,
        mainButton,
        secondButton,
        divider
    },
    setup(){

        const router = useRouter()

        // Store
        const authStore = useAuthStore()

        // State
        const credentials = ref<Credentials>({
            username:'',
            password:'',
            email:''
        })

        const errorMessage = ref<ErrorMessage>({
            username: '',
            password: ''
        })

        // computed
        const validateForm = (): boolean => {
            // On réinitialise les messages d'erreur à chaque vérification
            errorMessage.value.username = ''
            errorMessage.value.password = ''
            
            let isValid = true

            if (!credentials.value.username.trim()) {
                errorMessage.value.username = "Veuillez entrer un email ou un nom d'utilisateur."
                isValid = false
            } else if (credentials.value.username.length < 3) {
                errorMessage.value.username = "L'identifiant doit contenir au moins 3 caractères."
                isValid = false
            }

            if (!credentials.value.password) {
                errorMessage.value.password = "Veuillez entrer votre mot de passe."
                isValid = false
            }

            return isValid
        }

        const handleLogin = async () => {
            // 1. On lance la validation locale
            if (!validateForm()) return

            try {
                // 2. Si c'est valide, on tente la connexion (Correction de l'envoi de l'email ici)
                await authStore.login({
                email: credentials.value.email,
                username: credentials.value.username,
                password: credentials.value.password
                })
                router.push('/dashboard/profile') 
            } catch (error) {
                console.log('[Login] Erreur capturée', error)
            }
        }

        return{
            useRouter,
            authStore,
            credentials,
            errorMessage,
            validateForm,
            handleLogin
        }

    }
}
</script>

<style scoped>
.err-message-wrapper {
  padding: 10px;
  border-radius: 10px;
  width: 100%;
  background-color: var(--glass-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 15px; /* Petit espace visuel */
}

.err-message-wrapper svg {
  color: #eb4d5d;
  flex-shrink: 0;
}

.error-message {
  color: #eb4d5d;
  font-size: 0.9em;
  font-weight: 600;
}
</style>