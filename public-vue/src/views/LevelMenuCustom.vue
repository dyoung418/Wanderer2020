<template>
  <div class="levelmenucustom">
    <LevelMenu msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import LevelMenu from '@/components/LevelMenu.vue'

export default {
  name: 'levelmenucustom',
  components: {
    LevelMenu
  },
  created()
  {
    this.$store.dispatch("changeSong", {song: 0});
  }
}
</script>