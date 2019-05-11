<template>
  <div class="mainmenubuttons">
    <button class="menu-button" @mouseover="hover" @click="press">{{label}}</button>
  </div>
</template>

<script>
export default {
  name: 'mainmenubutton',
  props: {
    label: String,
    route: String,
    sound: String,
  },
  methods: {
      hover()
      {
            this.$store.dispatch("playSound", {sound: 2, volume: 0});
      },
      press()
      {
            this.$store.dispatch("playSound", {sound: 0, volume: 0});
            this.$router.push(this.route);
      },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url('https://fonts.googleapis.com/css?family=Francois+One');
.menu-button
{
    font-family: 'Francois One', sans-serif;
    text-transform: uppercase;
    display: block;
    margin: 0 auto;
    margin-bottom: 30px;
    border-radius: 15px;
    padding: 1em;
    width: 400px;
    border: 0px solid black;
    font-size: 1.75em;
    text-align: center;
    color: rgba(131, 131, 131, 0.904);
    background: radial-gradient(rgb(48, 7, 124),rgb(35, 4, 92));
    background-size: cover;
    background-repeat: no-repeat;
    transition: font-size .1s ease-in-out 0s, padding .1s ease-in-out 0s, background .1s ease-in-out 0s;
}

.menu-button:hover
{
    font-size: 2.5em;
    padding-top: .49em;
    padding-bottom: .48em;
    color: white;
    background: radial-gradient(rgb(74, 10, 192),rgb(29, 2, 80));
}
</style>
