<template>
  <div class="builder-grid page-inner">
    <div class="inner">
      <div
        v-for="(row, rowIdx) in gridHeight"
        :key="rowIdx"
        class="row"
      >
        <div class="inner">
          <div
            v-for="(cell, cellIdx) in gridWidth"
            :key="`${cellIdx + 1}:${rowIdx + 1}`"
            :class="['cell', ...getCellClass(rowIdx, cellIdx)]"
            :style="getCellStyle(rowIdx, cellIdx)"
          >
            <cell
              :class="{
                hovered: hoveredCells.includes(`${cellIdx + 1}:${rowIdx + 1}`),
                red: twoLetterWords.includes(`${cellIdx + 1}:${rowIdx + 1}`),
                yellow: threeLetterWords.includes(`${cellIdx + 1}:${rowIdx + 1}`),
              }"
              :value="letters[`${cellIdx + 1}:${rowIdx + 1}`]"
              :x="cellIdx + 1"
              :y="rowIdx + 1"
              :number="getNumber(cellIdx + 1, rowIdx + 1)"
              :is-blank="blanks.includes(`${cellIdx + 1}:${rowIdx + 1}`)"
              :is-active="active.cell === `${cellIdx + 1}:${rowIdx + 1}`"
              @keyup.exact="onKeyUp"
              @keyup.left.up="onLeftPress"
              @cellclick="onCellClick"
              @cellinput="goNextCell"
              @cellmouseup="onMouseUp"
              @cellmousedown="onMouseDown"
              @cellmouseenter="onMouseEnter"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Cell from './Cell'


export default {
  name: 'BuilderGrid',

  components: { Cell },

  props: {
    words: { type: Array, default: () => [] },
    blanks: { type: Array, default: () => [] },
    letters: { type: Object, default: () => ({}) },
    gridWidth: { type: Number, default: () => 1 },
    gridHeight: { type: Number, default: () => 1 },
    filledWords: { type: Array, default: () => [] },
    focusedCell: { type: String, default: () => '0:0' },
    hoveredWord: { type: String, default: () => '0:0:0:0' },
    editGridMode: { type: Boolean, default: () => false },
    twoLetterWords: { type: Array, default: () => [] },
    impossibleWords: { type: Array, default: () => [] },
    threeLetterWords: { type: Array, default: () => [] },
    suggestionCounts: { type: Array, default: () => [] },
  },

  data: () => ({
    dragging: false,
    toBlank: true,
    answers: {},
    active: {
      cell: '',
      word: [],
      vertical: false,
    },
    cells: [],
  }),

  computed: {
    hoveredCells () {
      const [x, y, isVertical, length] = this.hoveredWord.split(':')
      const acc = []

      for (let idx = 0; idx < length; idx += 1) {
        acc.push(`${Number(isVertical) ? x : Number(x) + idx}:${Number(isVertical) ? Number(y) + idx : y}`)
      }

      return acc
    },
  },

  methods: {
    onMouseDown ({ id }) {
      if (!this.editGridMode) {
        return
      }
      this.cells = []
      if (id) {
        this.dragging = true
        if (!this.cells.includes(id)) {
          this.cells.push(id)
        }
        this.toBlank = !this.blanks.includes(id)
        this.$emit('updateblanks', id)
        this.$bus.$emit('changed::ondrag', { id, value: true })
      }
    },

    onMouseUp () {
      if (!this.editGridMode) {
        return
      }
      this.dragging = false
      this.cells.forEach((id) => {
        this.$bus.$emit('changed::ondrag', { id, value: false })
      })
    },

    onMouseEnter ({ id }) {
      if (!this.editGridMode || !this.dragging) {
        return
      }

      if (id) {
        if (this.toBlank !== this.blanks.includes(id)) {
          this.$emit('updateblanks', id)
          this.$bus.$emit('changed::ondrag', { id, value: true })
          if (!this.cells.includes(id)) {
            this.cells.push(id)
          }
        }
      }
    },

    isTitleCell (x, y) {
      return this.words.find((word) => word.x === +x && word.y === +y)
    },

    getNumber (x, y) {
      const titleCell = this.isTitleCell(x, y)

      return titleCell ? titleCell.index : null
    },

    onKeyUp (e) {
      if (e.target.value.match(/[A-Za-zА-Яа-я]/)) {
        return this.goNext(e.target)
      }
      e.currentTarget.value = ''
    },

    onCellClick () {
      // this.$emit('updateblanks', id)
    },

    onLeftPress (e) {
      this.goPrev(e.currentTarget)
    },

    getNextId (id) {
      const match = id.match(/(\d+):(\d+)/)
      const last = this.active.word[this.active.word.length - 1]
      const next = Number(match[Number(this.active.vertical) + 1]) + 1

      if (next > last.split(':')[Number(this.active.vertical)]) {
        return false
      }

      return this.active.vertical
        ? `${match[1]}:${next}`
        : `${next}:${match[2]}`
    },

    getPrevId (id) {
      const match = id.match(/(\d+):(\d+)/)
      const first = this.active.word[0]
      const prev = Number(match[Number(this.active.vertical) + 1]) - 1

      if (prev < first.split(':')[Number(this.active.vertical)]) {
        return false
      }

      return this.active.vertical
        ? `${match[1]}:${prev}`
        : `${prev}:${match[2]}`
    },

    goNextCell ({ id }) {
      const next = this.getNextId(id)

      this.active.cell = next
      // next && next.focus() || el.blur()
      document.execCommand('selectAll')
    },

    goPrevCell ({ id }) {
      const prev = this.getPrevId(id)

      this.active.cell = prev
      // prev && prev.focus() || el.blur()
      document.execCommand('selectAll')
    },

    activateWord (key) {
      let dir

      if (this.isHorizontal(key)) {
        dir = 'horizontal'
      }
      if (this.isVertical(key)) {
        dir = 'vertical'
      }

      return this.updateData(key, dir)
    },

    toggleWords (key) {
      let dir = 'horizontal'

      if (!this.active.word.length) {
        return this.updateData(key, dir)
      }

      if (this.typeOfWord(this.active.word) === 'horizontal') {
        dir = 'vertical'
      }

      return this.updateData(key, dir)
    },

    updateData (key, dir) {
      const word = this[`get${dir.capitalize()}Word`](key)

      if (word === this.active.word) {
        return true
      }

      if (!word) {
        return false
      }

      this.active.word = word
      this.active.cell = word[0]
      this.active.vertical = dir.toLowerCase() === 'vertical'

      return true
    },

    typeOfWord (word) {
      let prev
      let type

      word.forEach((cell) => {
        if (!prev) {
          prev = cell
          return true
        }

        type = prev.split(':')[0] === cell.split(':')[0]
          ? 'vertical'
          : 'horizontal'
      })

      return type
    },

    isVertical (id) {
      return (
        !this.allStartCells('horizontal').includes(this.getHorizontalStartCell(id)) &&
        this.allStartCells('vertical').includes(this.getVerticalStartCell(id))
      )
    },

    isHorizontal (id) {
      return (
        !this.allStartCells('vertical').includes(this.getVerticalStartCell(id)) &&
        this.allStartCells('horizontal').includes(this.getHorizontalStartCell(id))
      )
    },

    isBoth (id) {
      return (
        this.allStartCells('vertical').includes(this.getVerticalStartCell(id)) &&
        this.allStartCells('horizontal').includes(this.getHorizontalStartCell(id))
      )
    },

    isNeither (id) {
      return (
        !this.allStartCells('vertical').includes(this.getVerticalStartCell(id)) &&
        !this.allStartCells('horizontal').includes(this.getHorizontalStartCell(id))
      )
    },

    getWordStartCells (id) {
      return this.allStartCells().filter((cell) => cell === id)
    },

    // getHorizontalWord (id) {
    //   id = this.allStartCells('horizontal').includes(id)
    //     ? id
    //     : this.getHorizontalStartCell(id)

    //   return this.collectHorizontalWordCells(this.getHorizontalQuestion(id))
    // },

    // getVerticalWord (id) {
    //   id = this.allStartCells('vertical').includes(id)
    //     ? id
    //     : this.getVerticalStartCell(id)

    //   return this.collectVerticalWordCells(this.getVerticalQuestion(id))
    // },

    getHorizontalStartCell (id) {
      const xy = id.split(':')

      while (!this.allStartCells('horizontal').includes(id) && xy[0] > 0) {
        xy[0] -= 1
        id = xy.join(':')
      }

      return id
    },

    getVerticalStartCell (id) {
      const xy = id.split(':')

      while (!this.allStartCells('vertical').includes(id) && xy[1] > 0) {
        xy[1] -= 1
        id = xy.join(':')
      }

      return id
    },

    getWordCells (word) {
      let increment = word.type === 'vertical' ? word.y : word.x

      return Array.from({ length: word.length }).map(() => {
        const idx = word.type === 'vertical'
          ? `${word.x}:${increment}`
          : `${increment}:${word.y}`

        increment = increment + 1
        return idx
      })
    },

    // collectHorizontalWordCells (question) {
    //   if (!question) {
    //     return []
    //   }

    //   const cells = []
    //   let idx

    //   for (idx = question.x; idx < question.x + question.length; idx += 1) {
    //     cells.push(`${idx}:${question.y}`)
    //   }

    //   return cells === [] ? null : cells
    // },

    // collectVerticalWordCells (question) {
    //   if (!question) {
    //     return []
    //   }

    //   const cells = []
    //   let idx

    //   for (idx = question.y; idx < question.y + question.length; idx += 1) {
    //     cells.push(`${question.x}:${idx}`)
    //   }

    //   return cells === [] ? null : cells
    // },

    // getVerticalQuestion (id) {
    //   return this.questions.vertical.find((question) => this.exact(question, id))
    // },

    // getHorizontalQuestion (id) {
    //   return this.questions.horizontal.find((question) => this.exact(question, id))
    // },

    exact (question, id) {
      const xy = id.split(':')

      return question.x === Number(xy[0]) && question.y === Number(xy[1])
    },

    getCellClass (row, col) {
      const classes = []
      const index = `${col + 1}:${row + 1}`

      classes.push(this.blanks.includes(index) ? 'blank' : 'letter')

      if (this.$root.getAllWordCells(this.filledWords).includes(index)) {
        classes.push('filled')
      }

      if (index === this.focusedCell) {
        classes.push('focused')
      }

      if (this.impossibleWords.includes(index)) {
        classes.push('error')
      }

      return classes
    },

    getCellStyle () {
      // return {
      //   background: this.getCellWeigth(row, col)
      //     .toString(16) // eslint-disable-line no-magic-numbers
      //     .padStart(6, 'ffffff'), // eslint-disable-line no-magic-numbers
      // }
    },

    getCellWeigth () {
      return this.words.reduce((word) => Array.from({ length: word.length })
        .map(() => word.type === 'vertical'))
    },

    allStartCells (direction = null) {
      const cells = []

      if (!direction || direction === 'horizontal') {
        this.questions.horizontal.forEach((question) => {
          cells.push(`${question.x}:${question.y}`)
        })
      }

      if (!direction || direction === 'vertical') {
        this.questions.vertical.forEach((question) => {
          cells.push(`${question.x}:${question.y}`)
        })
      }

      return cells
    },
  },
}
</script>
