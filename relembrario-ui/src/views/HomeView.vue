<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
    import { getAPI } from '../axios-api'

    export default {
      name: "Blog",
      data(){
        return {
          APIdata: [],
          loading: true,
          error: null
        }
      }


      created () {   
          getAPI.get('/blog/', )
              .then(response => {
                console.log('Deu certo')
                this.APIdata = response.data
                this.loading = false
                this.error = null
              })
              .catch(error => {
                console.error('Deu ruim', error)
                this.loading = false
                this.error = error.message
              })
        }
      }

</script>
