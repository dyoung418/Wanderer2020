<template>
  <div v-if="user" class="account">
    HELLO
  </div>
  <div v-else class="margin-top center">
    <p>Please Register for an Account or Login.</p>
    <router-link to="/register" class="link pure-button">Register</router-link> or
    <router-link to="/login" class="link pure-button">Login</router-link>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'account',
  components: {
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
  }
}
</script>

<style scoped>
.center{
  display: block;
  width: 100%; 
  margin: 0 auto;
  text-align: center;
}
.margin-top
{
  margin-top: 10%;
}
.link
{
  text-decoration: none;
  color: black;
}
</style>