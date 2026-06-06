<template>
  <div
    class="divider"
    :class="[
      `divider--${orientation}`,
      { 'divider--dashed': dashed }
    ]"
    :style="dividerStyle"
    role="separator"
    :aria-orientation="orientation"
  />
</template>

<script setup> 
import { computed } from 'vue';

const props = defineProps({
  // Orientation : 'horizontal' ou 'vertical'
  orientation: {
    type: String,
    default: 'horizontal',
    validator: (val) => ['horizontal', 'vertical'].includes(val)
  },
  // Couleur du trait (tout format CSS valide)
  color: {
    type: String,
    default: '#e0e0e0'
  },
  // Épaisseur (en px)
  thickness: {
    type: Number,
    default: 1
  },
  // Marge intérieure (padding) ou espacement autour
  spacing: {
    type: String,
    default: '16px'  // ex: '1rem', '20px', '0 16px'
  },
  // Version pointillée
  dashed: {
    type: Boolean,
    default: false
  },
  // Longueur max (pour orientation verticale = hauteur, horizontale = largeur)
  length: {
    type: String,
    default: 'auto'
  }
});

const dividerStyle = computed(() => {
  const base = {
    backgroundColor: props.dashed ? 'transparent' : props.color,
    border: props.dashed ? `${props.thickness}px dashed ${props.color}` : 'none'
  };

  if (props.orientation === 'horizontal') {
    return {
      ...base,
      width: props.length === 'auto' ? '100%' : props.length,
      height: `${props.thickness}px`,
      margin: `${props.spacing} 0`
    };
  } else {
    // vertical
    return {
      ...base,
      height: props.length === 'auto' ? '100%' : props.length,
      width: `${props.thickness}px`,
      margin: `0 ${props.spacing}`
    };
  }
});
</script>

<style scoped>
.divider {
  flex-shrink: 0;
  display: inline-block;
}

.divider--horizontal {
  display: block;
}

.divider--vertical {
  display: inline-block;
  vertical-align: middle;
}
</style>