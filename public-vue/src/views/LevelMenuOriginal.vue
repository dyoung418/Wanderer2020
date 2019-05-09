<template>
  <div class="levelmenuoriginal">
    <LevelMenu levels="originalLevels" page="this.$route.params.page" isOriginal="1"/>
  </div>
</template>

<script>
// @ is an alias to /src
import LevelMenu from '@/components/LevelMenu.vue'

export default {
  name: 'levelmenuoriginal',
  props: {
  },
  components: {
    LevelMenu
  },
  created()
  {
    this.$store.dispatch("changeSong", {song: 0});
  },
  data() {
    return {
    originalLevels: [
      {
          time: 1000,
          author: "Steven Shipway",
          title: "Unplug the Cistern #1",
      },
      {
          time: 350,
          author: "Steven Shipway",
          title: "Unplug the Cistern #2",
      },
      {
          time: 750,
          author: "Steven Shipway",
          title: "My Favorite One of the Lot - Steve",
      },
      {
          time: -1,
          author: "Steven Shipway",
          title: "Hanging by a Thread",
      },
      {
          time: 750,
          author: "James Beckett",
          title: "Untitled",
      },
      {
          time: 750,
          author: "James Beckett",
          title: "Yet Another Beckett Screen",
      },
      {
          time: -1,
          author: "Steven Shipway",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Steven Shipway",
          title: "Untitled",
      },
      {
          time: 2001,
          author: "Kenton Oatley",
          title: "Untitled",
      },
      {
          time: 25,
          author: "Steven Shipway",
          title: "Meet the Baby Monsters!",
      },
      {
          time: -1,
          author: "play@nl.cwi",
          title: "play@nl.cwi is Responsible for this Mess",
      },
      {
          time: -1,
          author: "Steven Shipway",
          title: "Get a Load of this One Then",
      },
      {
          time: -1,
          author: "Unknown",
          title: "Return of the Dutch Designer",
      },
      {
          time: -1,
          author: "Unknown",
          title: "Is There No Stopping these Dutchmen?  They'll be Flying Next.",
      },
      {
          time: 70,
          author: "Bruce Butterfield and Son",
          title: "The Aussies Start to Move In",
      },
      {
          time: 50,
          author: "Steven Shipway",
          title: "All but the One",
      },
      {
          time: -1,
          author: "David",
          title: "Untitled",
      },
      {
          time: 25,
          author: "Bruce Butterfield and Son",
          title: "And Another Offering from Oz",
      },
      {
          time: -1,
          author: "Unknown",
          title: "More from the Netherlands",
      },
      {
          time: -1,
          author: "Unknown",
          title: "And Still More.",
      },
      {
          time: 0,
          author: "Shaun Flisakowski",
          title: "Max Moves In",
      },
      {
          time: -1,
          author: "Hugo Wouters",
          title: "And Then Moves Out Again",
      },
      {
          time: -1,
          author: "Steven Shipway",
          title: "Introducing THE BALLOONS!",
      },
      {
          time: -1,
          author: "Steven Shipway",
          title: "The Shrine of Quetzacoatl",
      },
      {
          time: -1,
          author: "Will Bent",
          title: "Untitled",
      },
      {
          time: 5000,
          author: "Steven Shipway",
          title: "Revitalization of the Dutch",
      },
      {
          time: -1,
          author: "Kenton Oatley",
          title: "Revived from the Dead",
      },
      {
          time: -1,
          author: "Frans Meulenbrooks",
          title: "Untitled",
      },
      {
          time: 17,
          author: "Kenton Oatley",
          title: "Kenton's Swan Song",
      },
      {
          time: -1,
          author: "Unknown",
          title: "Who's is it?",
      },
      {
          time: 500,
          author: "Alan Bland",
          title: "Alan Bland did this and the Amiga Port",
      },
      {
          time: 200,
          author: "Ed Strong",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Mark Maplethorpe",
          title: "Untitled",
      },
      {
          time: 200,
          author: "David Goodenough",
          title: "Cause and Effect",
      },
      {
          time: 1000,
          author: "Mark Maplethorpe",
          title: "The Combination Lock",
      },
      {
          time: -1,
          author: "Kevin Pickard",
          title: "Untitled",
      },
      {
          time: 700,
          author: "Paul Metcalf",
          title: "Labyrinth #1",
      },
      {
          time: 300,
          author: "Paul Metcalf",
          title: "Temptation",
      },
      {
          time: 0,
          author: "Paul Metcalf",
          title: "The Water System",
      },
      {
          time: 1000,
          author: "Bill Martin",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Bruce Butterfield and Son",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Bruce Butterfield and Son",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Bryan Ewbank",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Hans Bodlaender",
          title: "Untitled",
      },
      {
          time: 300,
          author: "Mark Sergent",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Hugo Wouters",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Shaun Flisakowski (modified a Hugo)",
          title: "Untitled",
      },
      {
          time: 600,
          author: "Kevin O'Donnell and Tony Newell",
          title: "Untitled",
      },
      {
          time: 50,
          author: "Paul White",
          title: "Untitled",
      },
      {
          time: 95,
          author: "Bill Martin",
          title: "Untitled",
      },
      {
          time: 90,
          author: "Bill Martin",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Hugo Wouters",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Bill Martin",
          title: "Untitled",
      },
      {
          time: 60,
          author: "Hugo Wouters",
          title: "Untitled",
      },
      {
          time: 3000,
          author: "Hans Bodlaender",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Hans Bodlaender",
          title: "Untitled",
      },
      {
          time: 200,
          author: "Danny Young",
          title: "Sneaking Around the Corner",
      },
      {
          time: -1,
          author: "Ronald Lamprecht",
          title: "Untitled",
      },
      {
          time: -1,
          author: "Ronald Lamprecht",
          title: "Untitled",
      },
      {
          time: 500,
          author: "Unknown",
          title: "Untitled",
      },
      {
          time: 0,
          author: "Shaun Flisakowski",
          title: "Untitled",
      },
      {
          time: 0,
          author: "Danny Young",
          title: "Untitled",
      },
    ],
    }
  }
}
</script>