<template>
  <div class="crossword">
    <crossword-grid :questions="questions" />
    <questions-list />
  </div>
</template>

<script>
import CrosswordGrid from './CrosswordGrid'
import QuestionsList from './QuestionsList'


export default {
  name: 'CrosswordPage',

  components: { CrosswordGrid, QuestionsList },

  data: () => ({
    questions: {
      horizontal: [
        { x: 1, y: 1, length: 4, question: 'Question text?' },
        { x: 6, y: 1, length: 5, question: 'Question text?' },
        { x: 1, y: 2, length: 7, question: 'Question text?' },
        { x: 9, y: 2, length: 2, question: 'Question text?' },
        { x: 3, y: 3, length: 8, question: 'Question text?' },
        { x: 1, y: 4, length: 6, question: 'Question text?' },
        { x: 8, y: 4, length: 3, question: 'Question text?' },
        { x: 3, y: 5, length: 5, question: 'Question text?' },
        { x: 1, y: 6, length: 6, question: 'Question text?' },
        { x: 8, y: 6, length: 3, question: 'Question text?' },
      ],
      vertical: [
        { x: 1, y: 1, length: 6, question: 'Question text?' },
        { x: 1, y: 8, length: 3, question: 'Question text?' },
      ],
    },
  }),
}
</script>

<style lang="stylus">
.crossword
  text-align left
</style>
