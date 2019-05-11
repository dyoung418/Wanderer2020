<template>
  <div v-if="user" class="account">
    HELLO
  </div>
  <div v-else class="center sign-in">
    <p class="center margin pure-form-message-inline">Please Register for an Account or Login.</p>
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
.link
{
  text-decoration: none;
  color: black;
}
.sign-in
{
  margin-top: 8%;
  border: 1px solid #ccc;
  background-color: #eee;
  border-radius: 4px;
  padding: 20px;
  color: black;
  width: 30%;
  max-width: 300px;
}
.margin {
  margin-top: 0px;
  margin-bottom: 15px;
}
</style>