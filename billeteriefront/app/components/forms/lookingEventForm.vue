<template>
    <form action="">
        <BaseSelect label="Catégorie de d'évènement"/>
        <BaseSelect label="Choisir la ville"/>
        <BaseInput label="Selectionner la date" type="date"/>
        <mainButton label="Rechercher"/>
    </form>  
</template>

<script>
import BaseInput from '../input/BaseInput.vue'
import BaseSelect from '../input/BaseSelect.vue'
import mainButton from '../buttons/mainButton.vue'
export default {
    components:{
        BaseInput,
        BaseSelect,
        mainButton
    }
}
</script>

<style>

</style>