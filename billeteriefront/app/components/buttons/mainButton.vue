<template>

    <button class="main-button">
        <template v-if="!isLoading">
            {{ label }}
        </template>

        <template v-else>
            <span class="loading loading-spinner loading-md"></span>
        </template>

    </button>

</template>

<script lang="ts">
export default {
    name:'mainButton',
    props:{
        label:{
            type:String,
            default:'Acheter vos billets'
        },
        isIcon:{
            type:Boolean,
            default:true
        },
        isLoading: {
            type: Boolean,
            default: false
        }
    },
}
</script>

<style scoped>

.main-button{
    background-color: var(--primary-color);
    color: var(--background-color);
    transition: all 0.2s ease-in-out;
}

.main-button:hover{
    background-color: #f8ff23;
    color: var(--background-color);
    transition: all 0.3s ease-in-out;
}

</style>