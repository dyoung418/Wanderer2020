<template>
  <div class="level">
    <Game/>
  </div>
</template>

<script>
// @ is an alias to /src
import Game from '@/components/Game.vue'

export default {
  name: 'level',
  components: {
    Game
  },
  created()
  {
    this.$store.dispatch("changeSong", {song: 1});
  }
}
</script>