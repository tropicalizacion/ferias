module.exports = {
  runtimeCompiler: true,
  css: { sourceMap: true },
  publicPath: process.env.NODE_ENV === 'production' ? '/vue-crossword/' : '/',
}
