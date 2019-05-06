var app = new Vue({
    el: '#app',
    data:
    {
        
    },
    methods:
    {
        async sendMove() {
            let payload = {key: "r"};
            let res = axios.put('/wanderer/', payload);
            this.updateBoard(res.data);
        },
        updateBoard(data)
        {
            for (var i = 0; i < data.updates.length; i++)
            {
                for (var j = 0; j < data.updates[i].length; j++)
                {
                    var id = this.getId(data.updates[i][j].row, data.updates[i][j].col);
                    var element = document.getElementById(id);
                    if (data.updates[i][j].add != "")
                    {
                        element.classList.add(data.updates[i][j].add);
                    }
                    if (data.updates[i][j].sub != "")
                    {
                        if (element.classList.contains(data.updates[i][j].sub))
                        {
                            element.classList.remove(data.updates[i][j].sub);
                        }
                    }
                }
            }
        },
        getId(row, col)
        {

        },
        newLevel(level)
        {
            let payload = {level: level};
        }
    },
    computed:
    {

    },
    created()
    {
        let res = axios.post('/wanderer/', payload);
    }
});