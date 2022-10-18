
import Pair from './pair'

describe('Pair Class', () => {
  it('should create a Pair smart object', async () => {
    const pair = new Pair('key', 0)

    expect(pair).toBeDefined()
    expect(pair.key).toEqual('key')
    expect(pair.value).toEqual(0)
  })
})
