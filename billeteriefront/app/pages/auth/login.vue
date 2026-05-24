<template>
    <div class="main-wrapper">
        <loginForm />
    </div>
</template>

<script setup>
import loginForm from '~/components/forms/loginForm.vue';
</script>

<style scoped>
.main-wrapper {
    /* Dégradé de transparent vers le noir + image de fond */
    background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0) 0%, #000000 100%),
                      url('../../assets/images/pexels-pavel-danilyuk-8761327.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    
    /* Centrage du formulaire et pleine hauteur */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* Optionnel : assombrit légèrement l'ensemble pour meilleur contraste */
    background-color: #000000;
}
</style>