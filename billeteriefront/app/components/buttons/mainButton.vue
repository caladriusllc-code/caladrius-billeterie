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
button{
    cursor: pointer;
    border: none;
    width: 100%;
    max-width: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 0.75rem 1.5rem;
    border-radius: 999px;
}

.main-button{
    background-color: var(--primary-color);
    color: var(--background-color);
    transition: all 0.2s ease-in-out;
}

.main-button:hover{
    background-color: var(--primary-color-dark);
    color: var(--background-color);
    transition: all 0.3s ease-in-out;
}

</style>