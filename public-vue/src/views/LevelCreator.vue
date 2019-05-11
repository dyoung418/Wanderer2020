<template>
  <div class="levelmenucustom">
    <moving-title-small class="movingTitle" title="Level Creator"/>
    <div v-if="user" class="account">
        <LevelMenu tag="usersaved" page="this.$route.params.page"/>
    </div>
    <not-logged-in v-else/>
  </div>
</template>

<script>
// @ is an alias to /src
import LevelMenu from '@/components/LevelMenu.vue'
import LevelCreator from '@/components/LevelCreator.vue'
import MovingTitleSmall from '@/components/MovingTitleSmall.vue'

import NotLoggedIn from '@/components/NotLoggedIn.vue'

export default {
  name: 'levelmenucustom',
  components: {
    LevelMenu,
    MovingTitleSmall,
    NotLoggedIn
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
  created()
  {
    this.$store.dispatch("changeSong", {song: 0});
  }
}
</script>