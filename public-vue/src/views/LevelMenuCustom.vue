<template>
  <div class="levelmenucustom">
    <moving-title-small class="movingTitle" title="Custom Levels"/>
    <LevelMenu msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import LevelMenu from '@/components/LevelMenu.vue'
import MovingTitleSmall from '@/components/MovingTitleSmall.vue'

export default {
  name: 'levelmenucustom',
  components: {
    LevelMenu,
    MovingTitleSmall
  },
  created()
  {
    this.$store.dispatch("changeSong", {song: 0});
  }
}
</script>