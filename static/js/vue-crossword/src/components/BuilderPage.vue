<template>
  <div class="page builder-page">
    <div class="toolbox">
      <button
        v-if="editGridMode"
        :class="{ editing: editGridMode }"
        class="btn"
        @click.prevent="switchLang"
      >
        {{ this.lang }}
      </button>
      <button
        :class="{ editing: editGridMode }"
        class="btn"
        @click.prevent="changeSizeClick"
      >
        {{ editGridMode ? 'Fill Words' : 'Edit Grid' }}
      </button>
      <button
        v-if="editGridMode"
        class="btn"
        @click.prevent="generateGrid(
          horizontalSym,
          verticalSym,
          blankProbability
        )"
      >
        Generate Grid
      </button>
      <button
        v-if="editGridMode"
        :class="{ editing: horizontalSym }"
        class="btn"
        @click.prevent="horizontalSymetria"
      >
        Horizontal Symetria
      </button>
      <button
        v-if="editGridMode"
        :class="{ editing: verticalSym }"
        class="btn"
        @click.prevent="verticalSymetria"
      >
        Vertical Symetria
      </button>
      <button
        v-if="editGridMode"
        class="btn"
        @click.prevent="clearGrid"
      >
        Clear Grid
      </button>
      <button
        class="btn"
        @click.prevent="newCrossword"
      >
        Create New Crossword
      </button>
      <button
        class="btn"
        @click.prevent="saveCrossword"
      >
        Save Crossword
      </button>
      <button
        class="btn"
        @click.prevent="saveGrid"
      >
        Save Grid
      </button>
      <button
        v-if="!editGridMode"
        class="btn"
        @click.prevent="refreshSuggestions"
      >
        Refresh Suggestions
      </button>
      <button
        v-if="!editGridMode"
        :class="{ editing: autoFillMode }"
        class="btn"
        @click.prevent="toggleAutoFill"
      >
        Auto Fill
      </button>
      <button
        v-if="editGridMode"
        class="btn"
        @click.prevent="rotateGrid({ width, height, blanks })"
      >
        Rotate Grid
      </button>
      <div class="statistics">
        <pre
          v-html="statsView.replace(
            /^\s*(2-letters words: \d+ items)/,
            '<span class=\'red\'>$1</span>'
          )"
        ></pre>
      </div>
      <div class="log">
        <pre>
          {{ log }}
        </pre>
      </div>
      <transition name="slide-left">
        <div
          v-if="editGridMode"
          class="grid-list"
          transition="slide-left"
        >
          <grid-preview
            v-for="grid in grids"
            :key="grid.id"
            :grid="grid"
            @loadgrid="loadGrid"
          />
        </div>
      </transition>
    </div>

    <builder-form
      :size="{ width, height }"
      :clues="clues"
      :words="words"
      :letters="letters"
      :loading="loading"
      :init-height="height"
      :grid-name="gridName"
      :next-query="nextQuery"
      :suggestions="suggestions"
      :filled-words="filledWords"
      :focused-cell="focusedCell"
      :change-size-mode="editGridMode"
      :two-letter-words="twoLetterWords"
      :three-letter-words="threeLetterWords"
      :suggestion-counts="suggestionCounts"
      @input="inputLetter"
      @rebuild="rebuildGrid"
      @changesize="changeSize"
      @changename="changeName"
      @focus-cell="focusCell"
      @paste-word="pasteWord"
      @paste-clue="pasteClue"
      @density="changeDensity"
      @form-leaved="wordLeave"
      @remove-word="removeWord"
      @form-hovered="wordHover"
      @letters-update="lettersUpdate"
    />

    <transition name="slide-right">
      <builder-grid
        ref="grid"
        :words="words"
        :blanks="blanks"
        :letters="letters"
        :grid-name="gridName"
        :grid-width="width"
        :grid-height="height"
        :filled-words="filledWords"
        :focused-cell="focusedCell"
        :hovered-word="hoveredWord"
        :edit-grid-mode="editGridMode"
        :two-letter-words="twoLetterWords"
        :impossible-words="impossibleWords"
        :three-letter-words="threeLetterWords"
        :suggestion-counts="suggestionCounts"
        @updateblanks="blanksUpdate"
      />
    </transition>
  </div>
</template>

<script lang="es6">
/* eslint-disable no-loop-func */
import nouns from '../resources/nouns'
import adjectives from '../resources/adjectives'

import BuilderGrid from './BuilderGrid'
import BuilderForm from './BuilderForm'
import GridPreview from './GridPreview'

export default {
  name: 'BuilderPage',

  components: { BuilderForm, BuilderGrid, GridPreview },

  data: () => ({
    log: [],
    lang: 'ru',
    clues: [],
    grids: [],
    width: 15,
    height: 15,
    blanks: [],
    letters: {},
    loading: false,
    gridName: '',
    prevWord: null,
    filledWords: [],
    suggestions: [],
    crosswordId: null,
    focusedCell: '0:0',
    hoveredWord: '0:0:0',
    autoFillMode: false,
    editGridMode: true,
    // eslint-disable-next-line no-magic-numbers
    blankProbability: 1 / 3,
    suggestionCounts: [],
    verticalSym: true,
    horizontalSym: true,
  }),

  computed: {
    statsView () {
      return Object.keys(this.statistics).map((key) => {
        const wordLength = Number(key.replace(/^l/, ''))
        const wordsCount = this.statistics[key].length

        return `${wordLength}-letters words: ${wordsCount} items`
      })
        .sort((a, b) => parseInt(a) - parseInt(b))
        .join('<br>')
    },

    statistics () {
      return this.words.reduce((acc, word) => {
        acc[`l${word.length}`] = acc[`l${word.length}`] || []
        acc[`l${word.length}`].push(word)
        return acc
      }, {})
    },

    horizontalWords () {
      const words = []
      let row = 1

      for (row; row <= this.height; row += 1) {
        const rowBlankCells = this.blanks
          .filter((cell) => Number(cell.split(':')[1]) === row)
          .map((cell) => Number(cell.split(':')[0]))

        if (rowBlankCells.length > 0) {
          const cols = Array.from({ length: this.width }).map((el, idx) => idx + 1)

          if (cols) {
            `:${cols.join('::')}:`
              .split(new RegExp(`:${rowBlankCells.join(':|:')}:`))
              .filter((word) => {
                const match = word.match(/:\d+:/g)

                return match ? match.length > 1 : false
              })
              .forEach((word) => {
                const match = word.match(/:\d+:/g)
                const length = match ? match.length : 0
                const x = Number(word.match(/^:(\d+)/)[1])

                words.push({
                  x,
                  y: row,
                  type: 'horizontal',
                  length,
                  question: '',
                  query: this.$root.getWordCells({
                    x,
                    y: row,
                    word: { length },
                    isVertical: false,
                  }).map((idx) => this.letters[idx] || '_')
                    .join(''),
                })
              })
          }
        }
        else {
          words.push({
            x: 1,
            y: row,
            type: 'horizontal',
            length: this.width,
            question: '',
            query: this.$root.getWordCells({
              x: 1,
              y: row,
              word: { length: this.width },
              isVertical: false,
            }).map((idx) => this.letters[idx] || '_')
              .join(''),
          })
        }
      }

      return words
    },

    verticalWords () {
      const words = []
      let col = 1

      for (col; col <= this.width; col += 1) {
        const colBlankCells = this.blanks
          .filter((cell) => Number(cell.split(':')[0]) === col)
          .map((cell) => Number(cell.split(':')[1]))

        if (colBlankCells.length > 0) {
          const rows = Array.from({ length: this.height }).map((el, idx) => idx + 1)

          if (rows) {
            `:${rows.join('::')}:`
              .split(new RegExp(`:${colBlankCells.join(':|:')}:`))
              .filter((word) => {
                const match = word.match(/:\d+:/g)

                return match ? match.length > 1 : false
              })
              .forEach((word) => {
                const match = word.match(/:\d+:/g)
                const length = match ? match.length : 0
                const y = Number(word.match(/^:(\d+)/)[1])

                words.push({
                  x: col,
                  y,
                  type: 'vertical',
                  length,
                  question: '',
                  query: this.$root.getWordCells({
                    x: col,
                    y,
                    word: { length },
                    isVertical: true,
                  }).map((idx) => this.letters[idx] || '_')
                    .join(''),
                })
              })
          }
        }
        else {
          words.push({
            x: col,
            y: 1,
            type: 'vertical',
            length: this.height,
            question: '',
            query: this.$root.getWordCells({
              x: col,
              y: 1,
              word: { length: this.height },
              isVertical: true,
            }).map((idx) => this.letters[idx] || '_')
              .join(''),
          })
        }
      }

      return words.sort((a, b) => a.y - b.y)
    },

    words () {
      return this.addIndexes([
        ...this.horizontalWords,
        ...this.verticalWords,
      ])
    },

    impossibleWords () {
      const emptyQueries = this.suggestionCounts
        .filter(({ count }) => count === 0)
        .map(({ query }) => query)
        .unique()

      return this.words.filter(({ query }) => emptyQueries.includes(query))
        .flatMap(({ x, y, length, type }) => this.$root.getWordCells({
          x,
          y,
          isVertical: type === 'vertical',
          word: { length },
        }))
    },

    twoLetterWords () {
      return this.words.filter(({ length }) => length === 2)
        .flatMap(({ x, y, length, type }) => this.$root.getWordCells({
          x,
          y,
          isVertical: type === 'vertical',
          word: { length },
        }))
    },

    threeLetterWords () {
      // eslint-disable-next-line no-magic-numbers
      return this.words.filter(({ length }) => length === 3)
        .flatMap(({ x, y, length, type }) => this.$root.getWordCells({
          x,
          y,
          isVertical: type === 'vertical',
          word: { length },
        }))
    },

    sortedByCounts () {
      return Array.from(this.suggestionCounts)
        .sort((a, b) => a.count - b.count)
        .filter((obj) => obj && obj.count > 0 && obj.query.includes('_'))
    },

    nextQuery () {
      return this.sortedByCounts[0] && this.sortedByCounts[0].query
    },

    queries () {
      return this.words.map(({ query }) => query.match(/^[A-Z]+$/) ? null : query)
        .filter(Boolean)
        .unique()
    },

    startCells () {
      return [
        ...this.horizontalWords,
        ...this.verticalWords,
      ]
        .map((word) => ({
          x: word.x,
          y: word.y,
        }))
        .reduce((acc, cur) => {
          if (!acc.find(({ x, y }) => x === cur.x && y === cur.y)) {
            acc.push(cur)
          }
          return acc
        }, [])
        .sort((a, b) => a.y === b.y ? a.x - b.x : a.y - b.y)
        .map((word, index) => ({ ...word, index: index + 1 }))
    },

    letterCells () {
      const cells = []
      let col = 1

      for (col; col <= this.width; col += 1) {
        let row = 1

        for (row; row <= this.height; row += 1) {
          if (this.blanks.includes(`${col}:${row}`)) {
            continue
          }
          cells.push({ x: col, y: row })
        }
      }

      return cells.reduce((acc, { x, y }) => {
        acc[`${x}:${y}`] = ''
        return acc
      }, {})
    },

    locale () {
      return this.lang === 'en' ? 'en/' : ''
    },

    crosses () {
      return [
        ...this.horizontalWords.map(
          ({ x, y, length }) => Array.from(
            { length },
            (el, idx) => `${x + idx}:${y}`,
          ),
        )
          .flat()
          .filter(
            (id) => this.verticalWords.map(
              ({ x, y, length }) => Array.from(
                { length },
                (el, idx) => `${x}:${y + idx}`),
            )
              .flat()
              .indexOf(id) !== -1,
          ),
      ]
    },
  },

  watch: {
    letterCells (value) {
      this.letters = { ...value, ...this.letters }
    },

    blanks () {
      if (this.editGridMode) {
        return
      }
      this.updateSuggestions()
    },

    queries () {
      if (this.editGridMode) {
        return
      }
      this.updateSuggestions()
    },

    allSym (value) {
      if (!this.editGridMode) {
        return
      }
      this.crossSym = value
      this.verticalSym = value
      this.horizontalSym = value
    },
  },

  mounted () {
    this.letters = this.letterCells
    this.updateGrids()

    if (window.location.search && window.location.search !== '?') {
      const { width, height, blanks } = window.location.search
        .replace('?', '')
        .split('&')
        .reduce((acc, cur) => {
          const splitted = cur.split('=')

          acc[splitted[0]] = splitted[1]
          return acc
        }, {})

      if (width) {
        this.width = width
      }
      if (height) {
        this.height = height
      }
      if (blanks) {
        this.blanks = blanks.split(',')
      }
    }
  },

  methods: {
    switchLang () {
      this.lang = this.lang === 'en' ? 'ru' : 'en'
    },

    rotateGrid ({ width, height, blanks }) {
      this.width = height
      this.height = width
      this.blanks = blanks.map((blank) => blank
        .split(':')
        .reverse()
        .join(':'))
    },

    toggleAutoFill () {
      this.autoFillMode = !this.autoFillMode
      if (this.autoFillMode) {
        this.autoFill()
      }
    },

    autoFill () {
      const current = this.suggestions
        .find(({ query }) => query === this.nextQuery)

      if (!current) {
        return
      }

      const word = current.data[this.getRandomInt(current.data.length - 1)]
      const place = this.words
        .find(({ query }) => query === this.nextQuery)

      if (!place) {
        return this.toggleAutoFill()
      }

      const { x, y, type } = place

      this.pasteWord({ word, x, y, isVertical: type === 'vertical' })
    },

    changeName ({ name }) {
      this.gridName = name
    },

    async updateGrids () {
      const response = await fetch('https://crossword.teacherlight.ru:3443/crossword/grids')
      const json = await response.json()

      if (json) {
        this.grids = json
      }
    },

    verticalSymetria () {
      this.verticalSym = !this.verticalSym
    },

    horizontalSymetria () {
      this.horizontalSym = !this.horizontalSym
    },

    wordLeave () {
      this.hoveredWord = '0:0:0:0'
    },

    wordHover ({ x, y, isVertical, length }) {
      this.hoveredWord = `${x}:${y}:${Number(isVertical)}:${length}`
    },

    changeSizeClick () {
      this.editGridMode = !this.editGridMode
      if (!this.editGridMode) {
        this.updateSuggestions()
      }
    },

    removeWord ({ x, y, isVertical, word }) {
      const index = this.filledWords.findIndex((item) => item.x === x &&
        item.y === y && item.isVertical === isVertical)

      this.filledWords.splice(index, 1)
      const keep = this.$root.getAllWordCells(this.filledWords)

      this.$root.getWordCells({ x, y, isVertical, word })
        .forEach((cell) => {
          if (keep.includes(cell)) {
            return
          }
          this.letters[cell] = ''
        })

      this.clues.splice(this.clues.findIndex((clue) => clue.word === word.word), 1)
    },

    refreshSuggestions () {
      this.suggestions = []
      this.suggestionCounts = []
      this.updateSuggestions(true)
    },

    async updateSuggestions (force = false) {
      this.loading = true

      const suggestionCounts = await this.getSuggestionCounts(this.queries, !force)
        .catch((error) => {
          console.log(error)
        })

      if (suggestionCounts.some(({ count }) => count === 0)) {
        this.removeWord(this.prevWord)
        await this.waitForRestart()
        return
      }

      this.suggestionCounts = suggestionCounts

      this.suggestions = await this.getSuggestions(this.queries, !force)
      this.suggestions = this.suggestions.filter(Boolean)

      this.loading = false

      if (this.autoFillMode) {
        return this.autoFill()
      }
    },

    waitForRestart (timeout = 1000) { // eslint-disable-line no-magic-numbers
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(this.autoFill())
        }, timeout)
      })
    },

    generateGrid () {
      this.blanks = []
      let fillWidth
      let fillHeight

      if (this.horizontalSym && this.verticalSym) {
        fillWidth = Math.round(this.width / 2)
        fillHeight = Math.round(this.height / 2)
      }
      else {
        fillWidth = this.horizontalSym ? this.width : Math.round(this.width / 2)
        fillHeight = this.verticalSym ? this.height : Math.round(this.height / 2)
      }

      for (let x = 1; x <= fillWidth; x += 1) {
        for (let y = 1; y <= fillHeight; y += 1) {
          if (Math.random() > this.blankProbability) {
            continue
          }

          this.blanksUpdate(`${x}:${y}`)
        }
      }

      this.addCrossClasses()
    },

    clearGrid () {
      this.blanks = []
      this.letters = {}
      this.filledWords = []
    },

    rebuildGrid ({ width, height }) {
      this.width = width
      this.height = height
    },

    changeSize ({ width, height }) {
      if (width && this.width !== width) {
        this.width = width
      }
      if (height && this.height !== height) {
        this.height = height
      }
    },

    blanksUpdate (id) {
      const [x, y] = id.split(':')
      const diagonalIndex = `${this.width - x + 1}:${this.height - y + 1}`
      const verticalIndex = `${this.width - x + 1}:${y}`
      const horizontalIndex = `${x}:${this.height - y + 1}`

      if (this.blanks.includes(id)) {
        this.removeBlank(id)

        if (this.verticalSym) {
          this.removeBlank(verticalIndex)
        }

        if (this.horizontalSym) {
          this.removeBlank(horizontalIndex)
        }

        if (this.verticalSym && this.horizontalSym) {
          this.removeBlank(diagonalIndex)
        }
        this.addCrossClasses()

        return
      }

      this.addBlank(id)

      if (this.verticalSym) {
        this.addBlank(verticalIndex)
      }

      if (this.horizontalSym) {
        this.addBlank(horizontalIndex)
      }

      if (this.verticalSym && this.horizontalSym) {
        this.addBlank(diagonalIndex)
      }
      this.addCrossClasses()
    },

    addBlank (id) {
      this.blanks.push(id)
    },

    removeBlank (id) {
      this.blanks = this.blanks.filter((blank) => blank !== id)
    },

    inputLetter ({ x, y, value }) {
      this.letters[`${x}:${y}`] = value
    },

    addIndexes (words) {
      return words
        .map((word) => {
          const { index } = this.startCells
            .find(({ x, y }) => word.x === x && word.y === y)

          return { ...word, index }
        })
    },

    focusCell (x, y) {
      this.focusedCell = `${x}:${y}`
    },

    async pasteWord ({ word: { word }, x, y, isVertical }) {
      this.prevWord = { x, y, isVertical, word: { word } }
      Array.from(word).forEach((letter, index) => {
        const key = isVertical ? `${x}:${y + index}` : `${x + index}:${y}`

        this.letters[key] = letter
      })

      this.filledWords.push({ word, x, y, isVertical })
      const url = `https://crossword.teacherlight.ru:3443/crossword/clues/${this.locale}find/${word}`
      let response

      if ('caches' in window) {
        const cache = await caches.open('clues')

        response = await cache.match(url)

        if (response) {
          response = await response.json()
          this.clues.push({ word, data: response.clues })
          this.filledWords[this.filledWords.length - 1].clue = response.clues[
            this.getRandomInt(response.clues.length - 1)
          ]
        }

        response = await fetch(url)
        await cache.put(url, response)

        response = await cache.match(url)
        response = await response.json()

        this.clues.push({ word, data: response.clues })
        this.filledWords[this.filledWords.length - 1].clue = response.clues[
          this.getRandomInt(response.clues.length - 1)
        ]
      }

      response = await fetch(url)
      response = await response.json()

      this.clues.push({ word, data: response.clues })
      this.filledWords[this.filledWords.length - 1].clue = response.clues[
        this.getRandomInt(response.clues.length - 1)
      ]
    },

    pasteClue ({ word: { clue, x, y, isVertical } }) {
      const index = this.filledWords.findIndex((item) => item.x === x &&
        item.y === y && item.isVertical === isVertical)

      if (index !== -1) {
        this.filledWords[index].clue = clue
      }
      // this.$http.post(
      //   'clues/create',
      //   { crossword: 1, clue: clue.id }
      // )
      //   .then(() => {
      //   })
      //   .catch(console.log)
    },

    newCrossword () {
      fetch(
        'https://crossword.teacherlight.ru:3443/crossword/create',
        {
          method: 'POST',
          data: {
            name: 'Test',
            description: '',
            words: '[]',
            blanks: '[]',
            width: this.width,
            height: this.height,
          },
        },
      )
        .then((response) => {
          if (!response.success) {
            return
          }

          const indexes = Object.keys(this.letters)

          for (let idx = indexes.length - 1; idx >= 0; idx -= 1) {
            this.letters[indexes[idx]] = ''
          }

          this.crosswordId = response.data.id
          this.blanks = JSON.parse(response.data.blanks)
          this.filledWords = JSON.parse(response.data.words)
        })
    },

    saveCrossword () {
      fetch(
        `edit/${this.crosswordId}`,
        {
          data: {
            words: JSON.stringify(this.filledWords),
            blanks: JSON.stringify(this.blanks),
            width: this.width,
            height: this.height,
          },
        },
      )
    },

    async loadCrossword (id) {
      const response = await fetch(`https://crossword.teacherlight.ru:3443/crossword/${id}`)
        .catch(console.log)

      if (response && response.success) {
        const { words, blanks, width, height } = response.data

        this.filledWords = JSON.parse(words)
        this.blanks = JSON.parse(blanks)
        this.height = height
        this.width = width
      }
    },

    getRandomInt (max) {
      return Math.floor(Math.random() * Math.floor(max))
    },

    generateName () {
      // eslint-disable-next-line no-magic-numbers
      const index = this.getRandomInt(10000)
      const nounIndex = this.getRandomInt(nouns.length)
      const adjectiveIndex = this.getRandomInt(adjectives.length)

      // eslint-disable-next-line no-magic-numbers
      return `${nouns[nounIndex]}-${adjectives[adjectiveIndex]}-${String(index).padStart(5, '0')}`
    },

    async saveGrid () {
      const params = {
        name: this.generateName(),
        description: this.statsView,
        width: this.width,
        height: this.height,
        blanks: JSON.stringify(this.blanks.sort()),
      }

      const response = await fetch(
        'https://crossword.teacherlight.ru:3443/crossword/grids',
        {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
          },
          body: Object.keys(params)
            .map((key) => encodeURIComponent(key) + '=' + encodeURIComponent(params[key]))
            .join('&'),
        },
      )
        .catch((error) => {
          console.log(error)
        })

      const json = await response.json()

      if (json && json.success) {
        this.loadGrid(json.data.grid)
        this.updateGrids()
      }
    },

    loadGrid (grid) {
      if (grid && grid.blanks) {
        if (grid.width && this.width !== grid.width) {
          this.width = grid.width
        }
        if (grid.height && this.height !== grid.height) {
          this.height = grid.height
        }
        this.blanks = JSON.parse(grid.blanks)
        this.gridName = grid.name

        window.history.replaceState(
          '',
          document.title,
          `${window.location.origin}${window.location.pathname}?width=${this.width}&height=${this.height}&blanks=${this.blanks.join()}`,
        )

        this.addCrossClasses()
      }
    },

    lettersUpdate ({ letters }) {
      Object.assign(this.letters, letters)
    },

    getSuggestionsUrl (query, page = 0) {
      return `words/find/${page}/${query}`
    },

    getSuggestions (queries, useCache = true) {
      return Promise.all(queries.map(async (query) => {
        if (!query.includes('_')) {
          return
        }
        let response
        const url = `https://crossword.teacherlight.ru:3443/crossword/words/${this.locale}find/${query}`

        if ('caches' in window && useCache) {
          const cache = await caches.open('words')

          this.log.push(`WORDS FOR ${query}`)
          response = await cache.match(url)

          if (response) {
            response = await response.json()
            return { query, data: response.words.filter(Boolean) }
          }

          response = await fetch(url)
          await cache.put(url, response)

          response = await cache.match(url)
          response = await response.json()

          this.log = []
          return { query, data: response.words.filter(Boolean) }
        }

        this.log.push(`WORDS FOR ${query}`)
        response = await fetch(url)
        response = await response.json()

        this.log = []
        return { query, data: response.words.filter(Boolean) }
      }))
    },

    getSuggestionCounts (queries, useCache = true) {
      return Promise.all(queries.map(async (query) => {
        if (!query.includes('_')) {
          return { query, count: 1 }
        }
        let response
        const url = `https://crossword.teacherlight.ru:3443/crossword/words/${this.locale}count/${query}`

        if ('caches' in window && useCache) {
          const cache = await caches.open('counts')

          this.log.push(`COUNT FOR ${query}`)
          response = await cache.match(url)

          if (response) {
            response = await response.json()
            return { query, count: response.count }
          }

          response = await fetch(url)
          await cache.put(url, response)

          response = await cache.match(url)
          response = await response.json()

          this.log = []
          return { query, count: response.count }
        }

        this.log.push(`COUNT FOR ${query}`)
        response = await fetch(url)
        response = await response.json()

        this.log = []
        return { query, count: response.count }
      }))
    },

    changeDensity ({ density }) {
      // eslint-disable-next-line no-magic-numbers
      this.blankProbability = 1 / density * 2
    },

    addCrossClasses () {
      this.$nextTick(() => {
        this.$refs.grid.$children
          .map((component) => {
            component.$el.classList.remove('cross')
            return component
          })
          .filter(({ x, y }) => this.crosses.includes(`${x}:${y}`))
          .forEach(({ $el: el }) => el.classList.add('cross'))
      })
    },
  },
}
</script>
