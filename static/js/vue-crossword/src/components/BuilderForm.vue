<template>
  <div class="builder-form page-inner">
    <transition name="slide-right" mode="in-out">
      <div v-show="changeSizeMode" class="controls">
        <div class="grid-name-field">
          Grid Name:
          <input
            v-model="name"
            type="text"
            maxlength="40"
          />
        </div>

        <span>
          Grid Width:
          <input
            v-model="width"
            type="number"
            maxlength="3"
            min="2"
            max="40"
          />
        </span>
        <input
          ref="sizeWidth"
          v-model="width"
          type="range"
          size="4"
          min="2"
          max="40"
        />

        <span>
          Grid Height:
          <input
            v-model="height"
            type="number"
            maxlength="3"
            min="2"
            max="40"
          />
        </span>
        <input
          ref="sizeHeight"
          v-model="height"
          type="range"
          size="4"
          min="2"
          max="40"
        />

        <span>
          Density: 1 /
          <input
            v-model="density"
            type="number"
            maxlength="3"
            min="4"
            max="40"
          />
        </span>
        <input
          ref="sizeHeight"
          v-model="density"
          type="range"
          size="4"
          min="4"
          max="40"
        />
      </div>
    </transition>

    <transition name="slide-right" mode="out-in">
      <div v-show="!changeSizeMode" class="forms-list-wrapper horizontal">
        <label>Horizontal questions:</label>
        <div class="forms-list">
          <word-form
            v-for="(word, index) in horizontalWords"
            :key="`h${index}`"
            :x="word.x"
            :y="word.y"
            :clues="clues"
            :letters="letters"
            :loading="loading"
            :index="word.index"
            :length="word.length"
            :is-vertical="false"
            :next-query="nextQuery"
            :suggestions="suggestions"
            :filled-words="filledWords"
            :focused-cell="focusedCell"
            :suggestion-counts="suggestionCounts"
            @input="(payload) => $emit('input', payload)"
            @focus-cell="(x, y) => $emit('focus-cell', x, y)"
            @paste-clue="(payload) => $emit('paste-clue', payload)"
            @paste-word="(payload) => $emit('paste-word', payload)"
            @remove-word="(payload) => $emit('remove-word', payload)"
            @letters-update="(payload) => $emit('letters-update', payload)"
          />
        </div>
      </div>
    </transition>

    <transition name="slide-left" mode="out-in">
      <div v-show="!changeSizeMode" class="forms-list-wrapper vertical">
        <label>Vertical questions:</label>
        <div class="forms-list">
          <word-form
            v-for="(word, index) in verticalWords"
            :key="`v${index}`"
            :x="word.x"
            :y="word.y"
            :clues="clues"
            :letters="letters"
            :loading="loading"
            :length="word.length"
            :index="word.index"
            :is-vertical="true"
            :next-query="nextQuery"
            :suggestions="suggestions"
            :filled-words="filledWords"
            :focused-cell="focusedCell"
            :suggestion-counts="suggestionCounts"
            @input="(payload) => $emit('input', payload)"
            @focus-cell="(x, y) => $emit('focus-cell', x, y)"
            @paste-clue="(payload) => $emit('paste-clue', payload)"
            @paste-word="(payload) => $emit('paste-word', payload)"
            @remove-word="(payload) => $emit('remove-word', payload)"
            @letters-update="(payload) => $emit('letters-update', payload)"
          />
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
// @form-leaved="(payload) => $emit('form-leaved', payload)"
// @form-hovered="(payload) => $emit('form-hovered', payload)"
// @form-leaved="(payload) => $emit('form-leaved', payload)"
// @form-hovered="(payload) => $emit('form-hovered', payload)"
import WordForm from './WordForm'

export default {
  name: 'BuilderForm',

  components: { WordForm },

  props: {
    size: { type: Object, default: () => ({}) },
    words: { type: Array, default: () => [] },
    clues: { type: Array, default: () => [] },
    letters: { type: Object, default: () => ({}) },
    loading: { type: Boolean, default: () => false },
    gridName: { type: String, default: () => '' },
    nextQuery: { type: String, default: () => '' },
    filledWords: { type: Array, default: () => [] },
    suggestions: { type: Array, default: () => [] },
    focusedCell: { type: String, default: () => '0:0' },
    twoLetterWords: { type: Array, default: () => [] },
    threeLetterWords: { type: Array, default: () => [] },
    changeSizeMode: { type: Boolean, default: () => false },
    // eslint-disable-next-line no-magic-numbers
    blankProbability: { type: Number, default: () => 4 },
    suggestionCounts: { type: Array, default: () => [] },
  },

  data () {
    return {
      max: 40,
      name: '',
      width: this.size.width,
      height: this.size.height,
      density: this.blankProbability,
    }
  },

  computed: {
    verticalWords () {
      return this.words.filter(({ type }) => type === 'vertical')
    },

    horizontalWords () {
      return this.words.filter(({ type }) => type === 'horizontal')
    },
  },

  watch: {
    name (value) {
      this.$emit('changename', { name: value })
    },

    width (value) {
      this.$emit('changesize', { width: value })
    },

    height (value) {
      this.$emit('changesize', { height: value })
    },

    density (value) {
      this.$emit('density', {
        density: Number(value),
      })
    },

    size: {
      handler ({ width, height }) {
        this.width = width
        this.height = height

        this.$emit('rebuild', {
          width: Number(this.width),
          height: Number(this.height),
        })
      },
      deep: true,
    },
  },

  async mounted () {
    const response = await fetch(
      'https://project-names.herokuapp.com/names',
      {
        mode: 'no-cors',
      }
    )

    this.name = await response.text()
  },
}
</script>
