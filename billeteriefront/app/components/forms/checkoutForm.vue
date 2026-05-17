<template>
    <form action="" class="checkout-form">
        <BaseInput label="Nom complet"/>
        <BaseInput label="Email"/>
        <BaseInput label="Numéro de téléphone"/>
        <BaseInput label="Adresse"/>
        <main-button label="Acheter"/>
    </form>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import BaseInput from '../input/BaseInput.vue';
import mainButton from '../buttons/mainButton.vue';
export default {
    components:{
        BaseInput,
        mainButton
    }
}
</script>

<style scoped>
/* mobile first */
.checkout-form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
</style>