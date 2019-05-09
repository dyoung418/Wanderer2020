<template>
  <div class="level">
    <Game level="1"/>
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