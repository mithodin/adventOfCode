export function parse(input: string): Array<Array<number>> {
    const elves = input.split("\n\n");
    return elves.map((elf) => elf.split("\n").filter(Boolean).map((num) => {
        const result = Number.parseInt(num, 10);
        if (!Number.isFinite(result)) {
            console.error(`input [${num}] could not be parsed as number: [${result}]`);
        }
        return result;
    }));
}

export function getTopN(input: Array<number>, n = 3): Array<number> {
    const top = input.slice(0, n);
    top.sort((n1, n2) => n1 - n2);
    return input.slice(n).reduce((topN, next) => {
        if (next <= topN[0]) {
            return topN;
        }
        return [next, ...topN.slice(1)].sort((n1, n2) => n1 - n2);
    }, top);
}

function arraySum(elf: Array<number>) {
    return elf.reduce((sum, next) => sum + next, 0);
}

export function solve1(input: string) {
    const elves = parse(input);
    const cals = elves.map(arraySum);
    return Math.max(...cals);
}

export function solve2(input: string) {
    const elves = parse(input);
    const cals = elves.map(arraySum);
    const top3 = getTopN(cals, 3);
    return arraySum(top3);
}
