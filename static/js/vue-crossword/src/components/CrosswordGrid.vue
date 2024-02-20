<template>
  <div class="grid">
    <div class="inner">
      <div
        v-for="(row, rowIdx) in gridWidth"
        :key="rowIdx"
        class="row"
      >
        <div class="inner">
          <div
            v-for="(cell, cellIdx) in gridHeight"
            :key="`${cellIdx + 1}:${rowIdx + 1}`"
            :class="['cell', ...getCellClass(rowIdx, cellIdx)]"
          >
            <cell
              :id="`${cellIdx + 1}:${rowIdx + 1}`"
              v-model="answers[`${cellIdx + 1}:${rowIdx + 1}`]"
              :x="cellIdx + 1"
              :y="rowIdx + 1"
              :is-active="active.cell === `${cellIdx + 1}:${rowIdx + 1}`"
              @keyup.exact="onKeyUp"
              @keyup.left.up="onLeftPress"
              @cellclick="onCellClick"
              @cellinput="goNextCell"
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
  name: 'CrosswordGrid',

  components: { Cell },

  props: {
    questions: { type: Object, default: () => ({}) },
  },

  data: () => ({
    answers: {},
    active: {
      cell: '',
      word: [],
      vertical: false,
    },
  }),

  computed: {
    gridWidth () {
      return Math.max(...this.questions.horizontal.map((question) => question.x + question.length)) - 1
    },

    gridHeight () {
      return Math.max(...this.questions.vertical.map((question) => question.y + question.length)) - 1
    },

    letterCells () {
      const cells = []

      this.questions.horizontal.forEach(({ x, y, length }) => {
        for (let i = x; i < length + x; i += 1) {
          cells.push(`${i}:${y}`)
        }
      })

      this.questions.vertical.forEach(({ x, y, length }) => {
        for (let i = y; i < length + y; i += 1) {
          cells.push(`${x}:${i}`)
        }
      })

      return cells
    },

    questionsCells () {
      // eslint-disable-next-line
      return this.startCells
        .sort((a, b) => {
          const aa = a.split(':')
          const bb = b.split(':')

          return Number(aa[1] + aa[0]) - Number(bb[1] + bb[0])
        })
        .unique()
        .map((cell, idx) => ({ cell, idx: idx + 1 }))
    },

    startCells () {
      return this.allStartCells()
    },
  },

  watch: {
    active: {
      handler (val) {
        let key = 0
        let first = document.getElementById(val.word[key])

        while (first.value) {
          key += 1
          first = document.getElementById(val.word[key])
        }

        first.focus()
      },
      deep: true,
    },
  },

  methods: {
    onKeyUp (e) {
      if (e.target.value.match(/[A-Za-zА-Яа-я]/)) {
        return this.goNext(e.target)
      }
      e.currentTarget.value = ''
    },

    onCellClick ({ id }) {
      if (this.isBoth(id)) {
        this.toggleWords(id)
        return
      }

      if (this.isNeither(id)) {
        return
      }

      this.activateWord(id)
    },

    onLeftPress (e) {
      this.goPrev(e.currentTarget)
    },

    getNextId (id) {
      const match = id.match(/(\d+):(\d+)/)
      const last = this.active.word[this.active.word.length - 1]

      const next = this.active.vertical
        ? Number(match[2]) + 1
        : Number(match[1]) + 1

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

      const prev = this.active.vertical
        ? Number(match[2]) - 1
        : Number(match[1]) - 1

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

    capitalize (str) {
      return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
    },

    updateData (key, dir) {
      const word = this[`get${this.capitalize(dir)}Word`](key)

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

    isVertical (cell) {
      return !this.allStartCells('horizontal').includes(this.getHorizontalStartCell(cell)) && this.allStartCells('vertical').includes(this.getVerticalStartCell(cell))
    },

    isHorizontal (id) {
      return !this.allStartCells('vertical').includes(this.getVerticalStartCell(id)) && this.allStartCells('horizontal').includes(this.getHorizontalStartCell(id))
    },

    isBoth (id) {
      return this.allStartCells('vertical').includes(this.getVerticalStartCell(id)) && this.allStartCells('horizontal').includes(this.getHorizontalStartCell(id))
    },

    isNeither (id) {
      return !this.allStartCells('vertical').includes(this.getVerticalStartCell(id)) && !this.allStartCells('horizontal').includes(this.getHorizontalStartCell(id))
    },

    getWordStartCells (id) {
      return this.allStartCells().filter((cell) => cell === id)
    },

    getHorizontalWord (id) {
      id = this.allStartCells('horizontal').includes(id)
        ? id
        : this.getHorizontalStartCell(id)

      return this.collectHorizontalWordCells(this.getHorizontalQuestion(id))
    },

    getVerticalWord (id) {
      id = this.allStartCells('vertical').includes(id)
        ? id
        : this.getVerticalStartCell(id)

      return this.collectVerticalWordCells(this.getVerticalQuestion(id))
    },

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

    collectHorizontalWordCells (question) {
      if (!question) {
        return []
      }

      const cells = []
      let i

      for (i = question.x; i < question.x + question.length; i += 1) {
        cells.push(`${i}:${question.y}`)
      }

      return cells === [] ? null : cells
    },

    collectVerticalWordCells (question) {
      if (!question) {
        return []
      }

      const cells = []
      let i

      for (i = question.y; i < question.y + question.length; i += 1) {
        cells.push(`${question.x}:${i}`)
      }

      return cells === [] ? null : cells
    },

    getVerticalQuestion (id) {
      return this.questions.vertical.find((question) => this.exact(question, id))
    },

    getHorizontalQuestion (id) {
      return this.questions.horizontal.find((question) => this.exact(question, id))
    },

    exact (question, id) {
      const xy = id.split(':')

      return question.x === Number(xy[0]) && question.y === Number(xy[1])
    },

    getCellClass (row, col) {
      const classes = []
      const index = `${col + 1}:${row + 1}`

      classes.push(this.letterCells.includes(index) ? 'letter': 'blank')

      if (this.startCells.includes(index)) {
        classes.push('start')
      }

      if (this.active.word.includes(index)) {
        classes.push('active')
      }

      return classes
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
