export default {
  methods: {
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
  },
}
