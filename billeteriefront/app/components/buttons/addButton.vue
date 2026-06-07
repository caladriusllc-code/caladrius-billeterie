<template>
    <button class="action-button" aria-label="Créer un événement">
        <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke-width="2.5" 
            stroke="currentColor" 
            class="icon"
        >
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>

        <span class="label">Créer</span>
    </button>
</template>

<script setup lang="ts">
// Pas de logique nécessaire pour le moment, juste de l'affichage.
</script>

<style scoped>
/* ============================================================
   1. STYLE BASE & MOBILE (Floating Action Button - FAB)
   ============================================================ */
.action-button {
  /* Réinitialisation styles par défaut */
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease-in-out;
  
  /* Couleurs (J'utilise tes variables Caladrius supposées) */
  background-color: var(--primary-color); /* Violet par défaut */
  color: var(--background-color);
  
  /* Positionnement Fixe sur Mobile (Bouton flottant) */
  position: fixed;
  /* J'ajoute un décalage pour ne pas coller à la barre de navigation du bas si elle existe */
  bottom: calc(80px); 
  right: 20px;
  z-index: 90; /* Juste en dessous d'une éventuelle modale mais au-dessus du contenu */

  /* Forme Ronde sur Mobile */
  width: 56px;
  height: 56px;
  border-radius: 50%;
  
  /* Ombre portée pour l'effet "flottant" (Élévation) */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  font-size: 0.75rem; /* Petite taille de texte pour le label sur mobile */
}

/* Effets au survol/clic (Mobile & Desktop) */
.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

.action-button:active {
  transform: translateY(0);
  background-color: var(--primary-dark-color, #3a0e9e);
}

/* Icône sur Mobile */
.icon {
  width: 28px;
  height: 28px;
}

/* Texte caché sur Mobile */
.label {
  display: none;
}

/* ============================================================
   2. STYLE TABLETTE & DESKTOP (Bouton Standard) -> min-width: 768px
   ============================================================ */
@media (min-width: 768px) {
  .action-button {
    /* On annule le positionnement fixe pour qu'il s'intègre dans le flux (header, toolbar...) */
    position: static; 
    
    /* Forme Rectangulaire arrondis (assorti à tes EventCards) */
    width: auto;
    height: auto;
    padding: 0.75rem 1.5rem;
    border-radius: 999px;
    
    /* Alignement horizontal Icône + Texte */
    flex-direction: row;
    gap: 10px; /* Espace entre icône et texte */
    
    /* On adoucit l'ombre pour un bouton standard */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .action-button:hover {
    /* Légère brillance au survol sur desktop au lieu du mouvement */
    transform: none;
    filter: brightness(1.1);
  }

  /* Icône plus petite sur Desktop */
  .icon {
    width: 20px;
    height: 20px;
  }

  /* Affichage du texte sur Desktop */
  .label {
    display: block;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
    white-space: nowrap; /* Empêche le texte de passer à la ligne */
  }
}
</style>