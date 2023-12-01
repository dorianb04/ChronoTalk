<template>
    <div class="card">
      <div class="card-image">
        <figure class="image is-4by3">
          <img :src="character.image" alt="Character Image" />
        </figure>
      </div>
      <div class="card-content">
        <div class="media">
          <div class="media-content">
            <p class="title is-4">{{ character.name }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      character: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  /* Ajoutez ici des styles spécifiques à la carte du personnage si nécessaire */
  </style>
  