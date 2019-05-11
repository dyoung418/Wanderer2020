<template>
  <div class="levelmenucustom">
    <moving-title-small class="movingTitle" title="Level Creator"/>
    <LevelMenu tag="usersaved" page="this.$route.params.page"/>  </div>
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