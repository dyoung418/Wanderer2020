<template>
<div id="game">
    <div id="board">
        <div v-for="row in height" v-bind:key="row" class="row">
            <div v-for="col in width" v-bind:key="col" class="block">
            </div>
        </div>
    </div>

</div>
</template>

<script>
import moment from 'moment';
export default {
    name: 'game',
    data()
    {
        return {
            width: 40,
            height: 17,
            board: [],
        }
    },
    methods: {
        createEmptyBoard()
        {
            this.height = this.level.height;
            this.width = this.level.width;
            for (var i = 0; i < this.height; i++)
            {
                this.board.push([]);
                for (var j = 0; j < this.width; j++)
                {
                    this.board[i].push("E");
                }
            }
        },
        formatDate(date) {
            if (moment(date).diff(Date.now(), 'days') < 15)
                return moment(date).fromNow();
            else
                return moment(date).format('d MMMM YYYY');
        },
    },
    computed:
    {
        user() {
            if (!this.$store.state.user)
            {
                return this.$store.state.user
            }
            return this.$store.state.user.name;
        },
        level() {
            return this.$store.state.level;
        },
    },
    created()
    {
        this.createEmptyBoard();
    },
};
</script>

<style scoped>

</style>
