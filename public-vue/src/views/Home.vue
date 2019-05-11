<template>
  <div class="home">
    <moving-title-large class="movingTitle" title="Wanderer"/>
    <main-menu-button class="mainMenuButton" label="Original Levels" route="/levelmenu/original/1" sound="click"/>
    <main-menu-button class="mainMenuButton" label="Custom Levels" route="/levelmenu/custom/1" sound="click"/>
    <main-menu-button class="mainMenuButton" label="Create" route="/levelmenu/custom/1" sound="click"/>
  </div>
</template>

<script>
// @ is an alias to /src
import MainMenuButton from '@/components/MainMenuButton.vue'
import MovingTitleLarge from '@/components/MovingTitleLarge.vue'

export default {
  name: 'home',
  components: {
    MainMenuButton,
    MovingTitleLarge
  },
  created()
  {
    this.$store.dispatch("changeSong", {song: 0});
  }
}
</script>

<style scoped>
.movingTitle
{
  margin-top: 2%;
}
.mainMenuButton
{
  margin-top: 30px;
}
</style>