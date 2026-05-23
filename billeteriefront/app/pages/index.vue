<template>
    <div class="main-wrapper">
        <navbar/>
        <eventDetailSectionVue/>
    </div>
</template>

<script>
import navbar from '../components/navbar/navbar.vue'
import eventDetailSectionVue from '../components/sections/eventDetailSection.vue'

export default {
    components:{
        eventDetailSectionVue,
        navbar
    }
}
</script>

<style>

</style>