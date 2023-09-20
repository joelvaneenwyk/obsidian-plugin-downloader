import { expose } from 'threads/worker'

expose(function work () {
  return 'This is the way!'
})
