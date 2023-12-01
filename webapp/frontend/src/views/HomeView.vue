<template>
  <div class="home">
    <h1 class="title has-text-white">Welcome to Chronotalk</h1>

    <template v-if="$store.state.isAuthenticated">
      <router-link to="/game/game-menu" class="button is-success">
        Play
      </router-link>
    </template>

    <template v-else>
      <p class="has-text-white">Please Register & Log in to play Chronotalk!</p>
    </template>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  components: {
  },
  beforeRouteEnter(to, from, next) {
    // Rediriger automatiquement vers la page GameMenu
    next({ name: "GameMenu" });
  },
}
</script>
