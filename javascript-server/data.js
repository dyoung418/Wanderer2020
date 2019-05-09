const axios = require("axios");

const levels = [
    {
        author: "Steven Shipway",

        width: 40,
        height: 17,
    
        map: "=======================\OOO*OOOO/#OO####*O       O:#         O/ \OOOOOO/# ::A**## O #### #:#       **/   \OOOO/   ####### #  O  *#:#              \OO/   ##    -# #* * ###:# OOO           O/    ##    -# ######:::#*****         :/  *###* O  -#    #*                 @     *<*###*< -#*#! ###                  \   *###*    -###              !     ::  \     ##    -# #          \ /=O=   ::::   \O     / O/#*           O O  =    ::   / \*   / */-###         #***# =        /   \    O/ -X < !!!     #\*/# =       /    O*O*O*O ->*   *   *<  # #  =      /     =**O*O= -    !!!   ! !# #! =! \    /    =:O*O:= -          ! *#T#*:::::\**/     =::::::*-########################################",
    
        time: 1000,
        title: "Unplug the Cistern #1",
        solution:
        {
            score: 501,
            movecount: 320,
            moves: "JJJLJHHKKHJJJJJLJJLHKHKHHJJLHHHHHLLLLKKKKKKKKKHHHHHHHHHHKHHJHHLLJJHHHHKKHHHJKLLLJJJHJHHLLJJJLLHHHHJJLLLLLLLLKKKLLJJJLHKKKKKKLKLLJJHJLKLJHJJJJLLHHHHHJHJJHHJJJKLLHHJJLLJJJJJJJLLLLLLHHKHHHKLKJLLKHKLKLKKKKHLKHHHLLJJHHLJJHJHHHKKHKHKHHHKKHLLKKKKJJJJHHHHHHHKKHHJJJHHHHHHJHHKKKKKHHHHHHHJJJLLLKLLHHHHHKKHLHHHLJJJJJLLLJJJHJJJHJHHK",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 1,
    },
    {
        author: "Steven Shipway",

        width: 40,
        height: 17,
    
        map: "C      O  OOO ##       \OOO*OOOO/    O *       *       *#       \OOOOOO/ >     A#!        /    #         \OOOO/        -  O    /         O      *<\OO/  =*==\  -\O<   /          :        :O/!!!    O\*/>O   /                     /        := -#O\ /                              = * -#O          /   @         \         ====#O         /    O    *<    \           -**              :            /         -====/                       /          -       \                   /           -X!   \ *\                 /            -!    /!!!*/!!!!!/*<      /   *         ->*   \!!!/         !!\    /            -*      *             *\ */T            *########################################",
    
        time: 350,
        title: "Unplug the Cistern #2",
        solution:
        {
            score: 239,
            movecount: 323,
            moves: "KKKLHHHKKKLHJJLLLLLLLLLLJHHHHHHJJJJJJJJHHHKHHHHHHJJKKKHHHJJLHKHHJJJJHHHHLLLLLLLLLLLLLLLLLLLLLHHHHKKKKKKHHHHHHHHHKKKKKKKKHHHHJJHHHLKKKHHLLLJJJJJJJJHJLKLLLLJLLLLLLLLLLLLLLKJJJJLLLJJJKKKKKKLLLLKLLLJJJLLLLLLLLJJJJHHHHHHHHHHKKJJHHHKJJJHJJHJHHKHHHKKJJJHHHHHHHKKHLLKKKKJJJJHHHJHHHHHHHHHHHHHHJJHHHHHHHJJLHHHHLLLLLLJJHHHJJJHHKLKKHHJ",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 2,
    },
    {
        author: "Steven Shipway",

        width: 40,
        height: 17,
    
        map: "   ====>*O        O<           /O:     - *       :*      *<    /        *<     O##<      /                  *<\       O/*                           O<       O/*######## #\ ###            OO====== O/ OAOO*OOO/*<<#               */     **/ */\OO!OO/: *#      /\      O#:   *   /   -*\OOO/::\*      /#O\ /   :#\      /    -  \O/ @  *     /O*<#* OO#   \    /    \-* :::   *      #O<  ##\O#    \**/     !* ::/:O#       # O *    : */   ><      !!  /# *       :##O## ######O \          *  ###\     ::::#O#: :::::::::#####::####::OOO#   ::::#:::::/>>::O  /##O*O:*::O*O::*OOO ::::!:#*## ##/*<!!  #!*O:*::O:*:**::::*O::::::#:#*>T*      X# O:*::*::O:*########################################",
    
        time: 750,
        title: "My Favorite One of the Lot - Steve",
        solution:
        {
            score: 566,
            movecount: 459,
            moves: "LLLKKJJJHJJJJJHJLLLLLKKKHJHJHKKKKKHHHHHHHHHKKJJJLJJJJLHHKJJLLLLLLKKKKHHKKHHJKLLHLHLLKLKLKLKKKHHHHHHHHLLKKHLLLLLLLKJLLLLLLLLJLLLLJJJJJJKKKKKKLLLLLLLLKLLLJLLLKKHJHLJJLLJJHHHJHJJJHKKHKHHKHHHHHHHHHHKKKKJJJHJJHJHJJHJJJLJJJKKLLLLKLKKHHHLKKJLLJJJLLLLLLLLLHKKKHHJHHLLKLLLJLJLLLLLJJJJLLKLLJLKHKHHHHHJJHHHLKKHJHLLLLLLKKKLLLLHHKKKKLLJJKKKHKHLKLKJHJJJHJJJJHHHHHHHHKHHJJHHHHJHKHJJJKKKLLLLJHHHHJJHHHLLLHJJLJJLLLLLLLKLLKLKLLKLLLLLLLLJLJLHLJJLLJJHJHHHHHHHHJHJJHLLLLLKKLLLLJJL",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 3,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 4,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 5,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 6,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 7,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 8,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 9,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 10,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 11,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 12,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 13,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 14,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 15,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 16,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 17,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 18,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 19,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 20,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 21,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 22,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 23,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 24,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 25,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 26,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 27,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 28,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 29,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 30,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 31,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 32,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 33,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 34,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 35,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 36,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 37,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 38,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 39,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 40,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 41,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 42,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 43,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 44,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 45,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 46,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 47,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 48,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 49,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 50,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 51,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 52,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 53,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 54,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 55,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 56,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 57,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 58,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 59,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 60,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 61,
    },
    {
        author: "AUTHOR",

        width: 40,
        height: 17,
    
        map: "MAP-STRING",
    
        time: NUMBER,
        title: NUMBER,
        solution:
        {
            score: NUMBER,
            movecount: NUMBER,
            moves: "SOLUTION",
        },
    
        likes: 0,
        likedBy: [],
    
        official: 62,
    }
];

levels.forEach(async level => {
  try {
    let response = await axios.post("http://localhost:3000/api/wanderer", image);
  } catch (error) {
    console.log(error);
  }
});