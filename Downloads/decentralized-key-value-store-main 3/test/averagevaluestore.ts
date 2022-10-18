import { Computer } from 'bitcoin-computer-lib'
import Store from '../src/highestamount'

describe('Key Value Store', () => {
  it('should create a Pair smart object', async () => {
    const computer = new Computer({ seed: 'replace this seed' })
    const query = new Store(computer)
    const pair = await query.set('Key')

    expect(pair).toBeDefined()
    expect(pair.key).toEqual('Key')
    expect(pair.value).toEqual(pair._amount)
  })

it('should return the Pair smart object with the higher amount', async () => {
  const computer = new Computer({ seed: 'replace this seed' })
  const query = new Store(computer)
  const pair0 = await query.set('Key', 0)
  const pair1 = await query.set('Key', 1)
  let value = 'Value0'
  if (pair1._amount > pair0._amount) {
    value = 'Value1'
  }
  // Assuming pair0 has the higher amount
  expect(await query.get('Key')).toEqual(value)
})
})
