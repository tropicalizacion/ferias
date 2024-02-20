<template>
  <div
    :class="{
      next: nextQuery === query,
      error: suggestionsCount === 0,
    }"
    class="word-form"
  >
    <div v-if="loading && !suggested.length" class="word-form-overlay">
      <div class="inner">
        Loading `{{ query.split('').join(' ') }}`
      </div>
    </div>

    <div v-if="suggestionsVisible" class="modal-area suggestions">
      <div class="inner">
        <a href="#" class="close" @click.prevent="hideSuggestions">
          X
        </a>
        <ul class="suggested-list">
          <li
            v-for="wordItem in suggested"
            :key="wordItem.id"
            :style="{ width: `${length / 1.618}em` }"
          >
            <a
              href="#"
              @mouseover="$emit('suggestion-hover', { x, y, isVertical, word })"
              @mouseleave="$emit('suggestion-leave')"
              @click.prevent="pasteWord(wordItem)"
              v-html="getWordHtml(wordItem)"
            ></a>
          </li>
        </ul>
        <div class="controls">
          <div class="prev go-to-page">
            <a href="#" @click.prevent="prevPage">
              Prev.
            </a>
          </div>
          <div class="index go-to-page">
            Page {{ page + 1 }}
          </div>
          <div class="next go-to-page">
            <a href="#" @click.prevent="nextPage">
              Next.
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-if="cluesVisible" class="modal-area clues">
      <div class="inner">
        <a href="#" class="close" @click.prevent="hideClues">
          X
        </a>
        <ol class="clues-list">
          <li v-for="clue in ownClues" :key="clue.id">
            <a
              href="#"
              @click.prevent="pasteClue(clue)"
              v-html="getClueHtml(clue)"
            ></a>
            <br />
          </li>
        </ol>
      </div>
    </div>

    <span class="index-number">
      {{ index }}
    </span>

    <div class="question">
      <div class="answer-letters">
        <div
          v-for="(letter, idx) of cells"
          :key="idx"
          :class="{ focused: isActive(idx), filled: isFilled(idx) }"
          class="letter"
        >
          <input
            v-model="answer[idx]"
            :data-idx="idx"
            type="text"
            size="1"
            minlength="1"
            maxlength="1"
            @blur="onBlur"
            @focus="onFocus"
            @input="onInputLetter"
            @paste.prevent.stop="onPaste"
          />
        </div>
      </div>
      <div class="clue">
        <textarea
          v-if="word && word.clue"
          ref="question"
          v-model="word.clue.name"
          :cols="cols"
          :rows="rows"
          type="text"
          class="textarea"
          @focus="showClues"
        ></textarea>
      </div>
      <div v-if="noClue" class="green-plus">
        +
      </div>
      <div style="clear: both;"></div>
    </div>

    <div class="words-count">
      <a
        href="#"
        title="Show variants"
        @click.prevent="toggleModal(query)"
        v-text="suggestionsText"
      ></a>
      <a
        v-if="word"
        class="danger"
        href="#"
        title="Remove word"
        @click.prevent="removeWord"
      >
        Remove word
      </a>
    </div>
  </div>
</template>

<script>
// @mouseover="$emit('form-hovered', { x, y, isVertical, length })"
// @mouseleave="$emit('form-leaved')"
export default {
  name: 'WordForm',

  props: {
    x: { type: Number, default: () => 0 },
    y: { type: Number, default: () => 0 },
    index: { type: Number, default: () => 0 },
    clues: { type: Array, default: () => [] },
    length: { type: Number, default: () => 0 },
    letters: { type: Object, default: () => ({}) },
    nextQuery: { type: String, default: () => '' },
    loading: { type: Boolean, default: () => false },
    isVertical: { type: Boolean, default: () => false },
    filledWords: { type: Array, default: () => [] },
    suggestions: { type: Array, default: () => [] },
    focusedCell: { type: String, default: () => '0:0' },
    suggestionCounts: { type: Array, default: () => [] },
  },

  data () {
    return {
      page: 0,
      active: null,
      answer: Array.from({ length: this.length }).fill(''),
      timeout: null,
      question: '',
      cluesVisible: false,
      suggestionsVisible: false,
    }
  },

  computed: {
    suggestionsText () {
      return !this.query.includes('_') && this.ownClues
        ? `Found ${this.ownClues.length} clues`
        : `Found ${this.suggestionsCount} words`
    },

    noClue () {
      return this.question && this.word &&
        !this.ownClues.map(({ name }) => name).includes(this.question)
    },

    word () {
      return this.answer.every(Boolean)
        ? this.filledWords.find(({ word }) => (
          word === this.answer.join('')
        ))
        : null
    },

    query () {
      return Object.keys(this.ownLetters)
        .map((key) => this.ownLetters[key] || '_')
        .join('')
    },

    ownSuggestions () {
      const data = this.suggestions.find(({ query }) => query === this.query)

      return data ? data.data : []
    },

    ownClues () {
      const clues = this.clues.find(({ word }) => word === this.answer.join(''))

      return clues ? clues.data : []
    },

    cells () {
      let i = this.isVertical ? this.x : this.y

      return Array.from({ length: this.length })
        .map(() => ({
          x: this.isVertical ? i++ : this.x, // eslint-disable-line
          y: this.isVertical ? this.y : i++, // eslint-disable-line
          value: '',
        }))
    },

    ownCells () {
      const cells = []

      if (this.isVertical) {
        const end = this.length + this.y

        for (let i = this.y; i < end; i += 1) {
          cells.push(`${this.x}:${i}`)
        }
        return cells
      }

      const end = this.length + this.x

      for (let i = this.x; i < end; i += 1) {
        cells.push(`${i}:${this.y}`)
      }
      return cells
    },

    ownLetters () {
      const letters = {}

      this.ownCells.forEach((cell) => {
        letters[cell] = this.letters[cell]
      })

      return letters
    },

    suggested () {
      const data = this.suggestions.find(({ query }) => query === this.query)

      // eslint-disable-next-line no-magic-numbers
      return data ? data.data : []
    },

    suggestionsCount () {
      const data = this.suggestionCounts.find(({ query }) => query === this.query)

      return data ? data.count : 0
    },

    cols () {
      return 28 // eslint-disable-line no-magic-numbers
    },

    rows () {
      return this.question
        // eslint-disable-next-line no-magic-numbers
        ? parseInt(this.question.length / this.cols * 1.618)
        : 1
    },
  },

  watch: {
    query () {
      this.answer = Object.values(this.ownLetters)
    },
  },

  methods: {
    removeWord () {
      const { x, y, isVertical, word } = this

      this.$emit('remove-word', ({ x, y, isVertical, word }))
      this.question = ''
    },

    toggleModal (query) {
      if (this.answer.includes('')) {
        if (this.suggestionsVisible) {
          this.hideSuggestions()
        }
        else {
          this.showSuggestions(query)
        }
      }
      else {
        if (this.cluesVisible) {
          this.hideClues()
        }
        else {
          this.showClues(query)
        }
      }
    },

    showModal (query) {
      if (this.answer.includes('')) {
        this.showSuggestions(query)
      }
      else {
        this.showClues()
      }
    },

    showClues () {
      this.cluesVisible = !!this.word
    },

    hideClues () {
      this.cluesVisible = false
    },

    prevPage () {
      this.page = this.page ? this.page - 1 : 0
    },

    nextPage () {
      this.page += 1
    },

    getWordHtml ({ word }) {
      return word
    },

    pasteWord (word) {
      this.$emit('paste-word', {
        word,
        x: this.x,
        y: this.y,
        isVertical: this.isVertical,
      })
      this.hideSuggestions()
    },

    hideSuggestions () {
      this.suggestionsVisible = false
    },

    getClueHtml ({ name }) {
      return name
    },

    pasteClue (clue) {
      this.word.clue = clue
      this.$emit('paste-clue', { word: this.word })
      this.question = clue.name
      this.hideClues()
    },

    showSuggestions () {
      this.suggestionsVisible = true
    },

    onInputLetter (e) {
      this.$emit('input', {
        value: e.target.value.toUpperCase(),
        ...this.getCellPosition(e.target.dataset.idx),
      })

      if (e.target.value !== '') {
        this.$nextTick(() => {
          const nextEl = e.target.parentElement.nextElementSibling

          if (nextEl) {
            nextEl.children[0].focus()
            document.execCommand('selectAll')
          }
          else {
            this.$refs.question.focus()
          }

          this.showSuggestions(this.query)
        })
      }
    },

    getCellPosition (index) {
      return this.isVertical
        ? { x: this.x, y: Number(this.y) + Number(index) }
        : { x: Number(this.x) + Number(index), y: this.y }
    },

    onFocus (e) {
      this.$emit(
        'focus-cell',
        this.isVertical
          ? Number(this.x)
          : Number(this.x) + Number(e.target.dataset.idx),
        this.isVertical
          ? Number(this.y) + Number(e.target.dataset.idx)
          : Number(this.y),
      )
    },

    onBlur () {
      this.$emit('focus-cell', 0, 0)
    },

    isActive (idx) {
      return this.isVertical
        ? `${this.x}:${Number(this.y) + Number(idx)}` === this.focusedCell
        : `${Number(this.x) + Number(idx)}:${this.y}` === this.focusedCell
    },

    isFilled (idx) {
      return this.isVertical
        ? this.$root.getAllWordCells(this.filledWords)
          .includes(`${this.x}:${Number(this.y) + Number(idx)}`)
        : this.$root.getAllWordCells(this.filledWords)
          .includes(`${Number(this.x) + Number(idx)}:${this.y}`)
    },

    onPaste (e) {
      const text = e.clipboardData.getData('text')

      if (typeof text === 'string' && text && text.length === this.length) {
        this.answer = text.split('')
      }
    },
  },
}
</script>
