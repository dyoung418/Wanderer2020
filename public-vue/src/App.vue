<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
      <router-link to="/account">Account</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css?family=Francois+One');

html
{
  display: block;
  width: 100%;
  height: 100%;
  background-image: url("./assets/back.png");
  background-size: contain;
  background-repeat: repeat;
  padding-bottom: 30px;
  color: white;
  font-family: 'Francois One', sans-serif;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#nav {
  padding: 20px;
  font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  width: 90%;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  background: radial-gradient(rgba(40, 29, 82,0),rgba(13, 12, 43, 0));
  
}

#nav a {
  font-weight: bold;
  text-transform: uppercase; 
  text-decoration: none;
  color: rgb(131, 131, 131);
}

#nav a:hover {
  color: rgb(198, 191, 255);
}

#nav a.router-link-exact-active {
  color: rgb(223, 223, 223);
}
</style>
