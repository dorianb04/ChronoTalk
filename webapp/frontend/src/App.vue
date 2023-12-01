<template>
  <div id=wrapper class="has-background-grey">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          <strong>Chronotalk</strong>
        </router-link>
      </div>
      <!--
      <div class="navbar-menu">
        <div class="navbar-end">
          <template v-if="$store.state.isAuthenticated">
            

            <div class="navbar-item">
              <div class="buttons">
                <router-link to="/dashboard/my-account" class="button is-light">
                  My account
                </router-link>
              </div>
            </div>
          </template>
          

          <template v-else>
            <router-link to="/" class="navbar-item">
                    Home
            </router-link>
            
            <div class="navbar-item">
              <div class="buttons">
                <router-link to="/sign-up" class="button is-success">
                  <strong>Sign up</strong>
                </router-link>

                <router-link to="/log-in" class="button is-light">
                  <strong>Log in</strong>
                </router-link>
              </div>
            </div>
          </template>
        </div>
      </div>
      -->
    </nav>

    

    <section class="section">
      <router-view/>
    </section>

    <footer class="footer has-background-dark">
      <p class="has-text-centered has-background-dark">Copyright (C) 2023</p>
    </footer>
  </div>
</template>

<script>
  import axios from 'axios'
  
  export default {
    name: 'App',
    beforeCreate() {
      this.$store.commit('initializeStore')

      const token = this.$store.state.token

      if (token) {
        axios.defaults.headers.common['Authorization'] = "Token " + token
      } else {
        axios.defaults.headers.common['Authorization'] = ""
      }

    }
  }
</script>

<style lang="scss">
@import '../node_modules/bulma';

#wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-wrapper {
  flex: 1;
  padding-bottom: 3rem; /* Adjust this value to control the footer height */
}

.footer {
  position: relative;
  bottom: 0;
  width: 100%;
  margin-top: auto;
}
</style>
