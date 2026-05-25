<template>
  <button class="cta-btn">
    <span>Espace membre</span>
  </button>
</template>

<script>
export default {

    name:'mainButton'

}
</script>

<style scope>

.cta-btn{
  max-width: 200px;
  border: none;
  border-radius: 999px;
  background: var(--secondary-color);
  color: var(--background-color);
  display:none;
}

@media (min-width: 768px) {
  .cta-btn {
    display: block;
  }
}

</style>