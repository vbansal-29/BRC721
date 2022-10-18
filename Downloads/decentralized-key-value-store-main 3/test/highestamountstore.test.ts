import { Computer } from 'bitcoin-computer-lib'
import Store from '../src/highestamount'

describe('Key Value Store', () => {
  it('should create a Pair smart object', async () => {
    const computer = new Computer({ seed: 'replace this seed' })
    const query = new Store(computer)
    const pair = await query.set('Key', 0)

    expect(pair).toBeDefined()
    expect(pair.key).toEqual('Key')
    expect(pair.value).toEqual(pair._amount)
  })

it('should return the Pair smart object average value', async () => {
  const computer = new Computer({ seed: 'replace this seed' })
  const query = new Store(computer)
  const pair0 = await query.set('Key', 0)
  const pair1 = await query.set('Key', 1)
  let value = (pair0.value + pair1.value)/2
  expect(await query.get('Key')).toEqual(value)
})
})
