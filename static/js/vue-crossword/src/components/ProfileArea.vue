<template>
  <div class="profile-area component">
    <div v-if="user" class="profile">
      <img :src="user.image" :alt="user.name" />
      <span>Signed in as {{ user.name }}.</span>
    </div>
  </div>
</template>

<script>
// <button @click="signOut">Sign Out</button>
// <button v-else @click="signIn">Sign In</button>
export default {
  name: 'ProfileArea',

  props: {
    user: { type: Object, default: () => null },
  },

  async mounted () {
    // const result = await this.$gapi.isSignedIn()

    // if (result) {
    //   this.signIn()
    // }
  },

  methods: {
    async signIn () {
      const user = await this.$gapi.signIn().catch((error) => {
        console.error('Not signed in: %s', error.error)
      })

      this.$bus.$emit('user::update', user)
    },

    async signOut () {
      await this.$gapi.signOut().catch((error) => {
        console.error('Not signed out: %s', error.error)
      })

      this.$bus.$emit('user::clear')
    },
  },
}
</script>

<style lang="css" scoped>
</style>
