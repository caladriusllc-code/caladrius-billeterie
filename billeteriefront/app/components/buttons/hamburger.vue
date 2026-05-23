<template>
  <div class="hamburger">
    <!-- From Uiverse.io by Cevorob --> 
    <label class="burger" for="burger">
      <input 
        type="checkbox" 
        id="burger" 
        :checked="isOpen"
        @change="$emit('toggle')"
      >
      <span></span>
      <span></span>
      <span></span>
    </label>
  </div>
</template>

<script lang="ts">

export default{
  props:{
    isOpen:{
      type:Boolean,
      default:false
    },
  },
  emits:['toggle']
}

</script>

<style scoped>
/* From Uiverse.io by Cevorob */ 

.burger {
  position: relative;
  width: 40px;
  height: 20px;
  background: transparent;
  cursor: pointer;
  display: block;
}

.burger input {
  display: none;
}

.burger span {
  display: block;
  position: absolute;
  height: 3px;
  width: 80%;
  background: var(--primary-color);
  border-radius: 9px;
  opacity: 1;
  left: 0;
  transition: .25s ease-in-out;
}

.burger span:nth-of-type(1) {
  top: 0px;
  transform-origin: center center;
}

.burger span:nth-of-type(2) {
  top: 50%;
  transform: translateY(-50%);
  transform-origin: center center;
}

.burger span:nth-of-type(3) {
  top: 100%;
  transform: translateY(-100%);
  transform-origin: center center;
}

.burger input:checked ~ span:nth-of-type(1) {
  transform: rotate(45deg);
  top: 10px;
  left: 0;
}

.burger input:checked ~ span:nth-of-type(2) {
  width: 0%;
  opacity: 0;
}

.burger input:checked ~ span:nth-of-type(3) {
  transform: rotate(-45deg);
  top: 10px;
  left: 0;
}

</style>