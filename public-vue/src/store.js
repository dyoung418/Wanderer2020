import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    userData: null,
    MUSIC: [
      {tag: "song11", volume: 0.3},
      {tag: "song04", volume: 0.1},
      {tag: "song25", volume: 0.1},
    ],
    song: 0,
    SOUNDS: [
      {tag: "click", volume: 0.05},
      {tag: "back", volume: 0.05},
      {tag: "hover", volume: 0.25},
      {tag: "err", volume: 0.05},
      {tag: "monsterdeath", volume: 0.1},
      {tag: "level-start", volume: 0.2},
    ],
    displayedLevels: [],
    displayedComments: [],
    level: {},
    gameId: "",
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setUserData(state, userData) {
      state.userData = userData;
    },
    setSong(state, song) {
      state.song = song;
    },
    setDisplayed(state, displayedLevels) {
      state.displayedLevels = displayedLevels;
    },
    setDisplayedComments(state, displayedComments) {
      state.displayedComments = displayedComments;
    },
    setLevel(state, level) {
      state.level = level;
    },
    setGameId(state, gameId) {
      state.gameId = gameId;
    }
  },
  actions: {
    playSound(context, payload)
    {
      try {
        var media = document.getElementById(this.state.SOUNDS[payload.sound].tag);
        if (payload.volume == 0)
        {
            media.volume = this.state.SOUNDS[payload.sound].volume;
        }
        else
        {
            media.volume = payload.volume;
        }
        const playPromise = media.play();
        if (playPromise !== null) 
            playPromise.catch(() => {media.play();})
      } catch (error) {
        console.log(error);
      }
    },
    changeSong(context, payload)
    {
      try{
        var media = document.getElementById(this.state.MUSIC[this.state.song].tag);
        var playPromise = media.pause();

        context.commit('setSong', payload.song);

        media = document.getElementById(this.state.MUSIC[this.state.song].tag);
        media.volume = this.state.MUSIC[this.state.song].volume;
        playPromise = media.play();
        if (playPromise !== null){
          playPromise.catch(() => { media.play(); })
        }
      } catch(error)
      {
        console.log(error);
      }
    },
  }
})
