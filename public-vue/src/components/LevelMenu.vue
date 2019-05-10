<template>
<div id="levelmenu">
    <h1 class="sticky">{{chat}}</h1>
    <div id="levelList">
        <div class="level-div" v-for="level in displayed" v-bind:key="level.title">
            <p v-if="isOriginal == 1" class="level-number">{{level.num}}</p>

            <p class="level-title">{{level.title}}</p>
            <p class="level-author">{{level.author}}</p>
            
            <p v-if="isOriginal != 1" class="level-date">{{formatDate(chat.created)}}</p>
        </div>
    </div>
    <div id="nav-menu">
    
    </div>


</div>
</template>

<script>
import moment from 'moment';
export default {
    name: 'levelmenu',
    props: {
        page: Number,
        levels: Array,
        isOriginal: Number,
    },
    data()
    {
        return {
            displayed: [],
        }
    },
    methods: {
        formatDate(date) {
            if (moment(date).diff(Date.now(), 'days') < 15)
                return moment(date).fromNow();
        else
            return moment(date).format('d MMMM YYYY');
        },
        computeLevels()
        {
            this.displayed = [];
            for (var i = 0; i < 9; i++)
            {
                console.log(this.levels);
                if (this.isOriginal) this.levels[i + ((this.page - 1) * 9)].num = (i + ((this.page - 1) * 9));
                this.displayed.push(this.levels[i + ((this.page - 1) * 9)]);
            }

        },
        toStart()
        {
            if (this.page != 1)
            {
                this.page = 1;
                this.computeLevels();
            }
            else this.err();
        },
        toPrevious()
        {
            if (this.page != 1)
            {
                this.page -= 1;
                this.computeLevels();
            }
            else this.err();
        },
        toEnd()
        {
            if (this.page != pageSize())
            {
                this.page = this.pageSize();
                this.computeLevels();
            }
            else this.err();
        },
        toNext()
        {
            if (this.page != pageSize())
            {
                this.page += 1;
                this.computeLevels();
            }
            else this.err();
        },
        err()
        {
            this.$store.dispatch("playSound", {sound: 2, volume: 0});
        }
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
        pageSize()
        {
            return Math.ceil(this.levels.length / 9);
        }
    },
    created()
    {
        this.computeLevels();
    },
};
</script>

<style scoped>
.studentChat
{
    margin-right: auto !important;
}

.userChat
{
    margin-left: auto !important;
    background: rgba(75, 135, 224, 0.3) !important;
}

#inputDiv
{
    display: flex;
    justify-content: space-around;
    position: fixed;
    width: 83.5%;
    bottom: 0px;
    padding: 30px;
    background-color: rgba(32, 34, 37, 08);
}
#inputBox
{
    display: block;
    width: 80%;
    background: radial-gradient(rgb(58, 62, 70), rgb(60, 65, 70));
    color: white;
    border: 0px;
    padding: 10px;
    border-radius: 10px; 
}
#sendButton
{
    display: block;
    background: radial-gradient(rgb(47, 68, 107), rgb(35, 70, 105));
    color: white;
    border: 0px;
    width: 100px;
    height: 50px;
    border-radius: 10px; 
}
#chatList
{
    display: block;
    width: 90%;
    height: 100%;
    padding: 30px;
    margin: 0 auto;
}

#relative
{
    position: relative;
    width: 100%;
    height: 100%;
}
h2{
    margin: 0 auto;
    margin-top: 10px;
    display: block;
    padding: 5px;
    border-radius: 4px;
    color: white;
    background: rgba(75, 135, 224, 0.3) !important;
    font-size: 100%;
    text-align: center;
    width: 200px;
}
h1
{
    color: rgb(212, 212, 212);
    text-align: left;
    padding-left: 20px;
    width: 100%;
    background: rgb(78, 85, 92);
    font-size: 200%;
    font-weight: lighter;
    margin: 0px;
    padding: 10px;
}
#account{
    color: rgb(126, 126, 126);
    background: rgba(0,0,0,0);
    font-size: 150%;
    text-align: center;
}
#account:hover
{
    color: rgb(223, 223, 223);
    text-align: center;
}

.chatBox
{
  border-radius: 10px;
  display: block;
  background: rgba(231, 231, 231, 0.3);
  width: 30%;
  margin-top: 15px;
  padding: 10px;
}
.chatText
{
    margin: 0px;
    color: rgb(32, 32, 32);
}
.chatUser
{
  color: rgba(211, 211, 211, 0.699);
  font-weight: bold;
  font-size: 75%;
  display: block;
  width: 100%;
  text-align: right;
  margin: 0px;
}
.chatDate
{
  color: rgba(190, 190, 190, 0.692);
  font-size: 75%;
display: block;
  width: 100%;
  text-align: right;
  margin: 0px;
}



</style>
