class BlockPosition {
    constructor(inputRow, inputCol)
    {
        this.row = inputRow;
        this.col = inputCol;
    }

    getRow()
    {
        return this.row;
    }

    getCol()
    {
        return this.col;
    }

    getId()
    {
        var string = "";
        if (this.row < 10)
        {
            string += "0";
        }
        string += this.row;
        string += "-";
        if (this.col < 10)
        {
            string += "0";
        }
        string += this.col;
        return string;
    }
}

var app = new Vue({
    el: '#app',
    data:
    {
        
    },
    methods:
    {
        
    },
    computed:
    {

    },
    created()
    {

    }
});