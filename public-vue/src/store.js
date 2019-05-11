import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // USER DATA
    user: null,
    userData: null,

    // SOUND CONSTANTS
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

    // LEVEL MENUS
    displayedLevels: [],

    // IN GAME DATA
    level: {},
    path: [],
    displayedComments: [],
    displayedPaths: [],
    gameId: "",
  },
  mutations: {
    // USER DATA
    setUser(state, user) {
      state.user = user;
    },
    setUserData(state, userData) {
      state.userData = userData;
    },
    // SOUND DATA
    setSong(state, song) {
      state.song = song;
    },
    // LEVEL MENUS
    setDisplayedLevels(state, displayedLevels) {
      state.displayedLevels = displayedLevels;
    },
    // GAME DATA
    setGameId(state, gameId) {
      state.gameId = gameId;
    },
    setDisplayedComments(state, displayedComments) {
      state.displayedComments = displayedComments;
    },
    setDisplayedPaths(state, displayedPaths) {
      state.displayedPaths = displayedPaths;
    },
    setLevel(state, level) {
      state.level = level;
    },
    setPath(state, path) {
      state.path = path;
    },
  },
  actions: {
    // USER METHODS
    async register(context, data) {
      try {
        let response = await axios.post("/api/users", data);
        context.commit('setUser', response.data);
        return "";
      } catch (error) {
        return error.response.data.message;
      }
    },
    async login(context, data) {
      try {
        let response = await axios.post("/api/users/login", data);
        context.commit('setUser', response.data);
        return "";
      } catch (error) {
        return error.response.data.message;
      }
    },
    async logout(context) {
      try {
        await axios.delete("/api/users");
        context.commit('setUser', null);
        return "";
      } catch (error) {
        return error.response.data.message;
      }
    },
    async getUser(context) {
      try {
        let response = await axios.get("/api/users");
        context.commit('setUser', response.data);
        return "";
      } catch (error) {
        return "";
      }
    },
    // SOUND METHODS
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
    // LEVEL MENU ACTIONS
    async getDisplayed(context, payload) {
      
    },
    // GAME METHODS
    async newLevel(context, payload) {
      
    },
    async saveProgress(context, payload) {

    },
    async reloadProcess(context, payload) {

    },
    async sendMove(context, payload) {

    },
    async deleteLevel(context, payload) {

    },
    async getComments(context, payload) {

    },
    async getPaths(context, payload) {

    }
  }
})
