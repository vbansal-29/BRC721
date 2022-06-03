import { Counter } from './counter'
import { SHA3 } from 'sha3';

export class Bucket {
    coins: number
    _owners: string[]
    name: string
    symbol: string
    tokenId: string
  
    constructor(to: string, name: string, symbol = '') {
      this._owners = [to]
      this.name = name
      this.symbol = symbol
      const hash = new SHA3(512)
      this.tokenId = hash.digest({_owners: [to], name: name, symbol: symbol})
    }
  }