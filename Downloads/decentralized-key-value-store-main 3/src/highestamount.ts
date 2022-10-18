import Pair from './pair'

interface IStore {
  get(key: string): Promise<number>
  set(key: string, value: number): Promise<Pair>
}
export default class Store implements IStore {
  computer: any

  constructor(computer: any) {
    this.computer = computer
  }

  async get(key: string): Promise<number> {
    const revs = await this.computer.queryRevs({ contractName: 'Pair' })
    const pairs: Pair[] = await Promise.all(revs.map((rev) => this.computer.sync(rev)))
    const filtered_pairs = pairs.filter((pair) => pair.key === key)
    let max = -Number.MAX_VALUE
    let sum = 0
    for(let i = 0; i < filtered_pairs.length; i++){
      if (filtered_pairs[i]._amount > max){
        max = filtered_pairs[i]._amount
      }
    }
    return pairs.find((pair) => pair._amount === max).value


  }

  async set(key: string, value: number): Promise<Pair> {
    return await this.computer.new(Pair, [key, value])
  }
}
