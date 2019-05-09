<template>
<div id="movingtitlelarge">
    <div class="title-div">
        <h1 @mouseover="hover()" v-for="char in chars" v-bind:key="char.id">{{char.c}}</h1>
    </div>
</div>
</template>

<script>
export default {
    name: 'movingtitlelarge',
    props: {
        title: String,
    },
    data()
    {
        return {
            chars: [],
        }
    },
    methods: {
        hover()
        {
            this.$store.dispatch("playSound", {sound: 2, volume: 0});
        },
        fillChar()
        {
            for (var i = 0; i < this.title.length; i++)
            {
                var charObject = {c: this.title.charAt(i), id: i};
                this.chars.push(charObject);
            }
        }
    },
    created()
    {
        this.fillChar();
    },
};
</script>

<style scoped>
.title-div
{
    display: flex;
    justify-content: center;
    margin: 0 auto; 
    width: 100%;
    align-items: stretch;
    height: 11em;
}

h1
{
    color: white;
    text-transform: uppercase;
    margin-top: 0px;
    margin-bottom: 0px;
    font-size: 8em;
    transition: font-size .3s ease-in-out 0s, color .3s ease-in-out 0s;
}

h1:hover
{
    color: rgb(73, 71, 189);
    font-size: 9em;
}
</style>
