/* eslint-disable */

Array.prototype.unique = function () {
  const unique = {}
  const array = []

  this.forEach((key) => {
    if (unique.hasOwnProperty(key)) {
      return
    }
    array.push(key)
    unique[key] = 1
  })

  return array
}

String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase()
}
