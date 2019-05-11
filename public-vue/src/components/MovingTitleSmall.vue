<template>
<div id="movingtitlelarge">
    <div class="title-div">
        <h1 @mouseover="hover()" v-bind:class="{space : (char.space)}" v-for="char in chars" v-bind:key="char.id">{{char.c}}</h1>
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
            var next = false;
            for (var i = 0; i < this.title.length; i++)
            {
                var charObject = {c: this.title.charAt(i), id: i, space: 0};
                if (next)
                {
                    charObject.space = 1;
                    next = false;
                }
                if (this.title.charAt(i) == " ")
                {
                    next = true;
                }
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
    height: 5em;
}
.space{
    margin-left: 20px;
}

h1
{
    color: white;
    text-transform: uppercase;
    font-family: 'Francois One', sans-serif;
    margin-top: 0px;
    margin-bottom: 0px;
    font-size: 3em;
    transition: font-size .3s ease-in-out 0s, color .3s ease-in-out 0s;
}

h1:hover
{
    color: rgb(73, 71, 189);
    font-size: 3.5em;
}
</style>
