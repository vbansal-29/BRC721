import { Bucket } from './bucket'

export class BRC721 {
    computer: any
    constructor(computer: any) {
        this.computer = computer
    }
    owner (bucket: Bucket): string[] {
        return bucket._owners
    }
    async transfer(from: string, to: string, tokenId: number) {
        const revs = await this.computer.getRevs(tokenId)
        const bucket = await Promise.resolve(revs.map(rev => this.computer.sync(rev)))
        if (!bucket._owners.includes(from)) {
          throw new Error()
        }
        else {
          bucket._owners = bucket._owners.filter(item => item !== from)
          bucket._owners.push(to)
        }
    }
    async balance(publicKeyString: string): Promise<number> {
        const revs = await this.computer.getRevs(publicKeyString)
        const objects = await Promise.all(revs.map(rev => this.computer.sync(rev)))
        return objects.length
    }
}