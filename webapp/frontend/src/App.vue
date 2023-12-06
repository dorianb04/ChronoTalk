<template>
  <div class="MyWrapper">
    <!--<nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          <strong>Chronotalk</strong>
        </router-link>
      </div>
      
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
      
    </nav>-->

    

    <section class="section">
      <router-view/>
    </section>
<!--
    <footer class="footer has-background-dark">
      <p class="has-text-centered has-background-dark">Copyright (C) 2023</p>
    </footer>-->
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



.MyWrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: -webkit-linear-gradient(-45deg, #183850 0, #183850 25%, #192C46 50%, #22254C 75%, #22254C 100%);
  padding: 0px;
  overflow: overlay;
}

.MyWrapper::-webkit-scrollbar {
  width: 8px;
}

.MyWrapper::-webkit-scrollbar-thumb {
  background-color: #6b6b6b;
  border-radius: 4px;
}

.MyWrapper::-webkit-scrollbar-track {
  background-color: #7070704d;
}

.MyWrapper::-webkit-scrollbar-thumb:hover {
  background-color: #555;
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

::-webkit-scrollbar {
   display: none;
}


body {
  overflow: hidden;
}
</style>
