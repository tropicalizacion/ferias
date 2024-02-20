<template>
  <ul>
    <li
      v-for="(page, index) in pages"
      :key="index"
    >
      <div class="inner">
        <router-link :to="page.href">
          {{ page.title }}
        </router-link>
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'MenuArea',

  props: {
    pages: {
      type: Array,
      default: () => [
        { title: 'Builder', href: '/builder' },
        { title: 'Crossword', href: '/crossword' },
      ],
    },
  },
}
</script>
