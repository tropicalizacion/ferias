<template>
  <div
    class="cell-item"
    @mouseup="onMouseUp"
    @mousedown="onMouseDown"
    @mouseenter="onMouseEnter"
  >
    <sup class="word-start">
      {{ number }}
    </sup>
    <input
      v-model="value"
      type="text"
      size="1"
      minlength="1"
      maxlength="1"
      readonly
      @click="onClick"
      @focus="onFocus"
      @input="onInput"
    />
  </div>
</template>

<script>
export default {
  name: 'Cell',

  props: {
    x: { type: Number, required: true },
    y: { type: Number, required: true },
    value: { type: String, default: () => '' },
    number: { type: Number, default: () => 0 },
    isBlank: { type: Boolean, default: () => false },
    isActive: { type: Boolean, default: () => false },
  },

  computed: {
    identifier () {
      return `${this.x}:${this.y}`
    },
  },

  methods: {
    onMouseEnter () {
      this.$emit('cellmouseenter', { id: this.identifier })
    },

    onMouseDown () {
      this.$emit('cellmousedown', { id: this.identifier })
    },

    onMouseUp () {
      this.$emit('cellmouseup', { id: this.identifier })
    },

    onClick () {
      this.$emit('cellclick', { id: this.identifier })
    },

    onInput () {
      this.$emit('cellinput', { id: this.identifier })
    },

    onFocus (e) {
      if (this.$parent.isEditBlanks) {
        return e.target.blur()
      }
    },
  },
}
</script>
