export default class Pair {
  key: string
  value: number
  readonly _amount: number

  constructor(key: string, value: number) {
    this.key = key
    this.value = value
  }
}
